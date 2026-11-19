class Inventory:
    def __init__(self):
        raise NotImplementedError('give each instance its own stock')

    def add(self, sku, quantity):
        raise NotImplementedError

    def get(self, sku):
        raise NotImplementedError

    def reserve(self, sku, quantity):
        raise NotImplementedError

    def snapshot(self):
        raise NotImplementedError
