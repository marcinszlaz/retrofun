# Copyright(c) by Marcin Szlaz xD.
# functions c & d resolving problem with data listing

from db import Session, engine
from models import Product
from sqlalchemy import select, or_, and_, not_
session = Session()


def cf(data, yield_: int = 5, offset: int = 0)->None:
    """ scalars, return list """
    result = session.scalars(data).all()
    if len(result) >= yield_:
        try:
            for _ in range(yield_):
                print(f"{_+1+offset}: {result[_+offset]}")
        except IndexError as ix:
            print(f"Decrease yield_ or offset. {ix}")
    elif yield_ > len(result):
        print(f'gave yield_ is {yield_} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    print(f'processed data rows yield_: {yield_}/{len(result)}')
    return None

def df(data, yield_: int = 5, offset: int = 0)->None:
    """ execute, returns tuples """
    result = session.execute(data).all()
    if len(result) >= yield_:
        try:
            for _ in range(yield_):
                print(f"{_+1+offset}: {result[_+offset]}")
        except IndexError as ix:
            print(f"Decrease yield_ or offset. {ix}")
    elif yield_ > len(result):
        print(f'gave yield_ is {yield_} but list length is {len(result)}')
    else:
        print('The query which was given is empty')
    print(f'processed data rows yield_: {yield_}/{len(result)}')
    return None

def cp(query)->None:
    print(query.compile(compile_kwargs={'literal_binds': True}))

# Copyright(c) by Marcin Szlaz xD.


