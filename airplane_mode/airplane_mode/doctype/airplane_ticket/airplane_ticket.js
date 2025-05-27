// Copyright (c) 2025, Shubh and contributors
// For license information, please see license.txt

function get_seat_through_prompt(frm) {
	frappe.prompt(
		"Seat Number",
		async (val) => {
			let occupied_seats = await frappe.db.get_list("Airplane Ticket", {
				filters: {
					flight: frm.doc.flight,
				},
				fields: ["seat"],
				pluck: "seat",
			});
			if (!occupied_seats.includes(val.value)) {
				frm.set_value("seat", val.value);
			} else {
				frappe.msgprint("seat already occupied");
				get_seat_through_prompt(frm);
			}
		},
		"Select Seat",
		"Assign"
	);
}

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			"Assign Seat",
			() => {
				get_seat_through_prompt(frm);
			},
			"Actions"
		);
	},
	update_total_amount(frm) {
		let total_amount = 0;
		for (add_on of frm.doc.add_ons) {
			total_amount += add_on.amount;
		}
		frm.set_value("total_amount", total_amount + frm.doc.flight_price);
	},
});

frappe.ui.form.on("Airplane Ticket Add-on Item", {
	amount(frm, cdt, cdn) {
		frm.trigger("update_total_amount");
	},
	item(frm, cdt, cdn) {
		all_add_ons = frm.doc.add_ons;
		prev_items = all_add_ons.map((add_on) => add_on["item"]);
		curr_item = prev_items.pop();
		if (prev_items.includes(curr_item)) {
			frappe.msgprint("item already added to add ons. please select other items");
			all_add_ons[prev_items.length].item = "";
		}
	},
});
