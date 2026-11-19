def get_store():
    raise NotImplementedError('export the same dependency object used by the routes')


def create_app(store=None):
    raise NotImplementedError('separate app-owned state, domain logic and HTTP adaptation')
