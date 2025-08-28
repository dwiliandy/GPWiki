from .api_client import get, post

def get_crews(params=None):
    res = get("crews", params)
    if res.status_code == 200:
        return res.json().get("data", [])
    return []

def get_crew_detail(crew_id):
    res = get(f"crews/{crew_id}")
    if res.status_code == 200:
        return res.json().get("data")
    return None

def store_crews(raw_text):
    res = post("crews", {"raw_text": raw_text})
    return res
