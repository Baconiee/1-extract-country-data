# Country data

This project loads country data from [countries.dev](https://countries.dev) into PostgreSQL and includes SQL queries for exploring it. PostgreSQL runs in Docker; the Python script runs on your computer.

## Requirements

- Docker with the Compose plugin
- Python 3.10+

## Run the project

1. Start PostgreSQL:

   ```bash
   docker compose up -d db
   ```

2. Create the tables:

   ```bash
   docker compose exec -T db psql -U postgres -d postgres < .sql/01_create_schemas.sql
   ```

3. Create a virtual environment and install the Python dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the database settings used by `docker-compose.yml`:

   ```dotenv
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres
   ```

5. Load the data:

   ```bash
   python extract_country_data.py
   ```

## Run the SQL queries

For example, run the population query with:

```bash
docker compose exec -T db psql -U postgres -d postgres < .sql/02_country_population_and_regional_share.sql
```

Use the same command with another `.sql` file to run a different query. The query files currently filter on `extraction_run_id = 3`; change that value to the ID you want to analyze. Find run IDs with:

```bash
docker compose exec db psql -U postgres -d postgres -c 'SELECT id, rows_accepted, rows_rejected, extracted_at FROM extraction_runs ORDER BY id DESC;'
```


