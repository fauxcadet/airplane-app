import frappe
from frappe.tests.utils import FrappeTestCase


class TestRentPayment(FrappeTestCase):
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
        self.tenant = frappe.get_doc(
            {
                "doctype": "Tenant",
                "tenant_name": f"Test Tenant {suffix}",
                "email": f"tenant-{suffix}@example.com",
                "active": 1,
            }
        ).insert(ignore_permissions=True)
        self.shop = frappe.get_doc(
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
        self.contract = frappe.get_doc(
            {
                "doctype": "Shop Contract",
                "shop": self.shop.name,
                "tenant": self.tenant.name,
                "start_date": "2026-01-01",
                "end_date": "2026-12-31",
                "monthly_rent": 1000,
            }
        ).insert(ignore_permissions=True)
        self.contract.submit()

    def make_payment(self, payment_month="2026-09-01"):
        return frappe.get_doc(
            {
                "doctype": "Rent Payment",
                "shop_contract": self.contract.name,
                "payment_month": payment_month,
                "amount": 1000,
                "payment_date": payment_month,
                "status": "Done",
            }
        )

    def test_populates_shop_from_contract(self):
        payment = self.make_payment()
        payment.insert(ignore_permissions=True)
        self.assertEqual(payment.shop, self.shop.name)

    def test_populates_tenant_from_contract(self):
        payment = self.make_payment()
        payment.insert(ignore_permissions=True)
        self.assertEqual(payment.tenant, self.tenant.name)

    def test_allows_first_payment_for_a_month(self):
        payment = self.make_payment()
        payment.insert(ignore_permissions=True)
        payment.submit()
        self.assertEqual(payment.docstatus, 1)

    def test_rejects_duplicate_submitted_payment_for_same_month(self):
        first_payment = self.make_payment()
        first_payment.insert(ignore_permissions=True)
        first_payment.submit()

        duplicate_payment = self.make_payment()
        self.assertRaises(frappe.ValidationError, duplicate_payment.insert)

    def test_allows_payment_for_a_different_month(self):
        first_payment = self.make_payment("2026-09-01")
        first_payment.insert(ignore_permissions=True)
        first_payment.submit()

        october_payment = self.make_payment("2026-10-01")
        october_payment.insert(ignore_permissions=True)
        self.assertEqual(october_payment.payment_month, "2026-10-01")

    def test_cancelled_payment_does_not_block_replacement(self):
        payment = self.make_payment()
        payment.insert(ignore_permissions=True)
        payment.submit()
        payment.cancel()

        replacement = self.make_payment()
        replacement.insert(ignore_permissions=True)
        self.assertEqual(replacement.docstatus, 0)
