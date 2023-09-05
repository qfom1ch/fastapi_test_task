import pytest


@pytest.mark.parametrize(
    "phone_worker, status_code, response",
    [
        (
                "123",
                200,
                [
                    {
                        "id": 1,
                        "name": "Magnit"
                    },
                    {
                        "id": 2,
                        "name": "Digital"
                    },
                ]
        ),
        (
                "456",
                200,
                []
        ),
        (
                "wrong_phone",
                401,
                {
                    "detail": "Could not validate credentials"
                }
        ),
    ]
)
async def test_get_store_by_worker_phone(client,
                                         create_worker_in_database,
                                         create_store_in_database,
                                         create_store_mtm_workers,
                                         phone_worker,
                                         status_code,
                                         response):
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
        "workers_id": 1,
    }
    for link_data in [link_1, link_2]:
        await create_store_mtm_workers(**link_data)

    resp = client.get(
        f"/workers/get_stores_by_worker_phone/?worker_phone={phone_worker}")
    assert resp.status_code == status_code
    assert resp.json() == response
