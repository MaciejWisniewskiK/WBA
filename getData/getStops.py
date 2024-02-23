import pandas as pd
import requests
import sys

URL = "https://api.um.warszawa.pl/api/action/dbstore_get"
RESOURCE_ID = "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3"
APIKEY = 'fd3159c7-45e3-4cf1-9431-bd0c263d38e0'

query_params = {
    "id" : RESOURCE_ID,
    "apikey": APIKEY,
}

def makeAList(data):
    return list(dict((elem["key"], elem["value"]) for elem in sublist["values"]) for sublist in data)

def get_Stops(dest_file):
    r = requests.get(url=URL, params=query_params)
    response = r.json()["result"]

    if r.status_code != requests.codes.ok or r.json().get("error") or r.json()["result"] == "Błędna metoda lub parametry wywołania":
        print("Błąd przy pobieraniu danych o przystankach.")
        exit(0)

    df = pd.DataFrame(makeAList(response))
    try:
        df.to_json(dest_file)
    except:
        raise Exception("Błąd przy zapisywaniu do pliku.")
