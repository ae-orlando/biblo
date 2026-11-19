def load_config(env):
    token = env.get('TRAINING_TOKEN', '').strip()
    if not token:
        raise ValueError('TRAINING_TOKEN is required')
    port_text = env.get('PORT', '8000')
    if not isinstance(port_text, str) or not port_text.isascii() or not port_text.isdecimal():
        raise ValueError('PORT must contain decimal digits')
    port = int(port_text)
    if not 1 <= port <= 65535:
        raise ValueError('PORT must be 1..65535')
    debug = env.get('DEBUG', 'false')
    if debug not in {'true', 'false'}:
        raise ValueError('DEBUG must be true or false')
    return {'token': token, 'port': port, 'debug': debug == 'true'}
