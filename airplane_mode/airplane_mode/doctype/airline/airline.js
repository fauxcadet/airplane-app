frappe.ui.form.on("Airline", {
    refresh(frm) {
        if (!frm.doc.website) {
            return;
        }

        frm.add_custom_button(__("Visit Website"), () => {
            window.open(frm.doc.website, "_blank");
        });
    }
});