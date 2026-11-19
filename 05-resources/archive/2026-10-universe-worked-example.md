# Universe Database

Historical worked example, preserved during the rebuild. Attempt [[universe-database]] before consulting this full script. Its exact columns/row counts are exercise-specific, not general schema-quality criteria; sci-fi seed values are illustrative rather than astronomical reference data.

Postgres project. Copy-paste in order in `psql`. Sci-fi seed data allowed.

## 1. Create + connect

```sql
CREATE DATABASE universe;
\c universe
```

## 2. Create tables (galaxy first due to FKs)

```sql
CREATE TABLE galaxy (
  galaxy_id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  type VARCHAR(50) NOT NULL,
  num_stars INT,
  distance_mly NUMERIC,
  description TEXT,
  has_supermassive_black_hole BOOLEAN
);

CREATE TABLE star (
  star_id SERIAL PRIMARY KEY,
  galaxy_id INT NOT NULL REFERENCES galaxy(galaxy_id),
  name VARCHAR(50) UNIQUE NOT NULL,
  spectral_type VARCHAR(20),
  temperature_k INT,
  mass_solar_units NUMERIC,
  has_planets BOOLEAN NOT NULL
);

CREATE TABLE planet (
  planet_id SERIAL PRIMARY KEY,
  star_id INT NOT NULL REFERENCES star(star_id),
  name VARCHAR(50) UNIQUE NOT NULL,
  atmosphere_type VARCHAR(30),
  diameter_km INT,
  mass_earth_units NUMERIC NOT NULL,
  has_life BOOLEAN NOT NULL,
  has_atmosphere BOOLEAN
);

CREATE TABLE moon (
  moon_id SERIAL PRIMARY KEY,
  planet_id INT NOT NULL REFERENCES planet(planet_id),
  name VARCHAR(50) UNIQUE NOT NULL,
  diameter_km INT,
  discovery_year INT,
  is_spherical BOOLEAN NOT NULL,
  has_atmosphere BOOLEAN
);

CREATE TABLE constellation (
  constellation_id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  abbreviation VARCHAR(10) UNIQUE NOT NULL,
  brightest_star VARCHAR(50),
  num_stars INT,
  area_sq_deg NUMERIC,
  is_zodiac BOOLEAN
);
```

Why this passes:
- 5 tables, each PK `table_name_id SERIAL PRIMARY KEY` (auto-increment).
- Each has `name VARCHAR UNIQUE NOT NULL`.
- FKs keep referenced name: `star.galaxy_id -> galaxy.galaxy_id`, `planet.star_id -> star.star_id`, `moon.planet_id -> planet.planet_id`.
- `INT` non-key: `galaxy.num_stars`, `star.temperature_k`, `planet.diameter_km`, `moon.discovery_year`, etc.
- `NUMERIC`: `galaxy.distance_mly`, `star.mass_solar_units`, etc.
- `TEXT`: `galaxy.description`.
- `BOOLEAN` x7: `galaxy.has_supermassive_black_hole`, `star.has_planets`, `planet.has_life`, `planet.has_atmosphere`, `moon.is_spherical`, `moon.has_atmosphere`, `constellation.is_zodiac`.
- 2+ `NOT NULL` per table via PK + `name NOT NULL` + others. 1+ `UNIQUE` per table via `name`.
- Col counts: galaxy 7, star 7, planet 8, moon 7, constellation 7.

## 3. Seed data (6 / 8 / 12 / 22 / 5)

