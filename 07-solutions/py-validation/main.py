def parse_count(text):
    if not isinstance(text, str):
        raise TypeError('count must be text')
    stripped = text.strip()
    if not stripped or not stripped.isascii() or not stripped.isdecimal():
        raise ValueError('count must contain ASCII decimal digits')
    value = int(stripped)
    if value > 100000:
        raise ValueError('count exceeds 100000')
    return value
