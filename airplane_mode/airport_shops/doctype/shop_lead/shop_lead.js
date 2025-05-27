// Copyright (c) 2025, Shubh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Lead", {
	refresh(frm) {
		frm.set_query("shop", function () {
			return {
				filters: {
					airport: frm.doc.airport,
					status: "vacant",
				},
			};
		});
	},
});
