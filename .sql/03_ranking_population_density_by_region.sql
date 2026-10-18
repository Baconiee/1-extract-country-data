-- Business question: Which regions have the highest population density, and how do they compare?
SELECT 
    region,
    ROUND(AVG(population_density), 2) AS avg_population_density
FROM countries
WHERE extraction_run_id = 1
GROUP BY region
ORDER BY avg_population_density DESC;


