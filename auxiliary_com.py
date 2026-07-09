from db import Session, engine
from models import Product
from sqlalchemy import select, or_, and_, not_
session = Session()


def c(data, count: int = 1)->None:
    result = session.scalars(data).all()
    if len(result) >= count:
        for _ in range(count):
            print(result[_])
    elif count > len(result):
        print(f'gave count is {count} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    return print(f'{len(result)}')

def d(data, count: int = 1)->None:
    result = session.execute(data).all()
    if len(result) >= count:
        for _ in range(count):
            print(result[_])
    elif count > len(result):
        print(f'gave count is {count} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    return print(f'{len(result)}')


