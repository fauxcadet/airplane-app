# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt
import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):

    def validate(self):
        self.remove_duplicate_add_ons()
        self.set_total_amount()

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only Boarded tickets can be submitted")
    def before_insert(self):
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])

        self.seat = f"{seat_number}{seat_letter}"

    def remove_duplicate_add_ons(self):
        unique_items = []
        seen = set()

        for row in self.add_ons:
            if row.item not in seen:
                seen.add(row.item)
                unique_items.append(row)

        self.add_ons = unique_items
    def on_submit(self):
        self.status = "Completed"
    def set_total_amount(self):
        total = self.flight_price or 0

        for addon in self.add_ons:
            total += addon.amount or 0

        self.total_amount = total