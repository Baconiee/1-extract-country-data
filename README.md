# Country data

This project extracts country data from [countries.dev](https://countries.dev), validates required fields, and stores accepted rows in PostgreSQL. Each load is recorded in `extraction_runs`; country rows reference that run. PostgreSQL and the Python loader can both run with Docker Compose.

## Requirements

- Docker with the Compose plugin
- A `.env` file in the project root

## Configure

Copy `.env.example` to `.env` and set the database name, username, and password. The Compose setup publishes PostgreSQL on port `5433` on your computer and uses port `5432` between containers.

```bash
cp .env.example .env
```

## Start and load data

Start PostgreSQL and wait for its health check:

```bash
docker compose up -d db
```

Create the tables (safe to rerun):

```bash
docker compose exec -T db psql -U YOUR_POSTGRES_USER -d YOUR_POSTGRES_DB < .sql/01_create_schemas.sql
```

Replace `YOUR_POSTGRES_USER` and `YOUR_POSTGRES_DB` with the values from `.env`.

Run the loader as a one-off Compose container:

```bash
docker compose run --rm python-app
```

The loader requests country data, rejects records missing required fields or a two-item coordinate list, then inserts the accepted countries and a run summary. The `python-app` service connects to PostgreSQL using the internal Compose host and port. To run the Python script directly on your computer instead, install the packages with `pip install -r requirements.txt` and set `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5433` in `.env`.

## Inspect extraction runs

List recent runs to find the ID to use in the analysis queries:

```bash
docker compose exec db psql -U YOUR_POSTGRES_USER -d YOUR_POSTGRES_DB -c 'SELECT id, rows_accepted, rows_rejected, extracted_at FROM extraction_runs ORDER BY id DESC;'
```

Replace `YOUR_POSTGRES_USER` and `YOUR_POSTGRES_DB` with the values from `.env`.

## Run the analysis queries

Each query in `.sql/02_*.sql`, `.sql/03_*.sql`, and `.sql/04_*.sql` currently filters on `extraction_run_id = 1`. Edit that value in the query file to analyze a different run, then execute the desired file. For example:

```bash
docker compose exec -T db psql -U YOUR_POSTGRES_USER -d YOUR_POSTGRES_DB < .sql/02_country_population_and_regional_share.sql
```

The query files compare countries' population shares within their regions, rank regions by average population density, and summarize populations by shared timezone.
