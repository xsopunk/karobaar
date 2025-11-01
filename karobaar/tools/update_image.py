import base64, os
from langchain_core.tools import tool
from core.odoo_client import call_odoo

@tool
def update_product_image(product_id: int, image_path: str):
    """
    Updates the image of an existing product in Odoo using a local image file.

    This tool reads the image from your computer, encodes it in Base64, and uploads it
    directly to the specified product record in Odoo.

    Args:
        product_id: The unique ID of the product to update (from 'product.product').
        image_path: The full local file path to the image
                    (e.g., "C:\\images\\chair.png" or "/home/user/pictures/chair.jpg").
    """

    if not os.path.exists(image_path):
        return {"error": "file_not_found"}

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    params = {"ids": [product_id], "vals": {"image_1920": img_b64}}
    result = call_odoo("product.product", "write", params)
    if result is True:
        return {"status": "success", "product_id": product_id}
    return {"status": "failed", "response": result}
