from http.client import HTTPConnection
from urllib.parse import urlsplit


def diagnose(url):
    try:
        parsed = urlsplit(url)
        port = parsed.port if parsed.port is not None else 80
        if not 1 <= port <= 65535:
            raise ValueError('invalid port')
        if parsed.scheme != 'http' or parsed.hostname not in {'127.0.0.1', 'localhost', '::1'} or parsed.username is not None or parsed.password is not None or parsed.fragment:
            raise ValueError('only loopback HTTP URLs without credentials or fragments are allowed')
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError('invalid local HTTP URL') from error
    connection = HTTPConnection(parsed.hostname, port, timeout=1)
    try:
        path = (parsed.path or '/') + ('?' + parsed.query if parsed.query else '')
        connection.request('GET', path)
        response = connection.getresponse()
        # Deliberately do not follow redirects or read an unbounded response body.
        return {'layer': 'http', 'status': response.status, 'ok': 200 <= response.status < 300}
    except (OSError, TimeoutError):
        return {'layer': 'transport', 'error': 'unreachable'}
    finally:
        connection.close()
