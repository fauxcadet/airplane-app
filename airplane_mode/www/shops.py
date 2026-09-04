import frappe


def get_context(context):
	context.no_cache = 1
	context.shops = frappe.get_all(
		"Shop",
		filters={"status": "Available"},
		fields=[
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
		order_by="airport, shop_number",
	)
