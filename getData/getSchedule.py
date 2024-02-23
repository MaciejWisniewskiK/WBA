import requests
from datetime import datetime

URL = "https://api.um.warszawa.pl/api/action/dbtimetable_get"
RESOURCE_ID = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"
APIKEY = 'fd3159c7-45e3-4cf1-9431-bd0c263d38e0'

def makeAList(data):
    ret_list = []
    for sublist in data:
        for elem in sublist["values"]:
            if (elem["key"] == "czas"):
                try:
                    ret_list.append(datetime.strptime(elem["value"], "%H:%M:%S"))
                except:
                    continue
    return ret_list

def getSchedule(line, stop_zesp, stop_slup):
    query_params = {
        "id" : RESOURCE_ID,
        "apikey": APIKEY,
        "busstopId": stop_zesp,
        "busstopNr": stop_slup,
        "line": line
    }

    r = requests.get(url=URL, params=query_params)
    response = r.json()["result"]

    if r.status_code != requests.codes.ok or r.json().get("error") or r.json()["result"] == "Błędna metoda lub parametry wywołania":
        print("Błąd przy pobieraniu danych o rozkładzie.")
        exit(0)

    time_list = makeAList(response)

    return time_list

# Jagielska
#getSchedule("709", "3021", "01")