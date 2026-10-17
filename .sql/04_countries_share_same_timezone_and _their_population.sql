-- Which UTC offsets are shared by the most countries, and what is the combined population of countries using each offset?
SELECT 
    timezone,
    COUNT(1) AS number_of_countries,
    SUM(population) sum_of_population
FROM countries,
     jsonb_array_elements_text(timezones) AS tz(timezone)
WHERE extraction_run_id = 3
GROUP BY timezone
ORDER BY number_of_countries DESC;