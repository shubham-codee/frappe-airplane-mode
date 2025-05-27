import frappe

def get_context(context):
    shop_name_in_url = frappe.request.path.split('/')[-1]

    shop = frappe.get_doc("Shop", shop_name_in_url)
    context.shop_name = shop.name
    context.airport = shop.airport
    context.area = shop.area
    context.location = shop.location
    context.status = shop.status
    