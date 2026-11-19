import csv
import json
import os
from pathlib import Path
import tempfile


def load_expenses(path):
    rows = []
    with Path(path).open(encoding='utf-8', newline='') as source:
        reader = csv.DictReader(source, strict=True)
        if reader.fieldnames != ['category','amount_cents']:
            raise ValueError('expected category,amount_cents header')
        try:
            for row in reader:
                category = (row.get('category') or '').strip()
                amount = row.get('amount_cents') or ''
                if None in row or not category or not amount or not amount.isascii() or not amount.isdecimal():
                    raise ValueError(f'invalid CSV record at physical line {reader.line_num}')
                rows.append({'category':category,'cents':int(amount)})
        except csv.Error as error:
            raise ValueError(f'invalid CSV near physical line {reader.line_num}') from error
    return rows


def write_report(path, data):
    destination = Path(path)
    if destination.is_symlink(): raise ValueError('refusing symlink destination')
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent, prefix='.report-', delete=False) as output:
            temporary = Path(output.name)
            output.write(text)
        os.replace(temporary, destination)
    finally:
        if temporary is not None: temporary.unlink(missing_ok=True)
