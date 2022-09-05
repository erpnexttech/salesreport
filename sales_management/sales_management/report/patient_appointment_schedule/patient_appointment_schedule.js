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
		"label": "From Date",
		 "reqd":1,
		 "default": frappe.datetime.get_today(),

  	  },
	 {
                "fieldname": "to_date",
                "fieldtype": "Date",
                "label": "To Date",
		 "reqd":1,
		 "default": frappe.datetime.get_today(),
          },
	   {
                "fieldname": "practitioner",
                "fieldtype": "Link",
                "label": "Practitioner",
		"options":"Healthcare Practitioner",
		   
          }

	
	]
};
