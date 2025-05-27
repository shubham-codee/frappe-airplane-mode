// Copyright (c) 2025, Shubh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
		if (frm.doc.is_published) {
			frm.add_web_link(`http://airplane.mode:8000/shops/${frm.doc.name}`, "Visit Website");
		} else {
			frm.web_link.remove();
		}

		frm.set_query("type", function () {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
	},

	is_published(frm) {
		if (frm.doc.is_published) {
			frm.add_web_link(`http://airplane.mode:8000/shops/${frm.doc.name}`, "Visit Website");
			frm.set_value("route", `shops/${frm.doc.name}`);
		} else {
			frm.web_link.remove();
			frm.set_value("route", ``);
		}
	},
});
