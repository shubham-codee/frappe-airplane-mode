# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ShopLease(Document):
	def before_save(self):
		shop = frappe.get_doc("Shop", self.shop)
		shop.status = "occupied"
		shop.save()
  
		if not self.monthly_rent:
			self.monthly_rent = frappe.db.get_single_value("Rent Settings", "default_rent")