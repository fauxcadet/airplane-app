# Copyright (c) 2026, sourav and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestShop(FrappeTestCase):
	def setUp(self):
		suffix = frappe.generate_hash(length=8)
		self.airport = frappe.get_doc(
			{
				"doctype": "Airport",
				"name": f"TEST-SHOP-AIRPORT-{suffix}",
				"code": f"S{suffix[:2].upper()}",
				"city": "Test City",
				"country": "India",
			}
		).insert(ignore_permissions=True)
		self.shop_type = frappe.get_doc(
			{
				"doctype": "Shop Type",
				"name": f"TEST-SHOP-TYPE-{suffix}",
				"enabled": 1,
			}
		).insert(ignore_permissions=True)
		self.suffix = suffix

	def make_shop(self, **overrides):
		values = {
			"doctype": "Shop",
			"shop_number": f"S-{self.suffix}-{frappe.generate_hash(length=4)}",
			"shop_name": "Test Shop",
			"airport": self.airport.name,
			"shop_type": self.shop_type.name,
			"area_sq_ft": 100,
			"status": "Available",
		}
		values.update(overrides)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_uses_default_monthly_rent_from_settings(self):
		frappe.db.set_single_value("Airport Shop Settings", "default_monthly_rent", 1250)
		shop = self.make_shop()
		self.assertEqual(shop.monthly_rent, 1250)

	def test_preserves_entered_monthly_rent(self):
		frappe.db.set_single_value("Airport Shop Settings", "default_monthly_rent", 1250)
		shop = self.make_shop(monthly_rent=900)
		self.assertEqual(shop.monthly_rent, 900)

	def test_updates_airport_shop_counts(self):
		self.make_shop(status="Available", monthly_rent=1000)
		self.make_shop(status="Occupied", monthly_rent=2000)
		counts = frappe.db.get_value(
			"Airport",
			self.airport.name,
			["custom_total_shops", "custom_available_shops", "custom_occupied_shops"],
			as_dict=True,
		)
		self.assertEqual(int(counts.custom_total_shops), 2)
		self.assertEqual(int(counts.custom_available_shops), 1)
		self.assertEqual(int(counts.custom_occupied_shops), 1)
