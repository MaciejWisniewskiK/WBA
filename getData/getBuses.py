import requests
from datetime import datetime, timedelta
from time import sleep
import pandas as pd

# API request constants
URL = 'https://api.um.warszawa.pl/api/action/busestrams_get'
RESOURCE_ID = "f2e5503e-927d-4ad3-9500-4ab9e55deb59"
APIKEY = 'fd3159c7-45e3-4cf1-9431-bd0c263d38e0'
TYPE = "1"

query_params = {
    "resource_id": RESOURCE_ID,
    "apikey": APIKEY,
    "type" : TYPE,
}

class Row:
    def __init__(self, lon, lat, line, time, nr):
        self.lon = lon
        self.lat = lat
        self.line = line
        self.time = time
        self.nr = nr

def getBuses(run_time, dest_file):
    end = datetime.now() + timedelta(minutes=run_time)

    data = set()
    while True:
        print("I'm still working...")

        r = requests.get(url=URL, params=query_params)

        while r.status_code != requests.codes.ok or r.json().get("error") or r.json()["result"] == "Błędna metoda lub parametry wywołania":
            r = requests.get(url=URL, params=query_params)
        
        response = r.json()["result"]

        for item in response:
            row = Row(item["Lon"], item["Lat"], item["Lines"], item["Time"], item["VehicleNumber"])
            if not row in data:
                data.add(row)

        if datetime.now() + timedelta(seconds=30) > end:
            break
        sleep(30)

    df = pd.DataFrame(list(data))
    try:
        df.to_json(dest_file)
    except:
        raise Exception("Błąd przy zapisywaniu do pliku.")


