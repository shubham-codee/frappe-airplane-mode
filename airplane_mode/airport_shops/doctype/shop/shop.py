# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Shop(Document):
    def before_save(self):
        if not self.is_published:
            self.route = ""
        else:
            if not self.route:
                self.route = f"shops/{self.name}"