# Universe Database - Table Designs

Work inside the database called universe.

## 1. galaxy - 6 columns - plan 6 rows
- galaxy_id - INT - main identifier, fills in automatically, required, must be different for every row
- name - VARCHAR - required, must be different for every row
- type - VARCHAR - required
- distance_million_ly - INT - optional
- description - TEXT - optional, covers TEXT requirement
- has_supermassive_black_hole - BOOLEAN - required, covers BOOLEAN requirement

Planned rows (6):
Milky Way, Andromeda, Triangulum, Large Magellanic Cloud, Whirlpool, Sombrero

## 2. star - 7 columns - plan 8 rows
- star_id - INT - main identifier, fills in automatically, required, must be different for every row
- name - VARCHAR - required, must be different for every row
- galaxy_id - INT - links to galaxy / galaxy_id, same name as the column it points to, required
- spectral_type - VARCHAR - optional
- temperature_k - INT - required, covers INT requirement
- mass_solar_units - NUMERIC - optional, covers NUMERIC requirement
- has_planets - BOOLEAN - required

Planned rows (8):
- Sun -> Milky Way
- Proxima Centauri -> Milky Way
- Sirius -> Milky Way
- Vega -> Milky Way
- Polaris -> Milky Way
- Andromeda-X1 -> Andromeda
- Triangulum-X1 -> Triangulum
- Whirlpool-X1 -> Whirlpool

## 3. planet - 7 columns - plan 12 rows
- planet_id - INT - main identifier, fills in automatically, required, must be different for every row
- name - VARCHAR - required, must be different for every row
- star_id - INT - links to star / star_id, same name as the column it points to, required
- atmosphere_type - VARCHAR - optional
- diameter_km - INT - optional
- mass_earth_units - NUMERIC - required
- has_life - BOOLEAN - required

Planned rows (12):
- Mercury -> Sun
- Venus -> Sun
- Earth -> Sun
- Mars -> Sun
- Jupiter -> Sun
- Saturn -> Sun
- Uranus -> Sun
- Neptune -> Sun
- Proxima-b -> Proxima Centauri
- Sirius-b -> Sirius
- Vega-b -> Vega
- Polaris-b -> Polaris

## 4. moon - 7 columns - plan 21 rows
- moon_id - INT - main identifier, fills in automatically, required, must be different for every row
- name - VARCHAR - required, must be different for every row
- planet_id - INT - links to planet / planet_id, same name as the column it points to, required
- diameter_km - INT - optional
- discovery_year - INT - optional
- is_spherical - BOOLEAN - required
- has_atmosphere - BOOLEAN - optional

Planned rows (21):
- Moon -> Earth
- Phobos -> Mars
- Deimos -> Mars
- Io -> Jupiter
- Europa -> Jupiter
- Ganymede -> Jupiter
- Callisto -> Jupiter
- Titan -> Saturn
- Enceladus -> Saturn
- Rhea -> Saturn
- Iapetus -> Saturn
- Titania -> Uranus
- Oberon -> Uranus
- Ariel -> Uranus
- Umbriel -> Uranus
- Triton -> Neptune
- Proteus -> Neptune
- Nereid -> Neptune
- Luna-1 -> Proxima-b
- Luna-2 -> Sirius-b
- Luna-3 -> Vega-b

## 5. asteroid - 5 columns - plan 3 rows - 5th table to reach 5 tables total
- asteroid_id - INT - main identifier, fills in automatically, required, must be different for every row
- name - VARCHAR - required, must be different for every row
- composition - VARCHAR - optional
- diameter_km - INT - optional
- is_potentially_hazardous - BOOLEAN - required

Planned rows (3):
Ceres, Vesta, Bennu

## Checklist
- 5 tables, each has a name column of type VARCHAR
- Each main identifier follows table_name_id naming and fills automatically
- Foreign columns keep the same name as the column they point to
- INT used in several non-identifier columns, NUMERIC in star and planet, TEXT in galaxy, BOOLEAN in all tables
- Each table has 2+ required columns and 1+ column that must be different for every row
- Row counts: galaxy 6, star 8, planet 12, moon 21, asteroid 3
