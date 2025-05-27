# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):
	def add_seat(self):
		all_seats = frappe.get_all("Seat",pluck="seat_no")
		occupied_seats = frappe.get_all("Airplane Ticket",filters={'flight':self.flight},pluck="seat")

		for seat in all_seats:
			if seat not in occupied_seats:
				self.seat = seat
				break

	def validate(self):
		unique_items = []
		present_add_ons = []
		i = 1
		for add_on in self.add_ons:
			if add_on.item not in unique_items:
				add_on.idx = i
				i += 1
				present_add_ons.append(add_on)
				unique_items.append(add_on.item)

		self.add_ons = present_add_ons
  
	def before_insert(self):
		total_tickets_of_flight = frappe.db.count("Airplane Ticket", {"flight" : self.flight})
		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight.airplane)
		total_capacity_of_airplane = airplane.capacity
  
		if total_tickets_of_flight + 1 > total_capacity_of_airplane:
			frappe.throw("Sorry, this flight is fully booked. No more tickets can be issued.")
		
		if not self.seat:
			self.add_seat()
       
	def before_save(self):
		total_add_ons_amount = 0
		for add_on in self.add_ons:
			total_add_ons_amount += add_on.amount
		
		self.total_amount = total_add_ons_amount + int(self.flight_price)
  
	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Ticket cannot be submitted unless the passenger has boarded.")