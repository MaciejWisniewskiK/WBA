import requests

# API request constants
URL = 'https://api.um.warszawa.pl/api/action/busestrams_get'
RESOURCE_ID = "f2e5503e-927d-4ad3-9500-4ab9e55deb59"
APIKEY = 'fd3159c7-45e3-4cf1-9431-bd0c263d38e0'
TYPE = "1"

query_params = {
    "resource_id": RESOURCE_ID,
    "apikey": APIKEY,
    "type" : TYPE,
    "line" : "709",
}

r = requests.get(url=URL, params=query_params)

print(r.json())
