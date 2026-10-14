from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import json

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
country_data_list = session.get("https://countries.dev/countries?fields=name%2Ccapital%2Cflag&full=true&sort=population&limit=100&offset=0").json()

data_to_load = []
accepted_rows = 0
rejected_rows = 0
for i in range(len(country_data_list)):
    if "area" not in country_data_list[i]:
        rejected_rows += 1
        continue

    country_data = {
        "area": country_data_list[i]["area"],
        "alpha2Code": country_data_list[i]["alpha2Code"],
        "name": country_data_list[i]["name"],
        "latitude": country_data_list[i]["latlng"][0],
        "longitude": country_data_list[i]["latlng"][1],
        "region": country_data_list[i]["region"],
        "timezones": country_data_list[i]["timezones"],
        "population": country_data_list[i]["population"],
        "populationDensity": country_data_list[i]["populationDensity"]

    }
    data_to_load.append(country_data)
    accepted_rows += 1

with open("data_to_load.json", "w") as file:
    json.dump(data_to_load, file, indent=4)
print(accepted_rows, rejected_rows)

