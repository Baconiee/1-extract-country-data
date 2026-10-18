from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import psycopg
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from psycopg.types.json import Jsonb

load_dotenv()

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
response = session.get("https://countries.dev/countries?fields=name%2Ccapital%2Cflag&full=true&sort=population", timeout=10)
response.raise_for_status()
country_data_list = response.json()

extreacted_at = datetime.now(timezone.utc).isoformat()

required_fields = [
    "area",
    "alpha2Code",
    "name",
    "latlng",
    "region",
    "timezones",
    "population",
    "populationDensity",
]

data_to_load = []
accepted_rows = 0
rejected_rows = 0
for country in country_data_list:
    if any(
        field not in country or country[field] is None 
        for field in required_fields
    ):
        rejected_rows += 1
        continue

    latlng = country["latlng"]
    if not isinstance(latlng, list) or len(latlng) != 2:
        rejected_rows += 1
        continue

    country_data = {
        "area": country["area"],
        "alpha2Code": country["alpha2Code"],
        "name": country["name"],
        "latitude": latlng[0],
        "longitude": latlng[1],
        "region": country["region"],
        "timezones": country["timezones"],
        "population": country["population"],
        "population_density": country["populationDensity"],
    }
    data_to_load.append(country_data)
    accepted_rows += 1

with psycopg.connect(
    host=os.environ["POSTGRES_HOST"],
    port=int(os.environ["POSTGRES_POST"]),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"]) as conn:
    print("Connection is successfull")
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO extraction_runs (rows_accepted, rows_rejected, extracted_at)
            VALUES(%s, %s, %s)
            RETURNING id
            """,
            (accepted_rows, rejected_rows, extreacted_at)
        )

        extraction_run_id = cur.fetchone()[0]

        cur.executemany(
            """
            INSERT INTO countries (extraction_run_id, alpha2_code, area, name, latitude, longitude, region, timezones, population, population_density)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    extraction_run_id,
                    country["alpha2Code"],
                    country["area"], 
                    country["name"], 
                    country["latitude"], 
                    country["longitude"], 
                    country["region"], 
                    Jsonb(country["timezones"]),
                    country["population"], 
                    country["population_density"]
                )
                for country in data_to_load
            ]
        )



