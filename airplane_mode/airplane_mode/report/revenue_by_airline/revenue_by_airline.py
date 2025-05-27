# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"fieldname" : "airline",
			"fieldtype" : "Link",
			"label" : "Airline",
			"options": "Airline",
			"width" : 250
		},
		{
			"fieldname" : "revenue",
			"fieldtype" : "Currency",
			"label" : "Revenue",
			"width" : 250
		}
	]
 
	all_tickets = frappe.get_all("Airplane Ticket", fields=["SUM(flight_price) AS revenue", "flight.airplane"], group_by="flight")
 
	all_airlines = frappe.get_all("Airline", fields=["name"], pluck="name")
 
	present_airlines = []
 
	for ticket in all_tickets:
		airline = frappe.db.get_value("Airplane", ticket.airplane, "airline")
		ticket["airline"] = airline
		present_airlines.append(airline)
  
  
	for airline in all_airlines:
		if airline not in present_airlines:
			new_record = {"revenue" : 0, "airline" : airline}
			all_tickets.append(new_record)
			
	for ticket in all_tickets:
		if "airplane" in ticket:
			del ticket["airplane"]
   
	data = all_tickets
 
	chart = {
		"data" : {
			"labels" : [x[list(x.keys())[1]] for x in data ],
			"datasets" : [
				{
					"values" : [x[list(x.keys())[0]] for x in data]
				}
			]
		},
		"type" : "donut"
	}
 
	total_revenue = sum(x["revenue"] for x in data)
 
	report_summary = [
    	{"label":"Total Revenue","value": frappe.format(total_revenue, {"fieldtype" : "Currency"}),'indicator':'green', "type" : "Currency"},
	]
 
	return columns, data, None, chart, report_summary