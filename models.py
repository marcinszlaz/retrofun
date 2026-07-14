from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from db import Model, engine
from typing import Optional

#class name convention `Product`, database table name convention `products`
# many products to one manufacuturer 
class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64), index = True, unique = True)
    #manufacturer: Mapped[str] = mapped_column(String(64), index = True)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index = True) #or Manufacturer.id
    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates = 'products')
    year: Mapped[int] = mapped_column(index = True)
    country: Mapped[Optional[str]] = mapped_column(String(32))
    cpu: Mapped[Optional[str]] = mapped_column(String(32))

    def __repr__(self):
        return f'Product({self.id}|{self.name}|{self.manufacturer}|{self.year}|{self.country}|{self.cpu})'


# one manufacturer to many products relationship
class Manufacturer(Model):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64), index = True, unique = True)
    products: Mapped[list['Product']] = relationship(
        cascade = 'all, delete-orphan', back_populates = 'manufacturer')

    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'


#c64 = Product(name = 'Commodore 64', manufacturer = 'Commodore')
#longer version
#with Session(engine) as session:
#    try:
#        session.add(c64)
#        session.commit()
#    except:
#        session.rollback()
#        raise
#    print(c64)

#shorter version with begin()
#begin() under the hood do try/except magic
#with Session(engine) as session:
#    with session.begin():
#        session.add(c64)
#    print(c64)
