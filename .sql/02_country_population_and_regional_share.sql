-- Which countries have the largest populations, and what share of their regions total population does each country represent?
SELECT 
    name, 
    region,
    population,
    ROUND(population::NUMERIC / SUM(population) OVER(
        PARTITION BY region
    ) * 100, 2) AS regional_population_share
FROM countries
WHERE extraction_run_id = 3 AND
      population != 0
ORDER BY population DESC;
