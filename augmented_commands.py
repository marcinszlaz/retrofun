#commands used in Python REPL

from db import Session, engine
from models import Product
from sqlalchemy import select, or_, and_, not_

session = Session()

#with this above imported we can get access to database through Python interactive Python console (REPL), we need Session = sessionmaker(engine), Table model (Product) and function select() from sqlalchemy

q = select(Product) # query for table Product model (without data, only modeli from sqlalchemy) with this sqlalchemy.orm magic (session) can request data from `physical` database (sqlite, mysql etc.)
print(q) #prints sql query hiding behind object model
r = session.execute(q)
list(r) #retrieve data from db
r = session.execute(q).all() #list of tuple
r = session.execute(q).first() #first result
r = session.execute(q).one() #one result or error if none or more than one
r = session.execute(q).one_or_none() # one or none, if more than one => error
#you can make same `r` but with scalars() function, scalars() returns different object
q = select(Product).where(Product.manufacturer == 'Commodore')
session.scalars(q).all()
q = select(Product).where(Product.year >= 1990)
q = select(Product).where(Product.manufacturer == 'Commodore', Product.year == 1980)
#you can use: and_(), or_(), not_() functions (self explanatory names)
q = select(Product).where(Product.name.like('%Sinclair%'))
#wildcard => `%` it means 0,1 or many chars
#`_` means one sign/char
#`ilike()` case insensitive like()
q = select(Product).where(Product.year.between(1970,1979))
print(q) #secure query (prevent sql injection)
print(q.compile(compile_kwargs={'literal_binds': True})) #unsecure query view :-)

q = select(Product).order_by(Product.year.desc())
q.=.select(Product).order_by(Product.year.desc(), Product.name.asc()))
from sqlalchemy import func #import aggregation functions
q = select(func.count(Product.id))
q = select(Product.manufacturer).order_by(Product.manufacturer)
q = select(Product.manufacturer).order_by(Product.manufacturer).distinct()
q = select(func.count(Product.manufacturer.distinct())) #disinct always in 

q = (select(
            Product.manufacturer,
            func.min(Product.year),
            func.max(Product.year),
            func.count()
        )
        .group_by(Product.manufacturer)
        .order_by(Product.manufacturer))

q = (select(Product.manufacturer, func.count()).group_by(Product.manufacturer).having(func.count() >= 5).order_by(func.count(Product.manufacturer).desc(), Product.manufacturer))
#instead of AS you can use function .label(), for egzample:
num_products = func.count().label(None) #or .label('your label')
    q = (select(
            Product.manufacturer,
            num_products
        )
        .group_by(Product.manufacturer)
        .having(num_products >= 5)
        .order_by(Product.manufacturer))
q = select(Product).where(Product.id == 23)
#OR
session.get(Product,23)
# limit(), offset() - uesefull funcions! Like in SQL

