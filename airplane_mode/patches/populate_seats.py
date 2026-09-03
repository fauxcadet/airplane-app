import frappe
import random


def execute():

    tickets = frappe.get_all(
        "Airplane Ticket",
        fields=["name", "seat"]
    )

    print(f"Found {len(tickets)} tickets")

    for ticket in tickets:

        if ticket.seat:
            continue

        seat_number = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])

        seat = f"{seat_number}{seat_letter}"

        frappe.db.set_value(
            "Airplane Ticket",
            ticket.name,
            "seat",
            seat
        )

        print(f"{ticket.name} -> {seat}")

    frappe.db.commit()