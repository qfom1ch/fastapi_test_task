import datetime

import pytest


@pytest.mark.parametrize(
    "phone_customer, status_code, count_order",
    [
        (
                "321",
                200,
                0,

        ),
        (
                "wrong_phone",
                401,
                1,
        ),

    ]
)
async def test_delete_order(client,
                            create_worker_in_database,
                            create_customer_in_database,
                            create_store_in_database,
                            create_store_mtm_workers,
                            create_order_in_database,
                            get_order_from_database,
                            phone_customer,
                            status_code,
                            count_order
                            ):
    worker_data = {
        "id": 1,
        "name": "Serega",
        "phone": "123",
    }
    await create_worker_in_database(**worker_data)

    store_data = {
        "id": 1,
        "name": "Magnit",
    }
    await create_store_in_database(**store_data)

    link_data = {
        "id": 1,
        "stores_id": 1,
        "workers_id": 1,
    }
    await create_store_mtm_workers(**link_data)

    customer_data = {
        "id": 1,
        "name": "Customer1",
        "phone": "321",
        "store_id": 1,
    }
    await create_customer_in_database(**customer_data)

    order_data = {
        "id": 1,
        "creation_time": datetime.datetime(2023, 5, 7),
        "end_time": datetime.datetime(2024, 5, 7),
        "store_id": 1,
        "author_id": 1,
        "status": "started",
        "executor_id": 1,
    }
    await create_order_in_database(**order_data)

    resp = client.delete(
        f"/orders/?customer_phone={phone_customer}&order_id=1")
    assert resp.status_code == status_code
    posts_from_db = await get_order_from_database(order_data["id"])
    assert len(posts_from_db) == count_order
