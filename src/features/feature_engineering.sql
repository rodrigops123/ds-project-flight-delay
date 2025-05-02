-- src/preprocessing/cleaning.sql

DROP TABLE IF EXISTS flights_transformed;

CREATE TABLE flights_transformed AS
SELECT *,
    CASE
        WHEN flight_depart_delay > 15 THEN 1
        ELSE 0
    END AS is_dalayed
FROM flights_clean