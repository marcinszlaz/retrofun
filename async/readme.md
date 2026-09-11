## async version

* What we have here? Whole app was rewrited to support asynchronous way of life
----------------------------------------------------------------------------------
* at the beginnig I had an idea, to make async branch in git, but NO, I'll make all async code inside this folder (./async),

### python section
----------------------------------------------------
* `python -m asyncio` - REPL with support to async programs (you can use await keyword directly from the prompt, regular Python sessions only allows await inside functions declared with async def)
*

### pip section
------------------------------------------------------------------------------------
* `pip install aiosqlite` - driver for sqlite
* `DATABASE_URL=sqlite+aiosqlite:///retrofun_a` - url for sqlite,
* `pip install aiomysql` - driver for mysql,
* `DATABASE_URL=mysql+aiomysql://login:password@10.215.14.30:3310/retrofun_a` - url for mysql
* `pip install asyncpg` - driver for postgresql,
* `DATABASE_URL=postgresql+asyncpg://login:password@10.215.14.30:5432/retrofun_a` - url for postresql

### alembic section
* `alembic init -t async migrations` - use alembic init but with template (-t) for asynchronous database code, migrations is folder
* 
