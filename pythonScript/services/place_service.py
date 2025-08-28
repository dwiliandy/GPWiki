from .api_client import get

def get_places(params=None):
    res = get("places", params)
    if res.status_code == 200:
        return res.json().get("data", [])
    return []
