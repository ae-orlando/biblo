import psycopg
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation


class DuplicateSKU(Exception): pass
class MissingItem(Exception): pass
class InsufficientStock(Exception): pass


class Repository:
    def __init__(self,dsn): self.dsn=dsn

    def connect(self): return psycopg.connect(self.dsn,connect_timeout=3,row_factory=dict_row)

    def initialize(self):
        # Lab bootstrap only; production schema evolution needs versioned migrations.
        with self.connect() as connection:
            connection.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                sku text NOT NULL UNIQUE CHECK(sku ~ '^[A-Z0-9][A-Z0-9_-]{0,39}$'),
                available integer NOT NULL CHECK(available>=0))''')

    def create(self,sku,available):
        try:
            with self.connect() as connection:
                return connection.execute('INSERT INTO inventory(sku,available) VALUES(%s,%s) RETURNING id,sku,available',(sku,available)).fetchone()
        except UniqueViolation as error: raise DuplicateSKU() from error

    def get(self,identifier):
        with self.connect() as connection:
            row=connection.execute('SELECT id,sku,available FROM inventory WHERE id=%s',(identifier,)).fetchone()
            if row is None: raise MissingItem()
            return row

    def reserve(self,identifier,quantity):
        with self.connect() as connection:
            row=connection.execute('UPDATE inventory SET available=available-%s WHERE id=%s AND available>=%s RETURNING id,sku,available',(quantity,identifier,quantity)).fetchone()
            if row is not None: return row
            exists=connection.execute('SELECT 1 FROM inventory WHERE id=%s',(identifier,)).fetchone()
            if exists is None: raise MissingItem()
            raise InsufficientStock()
