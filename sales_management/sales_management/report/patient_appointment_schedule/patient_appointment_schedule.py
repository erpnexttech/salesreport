# Copyright (c) 2022, Sales and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data, dictPractitioner = [], [], []
    # Get list of practitioners sothat we can make the dynamic column
    
    cs_data, dictPractitioner = get_data(filters)
    
    columns = get_columns(dictPractitioner)
    # Get the entire data from practitioner schedule table

    # Using the data read from table create our own row data sothat it matches with the dynamic column
    client_dict = {}
    for d in cs_data:
        """row = {}        
        row['time'] = d.appointment_time
        row['date'] = d.appointment_date
        row[d.practitioner_name.lower().replace(' ','')] = d.patient_name"""

        if (d.appointment_date,d.appointment_time) in client_dict:
            client_dict[(d.appointment_date,d.appointment_time)].update({d.practitioner_name.lower().replace(' ',''):d.patient_name})
        else:
            client_dict[(d.appointment_date,d.appointment_time)] = {'date':d.appointment_date,'time':d.appointment_time,d.practitioner_name.lower().replace(' ',''):d.patient_name}


    return columns, list(client_dict.values())


def get_columns(dictPractitioner):
    x = []
    row = {}
    row['fieldname'] = 'date'
    row['fieldtype'] = _('Date')
    row['label'] = 'Date'
    row['width'] = '120'
    x.append(row)

    row = {}
    row['fieldname'] = 'time'
    row['fieldtype'] = _('Data')
    row['label'] = 'Time'
    row['width'] = '120'
    x.append(row)
    for d in dictPractitioner:
        row = {}
        row['fieldname'] = d.lower().replace(' ','')
        row['fieldtype'] = _('Data')
        row['label'] = d
        row['width'] = '120'
        x.append(row)
    return x


def get_data(filters):
    conditions = ' where company="%s" and appointment_date between "%s" and "%s"'%(filters.company,filters.from_date,filters.to_date)
    if filters.practitioner:
        conditions += ' and practitioner = "%s"'%filters.practitioner

    
    data = frappe.db.sql("""select appointment_date, appointment_time,
                patient_name, practitioner, practitioner_name
                from `tabPatient Appointment` %s"""%conditions,as_dict=1)

    dictPractitioner = []
    for practitioner in data:
        if practitioner.practitioner_name not in dictPractitioner:
            dictPractitioner.append(practitioner.practitioner_name)

    return data, dictPractitioner




