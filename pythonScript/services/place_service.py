from .api_client import get, post

def get_places(params=None):
    res = get("places", params)
    if res.status_code == 200:
        return res.json().get("data", [])
    return []

def store_places(raw_text):
    res = post("places", {"raw_text": raw_text})
    return res
