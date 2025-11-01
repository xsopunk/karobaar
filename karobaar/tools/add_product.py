from langchain_core.tools import tool
from core.odoo_client import call_odoo
from tools.find_products import find_products

@tool
def add_product(
    name: str,
    list_price: float,
    standard_price: float,
    quantity: float = 0.0,
    product_type: str = "consu"
):
    """
    Creates a new product in Odoo and optionally sets its opening stock quantity.

    Use this tool to quickly add new items to your inventory without manually updating stock.

    Args:
        name: The display name of the new product (e.g., "Plastic Chair").
        list_price: The selling price of the product (e.g., 120.0).
        standard_price: The cost or purchase price of the product (e.g., 60.0).
        quantity: The initial stock quantity to set after creation (e.g., 50).
        product_type: The product category type. Must be one of ['consu', 'service', 'product'].
                      Defaults to 'consu' (Consumable).
    """

    existing = find_products(field_name="name", operator="=", value=name)
    if isinstance(existing, list) and len(existing) > 0:
        return {"status": "exists", "product": existing[0]}

    vals = {
        "name": name,
        "list_price": list_price,
        "standard_price": standard_price,
        "type": product_type,
        "uom_id": 1,
    }

    # 1️⃣ Create the product template
    res = call_odoo("product.template", "create", {"vals_list": [vals]})
    if "error" in res: return res
    tmpl_id = res[0]

    # 2️⃣ Get the product variant
    variant = call_odoo("product.product", "search_read", {
        "domain": [["product_tmpl_id", "=", tmpl_id]],
        "fields": ["id", "name"]
    })
    if not variant: return {"error": "variant_not_found"}
    product_id = variant[0]["id"]

    # 3️⃣ Update stock quantity (only if quantity > 0)
    if quantity > 0:
        qty_vals = {"product_id": product_id, "new_quantity": quantity}
        stock_res = call_odoo("stock.change.product.qty", "create", {"vals_list": [qty_vals]})
        if isinstance(stock_res, list) and stock_res:
            call_odoo("stock.change.product.qty", "change_product_qty", {"ids": stock_res})
        else:
            print("⚠️ Could not update stock quantity")

    return {"status": "created", "product": variant[0], "quantity_set": quantity}
