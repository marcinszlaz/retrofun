from db import Session, engine
from models import Product
from sqlalchemy import select, or_, and_, not_
session = Session()


def c(data, count: int = 5, offset: int = 0)->None:
    """ scalars return list """
    result = session.scalars(data).all()
    if len(result) >= count:
        try:
            for _ in range(count):
                print(f"{_+1+offset}: {result[_+offset]}")
        except IndexError as ix:
            print(f"Decrease count or offset. {ix}")
    elif count > len(result):
        print(f'gave count is {count} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    print(f'processed data rows count: {count}/{len(result)}')
    return None

def d(data, count: int = 5, offset: int = 0)->None:
    """ execute returns tuples """
    result = session.execute(data).all()
    if len(result) >= count:
        try:
            for _ in range(count):
                print(f"{_+1+offset}: {result[_+offset]}")
        except IndexError as ix:
            print(f"Decrease count or offset. {ix}")
    elif count > len(result):
        print(f'gave count is {count} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    print(f'processed data rows count: {count}/{len(result)}')
    return None

