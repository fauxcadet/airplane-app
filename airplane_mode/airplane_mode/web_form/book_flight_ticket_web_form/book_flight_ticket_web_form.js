frappe.web_form.after_load = () => {
    const flight = frappe.utils.get_url_arg("flight");
    const flightPrice = frappe.utils.get_url_arg("flight_price") || 0;

    if (flight) {
        frappe.web_form.set_value("flight", flight);
    }

    frappe.web_form.set_value("flight_price", flightPrice);
};
