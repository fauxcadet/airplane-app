import frappe
from frappe.utils import getdate, nowdate

def sync_ticket_gate_numbers(flight_name: str, gate_number: str | None):
    """Copy a flight's gate to its active tickets in a background worker."""
    ticket_names = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight_name, "docstatus": ["!=", 2]},
        pluck="name",
    )

    for ticket_name in ticket_names:
        frappe.db.set_value(
            "Airplane Ticket",
            ticket_name,
            "custom_gate_number",
            gate_number,
            update_modified=False,
    )
def update_airport_shop_counts(airport_name: str):
    total = frappe.db.count("Shop", {"airport": airport_name})
    available = frappe.db.count(
        "Shop", {"airport": airport_name, "status": "Available"}
    )
    occupied = frappe.db.count(
        "Shop", {"airport": airport_name, "status": "Occupied"}
    )

    frappe.db.set_value(
        "Airport",
        airport_name,
        {
            "custom_total_shops": total,
            "custom_available_shops": available,
            "custom_occupied_shops": occupied,
        },
    )


def send_monthly_rent_reminders():
    settings = frappe.get_single("Airport Shop Settings")
    if not settings.enable_rent_reminders:
        return

    today = getdate(nowdate())
    contracts = frappe.get_all(
        "Shop Contract",
        filters={"docstatus": 1, "status": "Active"},
        fields=["name", "shop", "tenant", "monthly_rent", "end_date"],
    )

    for contract in contracts:
        if contract.end_date and getdate(contract.end_date) < today:
            continue

        email = frappe.db.get_value("Tenant", contract.tenant, "email")
        if not email:
            continue

        frappe.sendmail(
            recipients=[email],
            subject="Monthly rent reminder",
            message=(
                f"Rent of {contract.monthly_rent} is due for shop {contract.shop}."
            ),
        )
