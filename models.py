from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from db import Model, engine
from typing import Optional


# Join table for simple many to many relationship
# between products and countries, some products was produced
# in multiple countries (Poland/Portugal)
ProductCountry = (Table('products_countries',
Model.metadata, Column('product_id', ForeignKey('products.id')), Column('country_id',
ForeignKey('countries.id'))))

# class name convention `Product`, database table name convention `products`
# many products to one manufacuturer 
class Product(Model):
    __tablename__ = 'products'
# columns
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64), index = True, unique = True)
    #manufacturer: Mapped[str] = mapped_column(String(64), index = True)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index = True) #or Manufacturer.id
    year: Mapped[int] = mapped_column(index = True)
    cpu: Mapped[Optional[str]] = mapped_column(String(32)) # optional[str] = can be NULL
# objects
    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates = 'products') # lazy = 'joined' => eager loader active
    countries: Mapped[list['Country']] = relationship(
                secondary='products_countries', back_populates='products')

    def __repr__(self):
        return f'Product({self.id}|{self.name}|{self.year}|{self.cpu})'


# one manufacturer to many products relationship
class Manufacturer(Model):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64), index = True, unique = True)
    products: Mapped[list['Product']] = relationship(
        cascade = 'all, delete-orphan', back_populates = 'manufacturer') # cascade 'save-update, merge' -> default setting, 'all, delete-orphan'

    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'


class Country(Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    
    products: Mapped[list['Product']] = relationship(secondary='products_countries', back_populates='countries')
    def __repr__(self):
        return f'Country({self.id}, "{self.name}")'




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
