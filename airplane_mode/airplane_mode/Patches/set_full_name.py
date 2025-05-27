import frappe

def execute():
    passengers = frappe.db.get_all("Flight Passenger", pluck="name")
    
    for passenger_name in passengers:
        passenger = frappe.get_doc("Flight Passenger", passenger_name)
        passenger.set_full_name()
        passenger.save()
        
    frappe.db.commit()