# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt

# import frappe
from unicodedata import name

from frappe.website.website_generator import WebsiteGenerator
# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt
# Copyright (c) 2026, sourav and contributors
# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class AirplaneFlight(Document):
    website = frappe._dict(
        condition_field="is_published",
        page_title_field="name",
        template="airplane_mode/doctype/airplane_flight/templates/airplane_flight.html",
    )

    def before_insert(self):
        month_year = frappe.utils.now_datetime().strftime("%m-%Y")
        self.name = make_autoname(f"{self.airplane}-{month_year}-.#####")
        self.set_route()

    def on_submit(self):
        self.status = "Completed"

    def get_page_info(self):
        return {
            "title": self.name,
            "route": self.route,
        }

    def set_route(self):
        if self.route:
            return

        airplane = frappe.get_doc("Airplane", self.airplane)

        airline = frappe.scrub(airplane.airline or self.airplane)
        source = frappe.scrub(self.source_airport_code)
        destination = frappe.scrub(self.destination_airport_code)
        date = frappe.utils.formatdate(self.date_of_departure, "yyyy-mm-dd")

        base_route = f"{airline}-{source}-{destination}-{date}"

        self.route = make_autoname(f"{base_route}-.#####")
    def on_update(self):
        if not self.has_value_changed("custom_gate_number"):
            return

        frappe.enqueue(
            "airplane_mode.tasks.sync_ticket_gate_numbers",
            queue="default",
            enqueue_after_commit=True,
            flight_name=self.name,
            gate_number=self.custom_gate_number,
        )
