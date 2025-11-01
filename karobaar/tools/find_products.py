from langchain_core.tools import tool
from core.odoo_client import call_odoo

@tool
def find_products(field_name: str, operator: str, value: str):
    """
      Searches for Odoo products using a flexible domain (filter).

      Use this to find any product by its name, sku, id, etc.

      Args:
          field_name: The field to search on (e.g., "name", "default_code", "id").
          operator: The comparison operator (e.g., "=", "ilike", ">", "<").
                    Use "ilike" for case-insensitive 'contains' search on names.
          value: The value to search for.
      """

    domain = [[field_name, operator, value]]
    fields = ["id", "name", "default_code", "qty_available", "list_price", "standard_price", "type"]
    params = {"domain": domain, "fields": fields}
    products = call_odoo("product.product", "search_read", params)
    if not products or (isinstance(products, dict) and "error" in products):
        return {"status": "not_found"}
    return products
