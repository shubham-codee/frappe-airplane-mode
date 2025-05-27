# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airport(Document):
	def before_save(self):
		if not len(self.gates) >= 1:
			frappe.throw("add atleast one gate")