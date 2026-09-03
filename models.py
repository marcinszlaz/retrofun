from datetime import datetime, UTC
from uuid import UUID, uuid4
from sqlalchemy import (String, ForeignKey, Table, Column,
Uuid, DateTime, Float, Text)
from sqlalchemy.orm import (Mapped, mapped_column, Session, relationship,
WriteOnlyMapped)
from db import Model, engine
from typing import Optional


# Join table for simple many to many relationship
# between products and countries, some products was produced
# in multiple countries (Poland/Portugal)
ProductCountry = (Table('products_countries',
Model.metadata, Column('product_id', ForeignKey('products.id')), Column('country_id', ForeignKey('countries.id'))))

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
# relationship objects
    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates = 'products') # lazy = 'joined' => eager loader active
    countries: Mapped[list['Country']] = relationship(
                secondary='products_countries', back_populates='products')
    order_items: WriteOnlyMapped['OrderItem'] = relationship(
    back_populates='product')
    reviews: WriteOnlyMapped['ProductReview'] = relationship(
        back_populates='product')
    blog_articles: WriteOnlyMapped['BlogArticle'] = relationship(
        back_populates='product')

    def __repr__(self):
        return f'Product({self.id}|{self.name}|{self.year}|{self.cpu})'


# one manufacturer to many products relationship
class Manufacturer(Model):
    __tablename__ = 'manufacturers'
# columns
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(64), index = True, unique = True)
# relationship objects
    products: Mapped[list['Product']] = relationship(
        cascade = 'all, delete-orphan', back_populates = 'manufacturer') # cascade 
    # 'save-update, merge' -> default setting, 'all, delete-orphan'

    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'

class Country(Model):
    __tablename__ = 'countries'
# columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
# relationship objects
    products: Mapped[list['Product']] = relationship(secondary='products_countries', 
    back_populates='countries')

    def __repr__(self):
        return f'Country({self.id}, "{self.name}")'

class Customer(Model):
    __tablename__ = 'customers'
# columns
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(128))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
# relationship objects
    orders: WriteOnlyMapped['Order'] = relationship(
        back_populates='customer')
    product_reviews: WriteOnlyMapped['ProductReview'] = relationship(
        back_populates='customer')
    blog_users: WriteOnlyMapped['BlogUser'] = relationship(
        back_populates='customer')

    def __repr__(self):
        return f"Customer({self.id.hex}, {self.name})"

class Order(Model):
    __tablename__ = 'orders'
# columns
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
    default=lambda:datetime.now(UTC), index=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'),
     index=True)
# relationship objects
    customer: Mapped['Customer'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(
    back_populates='order')

    def __repr__(self):
        return f"Order({self.timestamp}, {self.id.hex})"

# In case when your join table has their own columns, besides foreign
# keys as primary key, you have to use full class inherits from Model class.
# Another implications of table has additional columns is that, we can't
# use `secondary` parameter in relationship function.
class OrderItem(Model):
    __tablename__ = 'orders_items'
# columns
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),
    primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'),
    primary_key=True)
    unit_price: Mapped[float]
    quantity: Mapped[int]
# relationship objects
    product: Mapped['Product'] = relationship(back_populates='order_items')
    order: Mapped['Order'] = relationship(back_populates='order_items')

class ProductReview(Model):
    __tablename__ = 'products_reviews'
# columns
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), 
    primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'),
    primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
    default=lambda:datetime.now(UTC), index=True)
    rating: Mapped[int]
    comment: Mapped[Optional[str]] = mapped_column(Text)
# relationship objects
    product: Mapped['Product'] = relationship(back_populates='reviews')
    customer: Mapped['Customer'] = relationship(
        back_populates='product_reviews')

class BlogArticle(Model):
    __tablename__ = 'blog_articles'
# columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('blog_authors.id'),
                                           index=True)
    product_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('products.id'), index=True)
    language_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('languages.id'), index=True)
    translation_of_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('blog_articles.id'), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC), index=True)
# relationship objects
    author: Mapped['BlogAuthor'] = relationship(back_populates='articles')
    product: Mapped[Optional['Product']] = relationship(
        back_populates='blog_articles')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates='article')
    language: Mapped[Optional['Language']] = relationship(
        back_populates='blog_articles')
    translation_of: Mapped[Optional['BlogArticle']] = relationship(
        remote_side=id, back_populates='translations')
    translations: Mapped[list['BlogArticle']] = relationship(
        back_populates='translation_of')

    def __repr__(self):
        return  f'BlogArticle({self.id}, "{self.title}")'

class BlogAuthor(Model):
    __tablename__ = 'blog_authors'
# columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
# relationship object
    articles: WriteOnlyMapped['BlogArticle'] = relationship(
        back_populates='author')

    def __repr__(self):
        return f'BlogAuthor({self.id}, "{self.name}")'

class BlogUser(Model):
    __tablename__ = 'blog_users'
# columns
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    customer_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('customers.id'), index=True)
# relationship objects
    customer: Mapped[Optional['Customer']] = relationship(
        back_populates='blog_users')
    sessions: WriteOnlyMapped['BlogSession'] = relationship(
        back_populates='user')

    def __repr__(self):
        return f'BlogUser({self.id.hex})'

class BlogSession(Model):
    __tablename__ = 'blog_sessions'
# columns
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('blog_users.id'),
                                          index=True)
# relationship objects
    user: Mapped['BlogUser'] = relationship(back_populates='sessions')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates = 'session')

    def __repr__(self):
        return f'BlogSession({self.id.hex})'

class BlogView(Model):
   __tablename__ = 'blog_views'
# columns
   id: Mapped[int] = mapped_column(primary_key = True)
   article_id: Mapped[int] = mapped_column(ForeignKey('blog_articles.id'))
   session_id: Mapped[UUID] = mapped_column(ForeignKey('blog_sessions.id'))
   timestamp: Mapped[datetime] = mapped_column(default=datetime.now(UTC),
                                               index=True)
# relationship objects
   article: Mapped['BlogArticle'] = relationship(back_populates='views')
   session: Mapped['BlogSession'] = relationship(back_populates='views')

class Language(Model):
    __tablename__ = 'languages'
# columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
# relationship object
    blog_articles: WriteOnlyMapped['BlogArticle'] = relationship(
        back_populates='language')

    def __repr__(self):
        return f'Language({self.id}, "{self.name}")'


