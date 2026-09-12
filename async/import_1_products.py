import asyncio
import csv
from datetime import datetime
from sqlalchemy import delete, select
from db import Session 
# removed after alembic implementation (Model, engine)
from models import (Product, Manufacturer, Country, ProductCountry, Customer,
Customer, Order, OrderItem)


async def main():
# Model.metadata.drop_all(engine) # deletes all data (tables)
# Model.metadata.create_all(engine) # creates tables
# removed after alembic implementation
    async with Session() as session:
        async with session.begin():
            await session.execute(delete(ProductCountry))
            await session.execute(delete(Product))
            await session.execute(delete(Manufacturer))
            await session.execute(delete(Country))

    async with Session() as session:
        async with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}
                all_countries = {}

                for row in reader:
                    row['year'] = int(row['year'])
                   
                    manufacturer = row.pop('manufacturer')
                    countries = row.pop('country').split('/')
                    p = Product(**row)
                    
                    if manufacturer not in all_manufacturers:
                        m = Manufacturer(name = manufacturer)
                        session.add(m)
                        all_manufacturers[manufacturer] = m
                    all_manufacturers[manufacturer].products.append(p)
                    #session.add(p) it isn't necessary

                    for country in countries:
                        if country not in all_countries:
                            c = Country(name=country)
                            session.add(c)
                            all_countries[country] = c
                        all_countries[country].products.append(p)
                        # p.countries.append(all_countries[country])

if __name__ == '__main__':
    asyncio.run(main())
