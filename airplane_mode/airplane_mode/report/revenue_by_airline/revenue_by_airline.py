import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 220,
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 160,
        },
    ]

    airlines = frappe.get_all(
        "Airline",
        fields=["name"],
        order_by="name asc",
    )

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"docstatus": 1},
        fields=["flight", "total_amount"],
    )

    flight_names = list({ticket.flight for ticket in tickets if ticket.flight})

    flight_to_airplane = {}
    if flight_names:
        flight_rows = frappe.get_all(
            "Airplane Flight",
            filters={"name": ["in", flight_names]},
            fields=["name", "airplane"],
        )
        flight_to_airplane = {
            flight.name: flight.airplane for flight in flight_rows
        }

    airplane_names = list(
        {
            airplane_name
            for airplane_name in flight_to_airplane.values()
            if airplane_name
        }
    )

    airplane_to_airline = {}
    if airplane_names:
        airplane_rows = frappe.get_all(
            "Airplane",
            filters={"name": ["in", airplane_names]},
            fields=["name", "airline"],
        )
        airplane_to_airline = {
            airplane.name: airplane.airline for airplane in airplane_rows
        }

    revenue_by_airline = {}

    for ticket in tickets:
        airplane = flight_to_airplane.get(ticket.flight)
        airline = airplane_to_airline.get(airplane)

        if airline:
            revenue_by_airline[airline] = (
                revenue_by_airline.get(airline, 0)
                + (ticket.total_amount or 0)
            )

    data = []
    total_revenue = 0

    for airline_doc in airlines:
        revenue = revenue_by_airline.get(airline_doc.name, 0)

        data.append(
            {
                "airline": airline_doc.name,
                "revenue": revenue,
            }
        )
        total_revenue += revenue

    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [
                {
                    "name": "Revenue",
                    "values": [row["revenue"] for row in data],
                }
            ],
        },
        "type": "donut",
        "height": 300,
    }

    summary = [
        {
            "value": total_revenue,
            "label": "Total Revenue",
            "datatype": "Currency",
            "indicator": "Green",
        }
    ]

    return columns, data, None, chart, summary