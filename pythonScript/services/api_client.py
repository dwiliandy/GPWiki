import requests
from config import API_BASE_URL

def get(endpoint, params=None):
    return requests.get(f"{API_BASE_URL}/{endpoint}", params=params)

def post(endpoint, data=None):
    return requests.post(f"{API_BASE_URL}/{endpoint}", data=data)
