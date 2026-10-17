CREATE TABLE IF NOT EXISTS extraction_runs(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rows_accepted INTEGER NOT NULL DEFAULT 0,
    rows_rejected INTEGER NOT NULL DEFAULT 0,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS countries(
    extraction_run_id INTEGER NOT NULL 
        REFERENCES extraction_runs(id),
    alpha2_code TEXT NOT NULL,
    area NUMERIC NOT NULL,
    name TEXT NOT NULL,
    latitude NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL,
    region TEXT NOT NULL,
    timezones JSONB NOT NULL,
    population BIGINT NOT NULL,
    population_density NUMERIC NOT NULL,

    PRIMARY KEY (alpha2_code, extraction_run_id)
);