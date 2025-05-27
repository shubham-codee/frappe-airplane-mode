// Copyright (c) 2025, Shubh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        let website = frm.doc.website;
        if(website){
            frm.add_web_link(frm.doc.website, "Visit Website");
        }
	},
});
