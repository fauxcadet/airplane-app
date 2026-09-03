# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class ShopContract(Document):
    def validate(self):
        if getdate(self.end_date) <= getdate(self.start_date):
            frappe.throw("End Date must be after Start Date.")
    def before_submit(self):
        self.status = "Active"

    def on_submit(self):
        shop = frappe.get_doc("Shop", self.shop)
        shop.status = "Occupied"
        shop.current_tenant = self.tenant
        shop.save(ignore_permissions=True)

    def on_cancel(self):
        has_other_active_contract = frappe.db.exists(
            "Shop Contract",
            {
                "shop": self.shop,
                "name": ["!=", self.name],
                "docstatus": 1,
                "status": "Active",
            },
        )

        if has_other_active_contract:
            return

        shop = frappe.get_doc("Shop", self.shop)
        shop.status = "Available"
        shop.current_tenant = None
        shop.save(ignore_permissions=True)
