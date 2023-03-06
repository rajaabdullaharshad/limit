from __future__ import unicode_literals, print_function
import frappe
from limit.limits import get_limits, update_limits
from frappe import _
from frappe.utils import cint

from frappe.email.smtp import SMTPServer
from frappe.email.queue import get_emails_sent_this_month,get_emails_sent_today
from frappe.installer import update_site_config

class MaxUsersReachedError(frappe.ValidationError): pass
class EmailLimitCrossedError(frappe.ValidationError): pass

def validate_user_limit(self,method):
		'''
			Validate if user limit has been reached for System Users
			Checked in 'Validate' event as we don't want welcome email sent if max users are exceeded.
		'''

		if self.user_type == "Website User":
			return

		if not self.enabled:
			# don't validate max users when saving a disabled user
			return

		limits = get_limits()
		if not limits.users:
			# no limits defined
			return

		total_users = get_total_users()
		if total_users==None:
			total_users=0
		if self.is_new():
			# get_total_users gets existing users in database
			# a new record isn't inserted yet, so adding 1
			total_users += 1
		if total_users > limits.users:
			message =_("Sorry. You have reached the maximum user limit of <b> {0} </b> for your subscription.<br> You can either disable an existing user or <br>{1} ").format(cint(limits.users),
				'Contact us on email <b>{0}</b> or phone <b>{1}</b>'.format(limits.support_email,limits.support_phone))	
			frappe.throw(msg=message,title='User Subscription Limit Reached', exc=MaxUsersReachedError)			

def get_total_users():
	from frappe.core.doctype.user.user import STANDARD_USERS
	"""Returns total no. of system users"""
	return frappe.db.sql('''select sum(simultaneous_sessions) from `tabUser`
		where enabled=1 and user_type="System User"
		and name not in ({})'''.format(", ".join(["%s"]*len(STANDARD_USERS))), STANDARD_USERS)[0][0]   

def mute_emails_on_email_limit_reached():
	try:
		check_email_limit(['admin@greycube.in'])
	except:	
		update_site_config('mute_emails',True)
	else:
		update_site_config('mute_emails', False)


def update_boot_with_limits(bootinfo):
	from limit.limits import get_limits, get_expiry_message
	# limits
	bootinfo.limits = get_limits()
	bootinfo.expiry_message = get_expiry_message()

	return bootinfo	

def check_email_limit(recipients):
	print('inside'*10)
	import json
	# if using settings from site_config.json, check email limit
	# No limit for own email settings
	smtp_server = SMTPServer()

	if (smtp_server.email_account
		or frappe.flags.in_test):
		monthly_email_limit = frappe.conf.get('limits', {}).get('emails')
		daily_email_limit = cint(frappe.conf.get('limits', {}).get('daily_emails'))
		if frappe.flags.in_test:
			monthly_email_limit = 500
			daily_email_limit = 50
		if daily_email_limit:
			# get count of sent mails in last 24 hours
			today = get_emails_sent_today()
			if (today + len(recipients)) > daily_email_limit:
				throw(_("Cannot send this email. You have crossed the sending limit of {0} emails for this day.").format(daily_email_limit),
					EmailLimitCrossedError)

		if not monthly_email_limit:
			return

		# get count of mails sent this month
		this_month = get_emails_sent_this_month()
		if (this_month + len(recipients)) > monthly_email_limit:
			throw(_("Cannot send this email. You have crossed the sending limit of {0} emails for this month.").format(monthly_email_limit),
				EmailLimitCrossedError)		             
