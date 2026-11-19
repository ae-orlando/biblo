import csv
import json
import os
from pathlib import Path
import tempfile


def load_rows(path):
    records=[]
    with Path(path).open(encoding='utf-8',newline='') as source:
        reader=csv.DictReader(source,strict=True)
        if reader.fieldnames!=['category','amount_cents']: raise ValueError('invalid CSV header')
        for row in reader:
            category=(row.get('category') or '').strip().lower()
            amount=row.get('amount_cents') or ''
            if None in row or not category or not amount or not amount.isascii() or not amount.isdecimal():
                raise ValueError(f'invalid CSV at physical line {reader.line_num}')
            records.append({'category':category,'cents':int(amount)})
    return records


def summarize(records):
    groups={}
    for record in records:
        key=record['category']
        previous=groups.get(key,{'category':key,'count':0,'cents':0})
        groups[key]={'category':key,'count':previous['count']+1,'cents':previous['cents']+record['cents']}
    categories=[groups[key] for key in sorted(groups)]
    return {'categories':categories,'total_cents':sum(row['cents'] for row in categories)}


def save(destination, report):
    destination=Path(destination)
    if destination.is_symlink(): raise ValueError('refusing symlink output')
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=destination.parent,prefix='.report-',delete=False) as file:
            temporary=Path(file.name); file.write(text)
        os.replace(temporary,destination)
    finally:
        if temporary is not None: temporary.unlink(missing_ok=True)
