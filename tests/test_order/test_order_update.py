import datetime
import json


async def test_update_order(client,
                            create_worker_in_database,
                            create_customer_in_database,
                            create_store_in_database,
                            create_store_mtm_workers,
                            create_order_in_database,
                            get_order_from_database):
    worker_data1 = {
        "id": 1,
        "name": "Serega",
        "phone": "123",
    }
    worker_data2 = {
        "id": 2,
        "name": "Maks",
        "phone": "456",
    }
    for worker_data in [worker_data1, worker_data2]:
        await create_worker_in_database(**worker_data)

    store_data1 = {
        "id": 1,
        "name": "Magnit",
    }
    store_data2 = {
        "id": 2,
        "name": "Digital",
    }
    for store_data in [store_data1, store_data2]:
        await create_store_in_database(**store_data)

    link_1 = {
        "id": 1,
        "stores_id": 1,
        "workers_id": 1,
    }
    link_2 = {
        "id": 2,
        "stores_id": 2,
        "workers_id": 2,
    }
    for link_data in [link_1, link_2]:
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

    order_data_updated = {
        "store_id": 2,
        "executor_id": 2
    }

    resp = client.patch(
        "/orders/?customer_phone=321&order_id=1",
        content=json.dumps(order_data_updated))
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["id"] == order_data["id"]
    orders_from_db = await get_order_from_database(order_data["id"])
    order_from_db = dict(orders_from_db[0])
    assert order_from_db["end_time"] == datetime.datetime(
        2024, 5, 6, 21, 0,
        tzinfo=datetime.timezone.utc)
    assert order_from_db["store_id"] == order_data_updated["store_id"]
    assert order_from_db["executor_id"] == order_data_updated["executor_id"]
    assert order_from_db["author_id"] == customer_data["id"]
    assert order_from_db["status"] == "started"
