# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	def on_submit(self):
		shop_lease = frappe.get_doc("Shop Lease", self.shop_lease)
		shop_lease.payment_status = "paid"
		shop_lease.save()