// Copyright (c) 2022, Sales and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Patient Appointment Schedule"] = {
	"filters": [
	 {
                "fieldname": "company",
                "fieldtype": "Link",
                "label": "Company",
		 "options":"Company",
		 "reqd":1,
		 "default": frappe.defaults.get_user_default("Company")
          }, 	
	 {
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "Date",
		 "reqd":1,
		 "default": frappe.datetime.get_today(),

  	  },
	   {
                "fieldname": "practitioner",
                "fieldtype": "Link",
                "label": "Practitioner",
		"options":"Healthcare Practitioner",
		   
          }

	
	],
	onload: function(report) {
		report.page.add_inner_button(__("Create Appointment"), function() {
			frappe.set_route('Form', "Patient Appointment",'new-patient-appointment-1')
		});
	}
};
