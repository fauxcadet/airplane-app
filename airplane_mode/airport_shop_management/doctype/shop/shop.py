# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Shop(Document):
	def before_validate(self):
		if self.monthly_rent:
			return
		self.monthly_rent = frappe.db.get_single_value(
			"Airport Shop Settings", "default_monthly_rent"
		)
	def on_update(self):
		from airplane_mode.tasks import update_airport_shop_counts
		update_airport_shop_counts(self.airport)
