# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "limit"
app_title = "Limit"
app_publisher = "GreyCube Technologies"
app_description = "Limit Frappe Erpnext usage via site_config"
app_icon = "octicon octicon-tools"
app_color = "red"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/limit/css/limit.css"
app_include_js = "/assets/limit/js/limit.js"

# include js, css files in header of web template
# web_include_css = "/assets/limit/css/limit.css"
# web_include_js = "/assets/limit/js/limit.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "limit.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "limit.install.before_install"
# after_install = "limit.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "limit.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events
on_login=["limit.limits.check_if_expired"]
boot_session = "limit.api.update_boot_with_limits"


before_write_file = "limit.limits.validate_space_limit"

doc_events = {
	"User": {
		"before_save": "limit.api.validate_user_limit",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"limit.tasks.all"
	# ],
	"daily": [
		"limit.utils.scheduler.disable_scheduler_on_expiry",
        "limit.api.mute_emails_on_email_limit_reached"
	],
	"hourly": [
        "limit.limits.update_space_usage"
		"limit.limits.update_site_usage"
	]
	# "weekly": [
	# 	"limit.tasks.weekly"
	# ]
	# "monthly": [
	# 	"limit.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "limit.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "limit.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "limit.task.get_dashboard_data"
# }

