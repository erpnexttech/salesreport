# Copyright (c) 2013, Dehaqan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _


def execute(filters=None):
    columns, data = [], []
    sales_persons = get_all_sales_person(filters)
    columns = get_columns()
    order_details = get_data(filters)

    totals = frappe._dict({})
    totals.update({
        "indent": 0.0, "name": 'Total', "parent_sales_person": '',
        "sales_person": 'Total', "opportunity": '', "customer_name": '', "territory": '',
        "opportunity_details": '',  "expected_closing": '',
        "status": '', "contact_by": '', "contact_date": '', "remarks": '',
        "probability": 0, 
    })

    grand_total_sales_amount = 0
    grand_total_oppor_value = 0
    grand_total_sale_opportunity = 0
    grand_total_sales_target = 0
    for sales_person in sales_persons:
        total_order = frappe.db.sql("""select sum(total) as total from `tabSales Order` so 
                                        inner join `tabSales Team` st
                                            on so.name = st.parent
                                        where st.sales_person = '%s' and so.docstatus = 1""" % sales_person.name, as_dict=1)
        
        if total_order:
            total_sale = total_order[0].total
        else:
            total_sale = 0

        total = {
            "indent": 0.0, "is_parent": True,
            'name':'Total',
            "parent_sales_person": "",
            "sales_person": sales_person.name,
            'target': sales_person.target,
            'sales_order_amount': total_sale
        }
        data.append(total)
        total_oppor_value = 0
        total_sale_opportunity = 0
        for ss in order_details:

            if sales_person.name == ss.sales_person:
                temp = frappe._dict({})

                temp.update({
                    "indent": 1.0,  "parent_sales_person": ss.sales_person, "sales_person": '', "opportunity": ss.name, "customer_name": ss.customer_name, "territory": ss.territory, "opportunity_details": ss.opportunity_details, "opportunity_amount": ss.opportunity_amount, "expected_closing": ss.expected_closing, "status": ss.status, "contact_by": ss.contact_by, "contact_date": ss.contact_date, "remarks": '',
                    "probability": 0, "total_sale": 0, "total_sale_opportunity": 0, "target": 0.0,"probability":ss.probability,'name':''
                })
                total_oppor_value = total_oppor_value + ss.opportunity_amount
                
                data.append(temp)
        
        total_sale_opportunity = total_oppor_value + total_sale
        total.update({
            'total_sale':total_oppor_value,
            'total_sale_opportunity':total_sale_opportunity
        })
        grand_total_sales_amount = grand_total_sales_amount + total_sale
        grand_total_oppor_value = grand_total_oppor_value + total_sale_opportunity
        grand_total_sale_opportunity = grand_total_sale_opportunity + total_oppor_value
        grand_total_sales_target = grand_total_sales_target + sales_person.target
    totals.update({
            'total_sale':grand_total_sale_opportunity,
            'total_sale_opportunity':grand_total_oppor_value,
            'sales_order_amount':grand_total_sales_amount,
            'target':grand_total_sales_target
        })
    
    data.append(totals)
    return columns, data


def get_columns():
    columns = [{
        "fieldname": "sales_person",
        "label": "Sales Person",
        "width": 250,
        "fieldtype": "Link",
        "options": "Sales Person"
    }, {
        "fieldname": "target",
        "label": "Target",
        "width": 100,
        "fieldtype": "Currency"
    },
        {
        "fieldname": "sales_order_amount",
        "label": "Sales Order Amount",
        "width": 100,
        "fieldtype": "Currency"
    },
        {
        "fieldname": "customer_name",
        "label": "Client",
        "width": 200,
        "fieldtype": "Data"
    },
        {
        "fieldname": "territory",
        "label": "Location",
        "width": 120,
        "fieldtype": "Data"
    },
        {
        "fieldname": "opportunity_amount",
        "label": "VALUE DHS",
        "width": 150,
        "fieldtype": "Currency"
    },
        {
        "fieldname": "expected_closing",
        "label": "Expected Closing Date",
        "width": 110,
        "fieldtype": "Date"

    },
        {
        "fieldname": "remarks",
        "label": "Remarks",
        "width": 150,
        "fieldtype": "Data"
    },
        {
        "fieldname": "status",
        "label": "Status",
        "width": 140,
        "fieldtype": "Data"
    },
        {
        "fieldname": "contact_by",
        "label": "Next Contact By",
        "width": 140,
        "fieldtype": "Data"
    },
        {
        "fieldname": "contact_date",
        "label": "Next Contact Date",
        "width": 100,
        "fieldtype": "Date"
    },
        {
        "fieldname": "probability",
        "label": "Probability",
        "width": 100,
        "fieldtype": "Percent"
    },
        {
        "fieldname": "total_sale",
        "label": "Total Opportunity Sale",
        "width": 140,
        "fieldtype": "Currency"
    },
        {
        "fieldname": "total_sale_opportunity",
        "label": "Total Sale",
        "width": 140,
        "fieldtype": "Currency"
    }
    ]
    return columns


def get_all_sales_person(filters):
    cond = ''
    if filters.sales_person:
        cond = 'and name="%s"'%(filters.sales_person)

    sales_persons = frappe.db.sql(
        """select name,total_target as target from `tabSales Person` where is_group = 0 %s"""%cond, as_dict=1)
    return sales_persons


def get_data(filters):

    return frappe.db.sql("""select name as opportunity,sales_person,customer_name,territory,opportunity_details,opportunity_amount,expected_closing,status,contact_by,contact_date,probability from `tabOpportunity`""", as_dict=1)
