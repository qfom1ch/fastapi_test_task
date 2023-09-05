import datetime
import json


async def test_create_order(client,
                            create_worker_in_database,
                            create_customer_in_database,
                            create_store_in_database,
                            create_store_mtm_workers,
                            get_order_from_database,
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
        "end_time": "2024-09-02T16:31:59.397245",
        "store_id": 1,
        "executor_id": 1,
    }

    resp = client.post("/orders/?customer_phone=321",
                       content=json.dumps(order_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["end_time"] == order_data["end_time"]
    assert data_from_resp["store_id"] == order_data["store_id"]
    assert data_from_resp["executor_id"] == order_data["executor_id"]
    assert data_from_resp["author_id"] == customer_data["id"]
    assert data_from_resp["status"] == "started"
    order_from_db = await get_order_from_database(data_from_resp["id"])
    assert len(order_from_db) == 1
    order_from_db = dict(order_from_db[0])
    assert order_from_db["end_time"] == datetime.datetime(
        2024, 9, 2, 13, 31,
        59, 397245,
        tzinfo=datetime.timezone.utc)
    assert order_from_db["store_id"] == order_data["store_id"]
    assert order_from_db["executor_id"] == order_data["executor_id"]
    assert order_from_db["author_id"] == customer_data["id"]
    assert order_from_db["status"] == "started"
