import requests, json
from config.settings import BASE_URL, HEADERS

def call_odoo(model, method, params=None):
    if params is None:
        params = {}
    url = f"{BASE_URL}/{model}/{method}"
    payload = {"ids": [], "context": {}}
    payload.update(params)

    try:
        res = requests.post(url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
