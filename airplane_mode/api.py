import frappe

def send_mail_for_rent_due():
    is_rent_reminder_enabled = frappe.db.get_single_value("Rent Settings", "enable_rent_reminder")
    
    if is_rent_reminder_enabled:
        all_shops_lease = frappe.get_all("Shop Lease")
        recipients = []
        
        for shop_lease in all_shops_lease:
            curr_shop_lease = frappe.get_doc("Shop Lease", shop_lease.name)
            
            if curr_shop_lease.payment_status == "unpaid":
                tenant = frappe.get_doc("Tenant", curr_shop_lease.tenant)
                tenant_email = tenant.email
                recipients.append(tenant_email)
            
        frappe.sendmail(
            recipients=recipients,
            subject=frappe._('Payment Reminder'),
            message= f"""
            ## 📢 Payment Reminder

                Dear {tenant.full_name},

                We hope this message finds you well.

                This is a kind reminder regarding a pending payment associated with your current agreement. We kindly request you to review your account and complete the payment at your earliest convenience to ensure continued smooth service and compliance with the agreed terms.

                If you have already made the payment, please disregard this message.

                Should you require any clarification or assistance regarding the payment process or details, feel free to get in touch with us.

                Thank you for your attention and cooperation.

                Warm regards,  
                **Airplane Mode**  
            """,
            as_markdown=True
        )
        
def change_entry_gate_number_in_ticket(flight):
    all_tickets_of_current_flight = frappe.db.get_all("Airplane Ticket", filters={"flight" : flight.name}, pluck="name")
    
    for ticket in all_tickets_of_current_flight:
        curr_ticket = frappe.get_doc("Airplane Ticket", ticket)
        curr_ticket.entry_gate_number = flight.entry_gate_number
        curr_ticket.save()

def change_exit_gate_number_in_ticket(flight):
    all_tickets_of_current_flight = frappe.db.get_all("Airplane Ticket", filters={"flight" : flight.name}, pluck="name")
    
    for ticket in all_tickets_of_current_flight:
        curr_ticket = frappe.get_doc("Airplane Ticket", ticket)
        curr_ticket.exit_gate_number = flight.exit_gate_number
        curr_ticket.save()
        
@frappe.whitelist(allow_guest=False)
def get_shops():
    try:
        shops = frappe.get_all(
            "Shop",
            fields=["*"],
        )
        
        return {
            "status": "success",
            "data": shops,
            "count": len(shops)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
@frappe.whitelist(allow_guest=False)
def create_new_shop():
    import json
    try:
        data = frappe.form_dict
        if isinstance(data, str):
            data = json.loads(data)

        shop = frappe.get_doc({
            "doctype": "Shop",
            "shop_name": data.get("shop_name"),
            "area": data.get("area"),
            "status": "vacant",
            "type": data.get("type"),
            "airport": data.get("airport"),
            "location": data.get("location"),
            "is_published": data.get("is_published", 1)
        })

        shop.insert()
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Shop created",
            "name": shop.name
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }