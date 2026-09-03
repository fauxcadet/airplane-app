// Copyright (c) 2026, sourav and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (frm.is_new()) {
            return;
        }

        frm.add_custom_button(__("Assign Seat"), () => {
            const dialog = new frappe.ui.Dialog({
                title: __("Assign Seat"),
                fields: [
                    {
                        label: __("Seat Number"),
                        fieldname: "seat",
                        fieldtype: "Data",
                        reqd: 1,
                        default: frm.doc.seat || ""
                    }
                ],
                primary_action_label: __("Assign"),
                primary_action(values) {
                    frm.set_value("seat", values.seat);
                    frm.save();
                    dialog.hide();
                }
            });

            dialog.show();
        });
    }
});