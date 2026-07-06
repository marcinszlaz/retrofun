from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from db import Model, engine


#class name convention `Product`, database table name convention `products`
class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64))
    manufacturer: Mapped[str] = mapped_column(String(64))
    year: Mapped[int]
    country: Mapped[str] = mapped_column(String(32))
    cpu: Mapped[str] = mapped_column(String(32))

    def __repr__(self):
        return f'Product({self.id}, "{self.name}", manufacturer: {self.manufacturer})'


c64 = Product(name = 'Commodore 64', manufacturer = 'Commodore')
with Session(engine) as session:
    try:
        session.add(c64)
        session.commit()
    except:
        session.rollback()
        raise
    print(c64)
#shorter version with begin()
with Session(engine) as session:
    with session.begin():
        session.add(c64)
    print(c64)

#Model.metadata.create_all(engine)
#Model.metadata.drop_all(engine)
