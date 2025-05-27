# Copyright (c) 2025, Shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
import random


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		all_tickets = frappe.get_all("Airplane Ticket",filters={'flight':self.name})
		for ticket in all_tickets:
			current = frappe.get_doc("Airplane Ticket",ticket.name)
			if current.status == "Boarded":
				current.submit()
		self.status = "Completed"
  
  
		for staff in self.flight_crew_members:
			curr = frappe.get_doc("Staff", staff.full_name)
			curr.status = "Free"
			curr.save()		
  
	def before_save(self):
		unique_staff = []
		present_staff = []
		i = 1
		for staff in self.flight_crew_members:
			if staff.full_name not in unique_staff:
				staff.idx = i
				i += 1
				present_staff.append(staff)
				unique_staff.append(staff.full_name)

		self.flight_crew_members = present_staff
  
		for staff in self.flight_crew_members:
			curr = frappe.get_doc("Staff", staff.full_name)
			curr.status = "Occupied"
			curr.save()
   
		if not self.entry_gate_number and not self.exit_gate_number:
			source_airport = frappe.get_doc("Airport", self.source_airport)
			destination_airport = frappe.get_doc("Airport", self.destination_airport)
	
			source_airport_gates = source_airport.gates
			destination_airport_gates = destination_airport.gates
	
			source_airport_gate_numbers = [gate.gate_number for gate in source_airport_gates]
			destination_airport_gate_numbers = [gate.gate_number for gate in destination_airport_gates]
	
			random_source_airport_gate_number = random.choice(source_airport_gate_numbers)
			random_destination_airport_gate_number = random.choice(destination_airport_gate_numbers)
	
			self.entry_gate_number = random_source_airport_gate_number
			self.exit_gate_number = random_destination_airport_gate_number
	
	def on_update(self):
		old_self_flight = self.get_doc_before_save()
		if old_self_flight.entry_gate_number != self.entry_gate_number:
			frappe.enqueue("airplane_mode.api.change_entry_gate_number_in_ticket", queue="short", flight=self)
		
		if old_self_flight.exit_gate_number != self.exit_gate_number:
			frappe.enqueue("airplane_mode.api.change_exit_gate_number_in_ticket", queue="short", flight=self)
   
	def validate(self):
		source_airport = frappe.get_doc("Airport", self.source_airport)
		destination_airport = frappe.get_doc("Airport", self.destination_airport)

		source_airport_gates = source_airport.gates
		destination_airport_gates = destination_airport.gates

		source_airport_gate_numbers = [gate.gate_number for gate in source_airport_gates]
		destination_airport_gate_numbers = [gate.gate_number for gate in destination_airport_gates]
  
		if self.entry_gate_number not in source_airport_gate_numbers or self.exit_gate_number not in destination_airport_gate_numbers:
			frappe.throw("Gate does not exist.")