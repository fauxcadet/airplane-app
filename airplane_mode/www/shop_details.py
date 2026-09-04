import frappe


def get_context(context):
	context.no_cache = 1
	shop_name = frappe.form_dict.get("name")
	if not shop_name:
		frappe.throw("Shop is required.")

	shop = frappe.db.get_value(
		"Shop",
		{"name": shop_name, "status": "Available"},
		[
			"name",
			"shop_number",
			"shop_name",
			"airport",
			"shop_type",
			"area_sq_ft",
			"monthly_rent",
			"description",
			"image",
		],
		as_dict=True,
	)
	if not shop:
		frappe.throw("This shop is not available for leasing.", frappe.DoesNotExistError)

	context.shop = shop
