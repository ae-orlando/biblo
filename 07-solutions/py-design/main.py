from dataclasses import dataclass


@dataclass(frozen=True)
class StockItem:
    sku: str
    available: int


class Inventory:
    def __init__(self):
        self._stock = {}

    def add(self, sku, quantity):
        if not isinstance(sku,str) or not sku or sku!=sku.strip() or sku in self._stock:
            raise ValueError('invalid or duplicate sku')
        if type(quantity) is not int or quantity<0: raise ValueError('invalid quantity')
        self._stock[sku]=StockItem(sku,quantity)

    def get(self, sku):
        return self._stock[sku]

    def reserve(self, sku, quantity):
        if type(quantity) is not int or quantity<=0: raise ValueError('invalid quantity')
        current=self.get(sku)
        if current.available<quantity: raise ValueError('insufficient stock')
        updated=StockItem(sku,current.available-quantity)
        self._stock[sku]=updated
        return updated

    def snapshot(self):
        return [{'sku':sku,'available':self._stock[sku].available} for sku in sorted(self._stock)]
