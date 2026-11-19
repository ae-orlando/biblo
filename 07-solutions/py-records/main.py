def summarize_sales(records):
    if not isinstance(records, list):
        raise TypeError('records must be a list')
    seen = set()
    groups = {}
    for record in records:
        if not isinstance(record, dict): raise TypeError('record must be a dictionary')
        identifier = record.get('id')
        category = record.get('category')
        cents = record.get('cents')
        if not isinstance(identifier,str) or not identifier or identifier != identifier.strip(): raise ValueError('invalid id')
        if identifier in seen: raise ValueError('duplicate id')
        if not isinstance(category,str) or not category.strip(): raise ValueError('invalid category')
        if type(cents) is not int or cents < 0: raise ValueError('invalid cents')
        seen.add(identifier)
        key = category.strip().lower()
        previous = groups.get(key, {'category':key,'count':0,'cents':0})
        groups[key] = {'category':key,'count':previous['count']+1,'cents':previous['cents']+cents}
    return [groups[key] for key in sorted(groups)]
