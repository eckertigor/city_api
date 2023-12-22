CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TYPE beauty AS ENUM ('ugly', 'average', 'gorgeous');

CREATE TABLE IF NOT EXISTS public.city
(
    uuid                    uuid           primary key DEFAULT uuid_generate_v4(),
    name                    text           not null,
    geo_location_latitude   float          not null,
    geo_location_longitude  float          not null,
    beauty                  beauty         not null,
    population              bigint         not null
);

CREATE TABLE IF NOT EXISTS public.city_ally
(
    city                    uuid           REFERENCES city(uuid),
    ally                    uuid           REFERENCES city(uuid),
    PRIMARY KEY (city, ally)
);

CREATE INDEX idx_city_ally_city ON public.city_ally(city);
