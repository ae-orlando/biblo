BEGIN;
UPDATE contacts SET email = lower(btrim(email));
ALTER TABLE contacts ALTER COLUMN email SET NOT NULL;
ALTER TABLE contacts ADD CONSTRAINT contacts_email_unique UNIQUE (email);
ALTER TABLE contacts ADD CONSTRAINT contacts_email_canonical
  CHECK (email <> '' AND email = lower(btrim(email)));
COMMIT;
