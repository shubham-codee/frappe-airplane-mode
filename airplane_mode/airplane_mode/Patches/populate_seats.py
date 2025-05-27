import frappe

def execute():
    airplane_tickets = frappe.db.get_all("Airplane Ticket", pluck = "name")
    
    for airplane_ticket_name in airplane_tickets:
        airplane_ticket = frappe.get_doc("Airplane Ticket", airplane_ticket_name)
        airplane_ticket.add_seat()
        airplane_ticket.save()
        
    frappe.db.commit()    