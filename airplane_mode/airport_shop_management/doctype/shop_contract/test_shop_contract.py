import frappe
from frappe.tests.utils import FrappeTestCase


class TestShopContract(FrappeTestCase):
    def setUp(self):
        suffix = frappe.generate_hash(length=8)
        self.airport = frappe.get_doc(
            {
                "doctype": "Airport",
                "name": f"TEST-AIRPORT-{suffix}",
                "code": f"T{suffix[:2].upper()}",
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
        self.tenant = self.make_tenant(suffix)
        self.shop = self.make_shop(suffix)

    def make_tenant(self, suffix):
        return frappe.get_doc(
            {
                "doctype": "Tenant",
                "tenant_name": f"Test Tenant {suffix}",
                "email": f"tenant-{suffix}@example.com",
                "active": 1,
            }
        ).insert(ignore_permissions=True)

    def make_shop(self, suffix):
        return frappe.get_doc(
            {
                "doctype": "Shop",
                "shop_number": f"S-{suffix}",
                "shop_name": "Test Shop",
                "airport": self.airport.name,
                "shop_type": self.shop_type.name,
                "area_sq_ft": 100,
                "status": "Available",
                "monthly_rent": 1000,
            }
        ).insert(ignore_permissions=True)

    def make_contract(self, start_date="2026-01-01", end_date="2026-12-31", shop=None):
        return frappe.get_doc(
            {
                "doctype": "Shop Contract",
                "shop": shop or self.shop.name,
                "tenant": self.tenant.name,
                "start_date": start_date,
                "end_date": end_date,
                "monthly_rent": 1000,
            }
        )

    def test_rejects_end_date_before_start_date(self):
        contract = self.make_contract("2026-12-31", "2026-01-01")
        self.assertRaises(frappe.ValidationError, contract.insert)

    def test_rejects_end_date_equal_to_start_date(self):
        contract = self.make_contract("2026-01-01", "2026-01-01")
        self.assertRaises(frappe.ValidationError, contract.insert)

    def test_allows_valid_date_range(self):
        contract = self.make_contract()
        contract.insert(ignore_permissions=True)
        self.assertEqual(contract.docstatus, 0)

    def test_submit_marks_contract_active(self):
        contract = self.make_contract()
        contract.insert(ignore_permissions=True)
        contract.submit()
        self.assertEqual(contract.status, "Active")

    def test_submit_marks_shop_occupied(self):
        contract = self.make_contract()
        contract.insert(ignore_permissions=True)
        contract.submit()
        self.assertEqual(frappe.get_doc("Shop", self.shop.name).status, "Occupied")

    def test_submit_sets_shop_current_tenant(self):
        contract = self.make_contract()
        contract.insert(ignore_permissions=True)
        contract.submit()
        shop = frappe.get_doc("Shop", self.shop.name)
        self.assertEqual(shop.current_tenant, self.tenant.name)

    def test_cancel_releases_shop_without_other_active_contract(self):
        contract = self.make_contract()
        contract.insert(ignore_permissions=True)
        contract.submit()
        contract.cancel()
        shop = frappe.get_doc("Shop", self.shop.name)
        self.assertEqual(shop.status, "Available")
        self.assertFalse(shop.current_tenant)
