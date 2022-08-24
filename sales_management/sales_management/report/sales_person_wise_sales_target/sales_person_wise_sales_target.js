// Copyright (c) 2022, Sales and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Wise Sales Target"] = {
	"filters": [
		{
                        "fieldname":"company",
                        "label": __("Company"),
                        "fieldtype": "Link",
                        "options": "Company",
                        "default": frappe.defaults.get_user_default("Company")
                },
		{
		        "fieldname":"sales_person",
                        "label": __("Sales Person"),
                        "fieldtype": "Link",
			"options": "Sales Person"
                },

	],
	"tree": true,
	"parent_field": "parent_sales_person",
	"name_field": "sales_person",
	"initial_depth": 2,
	"formatter":function (value, row, column, data, default_formatter)  {
 	   	value = default_formatter(value, row, column, data);
		
		if (data.name == 'Total') {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	}
}

