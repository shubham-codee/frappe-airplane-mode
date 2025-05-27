// Copyright (c) 2025, Shubh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	source_airport(frm) {
		if (frm.doc.source_airport) {
			frappe.db.get_doc("Airport", frm.doc.source_airport).then((current_source_airport) => {
				let gate_numbers = current_source_airport.gates
					.map((gate) => gate.gate_number)
					.join(", ");

				frm.set_df_property(
					"entry_gate_number",
					"description",
					"Available Gates: " + gate_numbers
				);
			});
		}
	},

	destination_airport(frm) {
		if (frm.doc.destination_airport) {
			frappe.db
				.get_doc("Airport", frm.doc.destination_airport)
				.then((current_destination_airport) => {
					let gate_numbers = current_destination_airport.gates
						.map((gate) => gate.gate_number)
						.join(", ");

					frm.set_df_property(
						"exit_gate_number",
						"description",
						"Available Gates: " + gate_numbers
					);
				});
		}
	},
});

frappe.ui.form.on("Flight Crew Members", {
	full_name(frm, cdt, cdn) {
		all_curr_staff = frm.doc.flight_crew_members;
		prev_staff = all_curr_staff.map((staff) => staff["full_name"]);
		curr_staff = prev_staff.pop();
		if (prev_staff.includes(curr_staff)) {
			frappe.msgprint("crew member already added");
			all_curr_staff[prev_staff.length].full_name = "";
			all_curr_staff[prev_staff.length].designation = "";
		}
	},
});
