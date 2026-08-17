# retrofun project
* explanation - sqlalchemy tutorial, mysql_server on docker is related with this project, name db, details in ~docker folders

## pip part :)
* `pip install sqlalchemy` sqlalchemy
* `pip install pymysql cryptography` mysql client in python, python driver
* db name = db, user = retrofun password = admin_xD driver = pymysql
* `pip install psycopg2-binary` - driver for PostgreSQL (we use here mysql)
* `pip install python-dotenv` - good old dotenv xD

## database part
* `mysql -h 10.215.14.30 -P 3310 -u retrofun -p retrofun` - enter to mysql in docker from linux, retrorun after -p is db-name
*  MySQL with pymysql:
    `url = 'mysql+pymysql://retrofun:my-password@localhost:3306/retrofun'`
* PostgreSQL with psycopg2:
    `url = 'postgresql+psycopg2://retrofun:my-password@localhost:5432/retrofun'`

## access to database from Python shell (REPL)
* `from sqlalchemy import select, func
  from db import Session
  from models import Product, Manufacturer
  session = Session()`
* ready to copy paste => 
from sqlalchemy import select,func, or_, and_, not_;from db import Session;from models import Product,Manufacturer,Country ProductCountry;session=Session();from auxiliary_com import c, d;from sqlalchemy.orm import joinedload;

## How to save your work in REPL?
* history of commands inputed in Python REPL are in /home/.python_history file
* script <file_name> save input/output to file, but works badly with tmux

## Database Migration [ALEMBIC]
* `pip install alembic` - install package,
* `alembic init migrations` - initializing, "migration" will be subdirectory with data
* `alembic revision --autogenerate -m"products, manufacturers, countries"` - first migration /  backup have to be run on empty database (no tables, no data), Model.metadata.drop_all(engine  ) commands clears all xD,
* `alembic upgrade head` - scripts itself doesn't create database, you have run the script you  rself,
* `alembic current` - shows current head, current revision of database, all backups have their unique revision codes,
* `alembic history` - shows history of upgrades, downgrades,
*
