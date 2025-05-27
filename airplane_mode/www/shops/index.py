import frappe


def get_context(context):
    all_shops = frappe.get_all("Shop", pluck="name")
    context["all_shops"] = all_shops
    context.path = frappe.request.path