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
