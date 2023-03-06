# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate,  nowdate
from frappe.commands.utils import set_config


class SetLimit(Document):
	def onload(self):
		if frappe.session.user!='Administrator':
			frappe.local.flags.redirect_location = 'app/home'
			raise frappe.Redirect			

	def validate(self):
		self.validate_all_field_values()
		self.set_set_limits_in_site_config()

	def validate_all_field_values(self):	
		if self.no_of_user <=0:
			frappe.throw(_(msg='No of users, restriction should be greater than 0.'),title=_('Error: No. Of Users'))
		elif self.no_of_emails <=0:
			frappe.throw(_(msg='No of emails per month, restriction should be greater than 0.'),title=_('Error: No. Of Emails Per Month'))
		elif self.max_space <=0:
			frappe.throw(_(msg='Space set_limit, restriction should be greater than 0.'),title=_('Error: Space SetLimit'))
		elif getdate(self.site_expiry) < getdate(nowdate()) or self.site_expiry==None or self.site_expiry=='':
			frappe.throw(_(msg='Site Expiry cannot be past date or empty.'),title=_('Error: Site Expiry Date'))
		elif self.support_email==None or self.support_email =='':
			frappe.throw(_(msg='Please put support email id.'),title=_('Error: Support Email'))
		elif self.support_phone==None or self.support_phone =='':
			frappe.throw(_(msg='Please put support phone no.'),title=_('Error: Support Phone'))


	def set_set_limits_in_site_config(self):
		from frappe.installer import update_site_config
		# delete set_limit key first
		update_site_config("limits",value="None",validate=False)
		# set fresh set_limits
		update_site_config("limits", self.get_set_limits(), validate=False)

	def get_set_limits(self):
		set_limits={
				"users": self.no_of_user,
				"emails": self.no_of_emails,
				"space": self.max_space,
				"expiry": self.site_expiry,
				"support_email":self.support_email,
				"support_phone":self.support_phone
			}
		return frappe._dict(set_limits)		
