-- Run only in your own empty scratch database in the vault practice cluster.
CREATE TABLE owners(id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,name text NOT NULL UNIQUE);
CREATE TABLE dogs(
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  age integer CHECK(age >= 0),
  owner_id bigint REFERENCES owners(id) ON DELETE SET NULL
);
INSERT INTO owners(name) VALUES ('Ana'),('Ben'),('Cara');
INSERT INTO dogs(name,age,owner_id) VALUES ('Gino',2,1),('Nora',3,1),('Milo',NULL,NULL);
-- Unique owner names are a toy label/seed convention, not a claim about people.