```sql
INSERT INTO galaxy (name, type, num_stars, distance_mly, description, has_supermassive_black_hole) VALUES
('Milky Way', 'Spiral', 250000000, 0.0, 'Home galaxy with Earth and the Federation outpost', TRUE),
('Andromeda', 'Spiral', 1000000000, 2.5, 'Nearest large neighbor, on collision course in 4B years', TRUE),
('Triangulum', 'Spiral', 40000000, 3.0, 'Third largest in Local Group, Jedi survey zone', FALSE),
('Whirlpool', 'Spiral', 160000000, 23.0, 'Grand-design spiral with Cybertron colony', TRUE),
('Sombrero', 'Spiral', 800000000, 29.0, 'Bright nucleus world of the Vulcan archives', TRUE),
('Alderaan Drift', 'Irregular', 5000000, 45.7, 'Sci-fi drift belt where Alderaan and Tatooine systems formed', FALSE);

INSERT INTO star (galaxy_id, name, spectral_type, temperature_k, mass_solar_units, has_planets) VALUES
(1, 'Sun', 'G2V', 5778, 1.00, TRUE),
(1, 'Proxima Centauri', 'M5V', 3042, 0.12, TRUE),
(1, 'Sirius', 'A1V', 9940, 2.06, TRUE),
(1, 'Vega', 'A0V', 9602, 2.14, TRUE),
(6, 'Alderaan Sun', 'G1V', 5900, 1.05, TRUE),
(2, 'Andromeda-X1', 'K5V', 4400, 0.70, TRUE),
(3, 'Triangulum-X1', 'M2V', 3500, 0.45, FALSE),
(5, 'Cybertron Prime', 'O9V', 33000, 18.50, TRUE);

INSERT INTO planet (star_id, name, atmosphere_type, diameter_km, mass_earth_units, has_life, has_atmosphere) VALUES
(1, 'Mercury', 'Exosphere', 4879, 0.055, FALSE, FALSE),
(1, 'Venus', 'CO2', 12104, 0.815, FALSE, TRUE),
(1, 'Earth', 'N2-O2', 12742, 1.000, TRUE, TRUE),
(1, 'Mars', 'CO2', 6779, 0.107, FALSE, TRUE),
(1, 'Jupiter', 'H2-He', 139820, 317.80, FALSE, TRUE),
(1, 'Saturn', 'H2-He', 116460, 95.20, FALSE, TRUE),
(1, 'Uranus', 'H2-He-CH4', 50724, 14.50, FALSE, TRUE),
(1, 'Neptune', 'H2-He-CH4', 49244, 17.10, FALSE, TRUE),
(5, 'Tatooine', 'N2-O2', 11800, 0.900, TRUE, TRUE),
(8, 'Cybertron', 'Metallic', 25000, 3.500, TRUE, TRUE),
(2, 'Proxima-b', 'Rocky', 11000, 1.070, FALSE, TRUE),
(6, 'Dagobah', 'Humid', 14410, 1.200, TRUE, TRUE);

INSERT INTO moon (planet_id, name, diameter_km, discovery_year, is_spherical, has_atmosphere) VALUES
(3, 'Moon', 3474, 1610, TRUE, FALSE),
(4, 'Phobos', 22, 1877, FALSE, FALSE),
(4, 'Deimos', 12, 1877, FALSE, FALSE),
(5, 'Io', 3643, 1610, TRUE, TRUE),
(5, 'Europa', 3122, 1610, TRUE, FALSE),
(5, 'Ganymede', 5268, 1610, TRUE, FALSE),
(5, 'Callisto', 4821, 1610, TRUE, FALSE),
(6, 'Titan', 5150, 1655, TRUE, TRUE),
(6, 'Enceladus', 504, 1789, TRUE, FALSE),
(6, 'Rhea', 1528, 1672, TRUE, FALSE),
(7, 'Titania', 1578, 1787, TRUE, FALSE),
(7, 'Oberon', 1523, 1787, TRUE, FALSE),
(7, 'Ariel', 1158, 1851, TRUE, FALSE),
(8, 'Triton', 2707, 1846, TRUE, TRUE),
(8, 'Proteus', 420, 1989, FALSE, FALSE),
(9, 'Mos Eisley-1', 1800, 2777, TRUE, TRUE),
(9, 'Mos Eisley-2', 950, 2778, FALSE, FALSE),
(10, 'Starkiller', 3200, 3010, TRUE, TRUE),
(11, 'Proxima Luna-1', 1200, 2990, TRUE, FALSE),
(12, 'Dagobah Minor', 800, 3001, FALSE, TRUE),
(3, 'Death Star', 160, 1977, TRUE, TRUE),
(10, 'Unicron Eye', 2100, 3015, FALSE, FALSE);

INSERT INTO constellation (name, abbreviation, brightest_star, num_stars, area_sq_deg, is_zodiac) VALUES
('Orion', 'ORI', 'Rigel', 81, 594.12, FALSE),
('Ursa Major', 'UMA', 'Alioth', 93, 1279.66, FALSE),
('Cassiopeia', 'CAS', 'Schedar', 55, 598.41, FALSE),
('Lyra', 'LYR', 'Vega', 45, 286.48, FALSE),
('Vulcan', 'VUL', 'TKhut', 12, 150.75, TRUE);
```

IDs assume insert order (SERIAL starts at 1). Insert galaxies -> stars -> planets -> moons.

## 4. Verify

```sql
SELECT count(*) FROM galaxy; -- >=6
SELECT count(*) FROM star; -- >=6
SELECT count(*) FROM planet; -- >=12
SELECT count(*) FROM moon; -- >=20
SELECT table_name FROM information_schema.tables WHERE table_schema='public';
\d galaxy
\d star
\d planet
\d moon
\d constellation
```

## Related Notes
- `02-notes/01-databases/00-postgres/99-practice-projects/universe databas.md`
