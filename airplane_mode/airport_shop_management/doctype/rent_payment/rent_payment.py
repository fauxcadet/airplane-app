# Copyright (c) 2026, sourav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class RentPayment(Document):
	def validate(self):
		contract = frappe.get_doc("Shop Contract", self.shop_contract)
		self.shop = contract.shop
		self.tenant = contract.tenant	

		existing_payment = frappe.db.exists(
			"Rent Payment",
			{
				"shop_contract": self.shop_contract,
				"payment_month": getdate(self.payment_month),
				"docstatus": 1,
				"name": ["!=", self.name],
			},
		)
		if existing_payment:
			frappe.throw(
				f"A rent payment for this contract and month already exists: {existing_payment}"
			)
