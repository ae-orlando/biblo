from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    user_id:str
    roles:frozenset[str]=frozenset()


def get_principal():
    raise NotImplementedError('deny unauthenticated requests; do not trust a user-id header')


def create_app():
    raise NotImplementedError('enforce object ownership independently of body validation')
