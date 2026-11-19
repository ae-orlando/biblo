def shipping_fee(subtotal_cents, zone):
    if type(subtotal_cents) is not int or subtotal_cents < 0 or zone not in ('local', 'domestic'):
        return None
    if zone == 'local':
        return 0 if subtotal_cents >= 5000 else 500
    return 0 if subtotal_cents >= 10000 else 1200


def grade(score):
    if type(score) is not int or not 0 <= score <= 100:
        return None
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    if score >= 70: return 'C'
    if score >= 60: return 'D'
    return 'F'
