import random

import frappe


def execute():
    """Populate seats for existing tickets without overwriting assigned seats."""
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"seat": ["in", ["", None]]},
        pluck="name",
    )

    for ticket_name in tickets:
        seat = f"{random.randint(1, 99)}{random.choice(['A', 'B', 'C', 'D', 'E'])}"
        frappe.db.set_value("Airplane Ticket", ticket_name, "seat", seat)
