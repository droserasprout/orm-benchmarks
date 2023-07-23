#!/usr/bin/env python
import os
import sys

try:
    concurrents = int(os.environ.get("CONCURRENTS", "10"))

    if concurrents != 10:
        loopstr = f" C{concurrents}"
    else:
        loopstr = ""
    if os.environ.get("UVLOOP", ""):
        import asyncio

        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
finally:
    pass

if concurrents > 1 and sys.version_info < (3, 7):
    sys.exit()

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    db_url = f"postgres://postgres:{os.environ.get('PASSWORD')}@127.0.0.1:5432/tbench?minsize={concurrents}&maxsize={concurrents}"
elif dbtype == "mysql":
    db_url = f"mysql://root:{os.environ.get('PASSWORD')}@127.0.0.1:3306/tbench?minsize={concurrents}&maxsize={concurrents}"
else:
    db_url = "sqlite:///tmp/db.sqlite3"


import test_a
import test_b
import test_c
import test_d
import test_e
import test_f
import test_g
import test_h
import test_i
import test_j
import test_k
from tortoise import Tortoise, run_async
from dipdup.transactions import TransactionManager

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(db_url=db_url, modules={"models": ["models"]})


async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()


async def run_benchmarks():
    async with TransactionManager(None).register():
        await create_db()
        await test_a.runtest(loopstr)
        await test_b.runtest(loopstr)
        await test_c.runtest(loopstr)
        await test_d.runtest(loopstr)
        await test_e.runtest(loopstr)
        await test_f.runtest(loopstr)
        await test_g.runtest(loopstr)
        await test_h.runtest(loopstr)
        await test_i.runtest(loopstr)
        await test_j.runtest(loopstr)
        await test_k.runtest(loopstr)


run_async(run_benchmarks())
