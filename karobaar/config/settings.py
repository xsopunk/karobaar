import os

ODOO_URL = "https://karobaar11.odoo.com"
ODOO_DB = "karobaar11"
ODOO_API_KEY = "407c6f66b4ccbeab6c6cfa3dfb3e07404c41217b"

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDnsVp0h0VPnF90BYMyYC6F55qjWK3OF4M"

BASE_URL = f"{ODOO_URL}/json/2"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"bearer {ODOO_API_KEY}",
    "X-Odoo-Database": ODOO_DB,
    "User-Agent": "langgraph-odoo-agent"
}
