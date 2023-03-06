// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Set Limit', {
	refresh: function(frm) {
			frm.add_custom_button('Check Set Limits On Usage Info', () => {
				frappe.set_route(["usage-info"])
		})					
	}
});
