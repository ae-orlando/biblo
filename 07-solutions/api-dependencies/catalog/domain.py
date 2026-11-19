from threading import Lock
from uuid import uuid4


class DuplicateName(Exception):
    pass


class Store:
    def __init__(self):
        self._items={}
        self._lock=Lock()

    def create(self,name):
        with self._lock:
            if any(item['name']==name for item in self._items.values()): raise DuplicateName()
            item={'id':uuid4().hex,'name':name}
            self._items[item['id']]=item
            return item.copy()

    def all(self):
        with self._lock: return [item.copy() for item in self._items.values()]

    def get(self,identifier):
        with self._lock: return self._items[identifier].copy()
