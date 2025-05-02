-- src/preprocessing/cleaning.sql

DROP TABLE IF EXISTS flights_clean;

CREATE TABLE flights_clean AS
SELECT
    id,
    flight_date,
    flight_status,
    departure_airport,
    arrival_airport,
    departure_scheduled,
    arrival_scheduled,
    flight_number,
    airline_name,
    flight_depart_delay,
    flight_arrival_delay
FROM flights_raw
WHERE
    flight_date IS NOT NULL
    AND departure_airport IS NOT NULL
    AND arrival_airport IS NOT NULL
    AND flight_number IS NOT NULL
    AND departure_scheduled IS NOT NULL
    AND arrival_scheduled IS NOT NULL;