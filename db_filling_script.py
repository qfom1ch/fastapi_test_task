import asyncio
import random

import asyncpg
from mimesis import Datetime, Person
from mimesis.locales import Locale

from config import REAL_DATABASE_URL

person = Person(Locale.EN)
date = Datetime()


async def main():
    conn = await asyncpg.connect("".join(REAL_DATABASE_URL.split("+asyncpg")))
    worker_id = 1
    customer_id = 1
    store_id = 1
    stores_mtm_workers_id = 1
    order_id = 1
    visit_id = 1
    status_list = ['started', 'ended', 'in_process',
                   'awaiting', 'canceled']
    try:
        for _ in range(150):
            await conn.execute('''
                INSERT INTO workers VALUES($1, $2, $3)
            ''', worker_id, person.name(), person.phone_number(mask='+7###'))
            worker_id += 1

        for _ in range(150):
            await conn.execute('''
                INSERT INTO stores VALUES($1, $2)
            ''', store_id, person.phone_number(mask='Store###'))
            store_id += 1

        for _ in range(150):
            await conn.execute('''
                INSERT INTO customers VALUES($1, $2, $3, $4)
            ''', customer_id, person.name(), person.phone_number(mask='+8###'),
                               customer_id)
            customer_id += 1

        for _ in range(200):
            await conn.execute('''
                INSERT INTO stores_mtm_workers VALUES($1, $2, $3)
            ''', stores_mtm_workers_id, random.randint(1, 150),
                               random.randint(1, 150))
            stores_mtm_workers_id += 1

        for _ in range(200):
            await conn.execute('''
                INSERT INTO orders VALUES($1, $2, $3, $4, $5, $6, $7)
            ''', order_id, date.date(start=2015, end=2022),
                               date.date(start=2023, end=2025),
                               random.randint(1, 150),
                               random.randint(1, 150),
                               status_list[random.randint(0, 4)],
                               random.randint(1, 150))
            order_id += 1

        for _ in range(150):
            await conn.execute('''
                INSERT INTO visits VALUES($1, $2, $3, $4, $5, $6)
            ''', visit_id, date.date(start=2015, end=2022),
                               random.randint(1, 150),
                               random.randint(1, 200),
                               random.randint(1, 150),
                               random.randint(1, 150))
            visit_id += 1
    except Exception:
        pass
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
