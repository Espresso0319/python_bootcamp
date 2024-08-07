from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


headers = {"X-Token": "fake-super-secret-token"}
query_params = f"?token=mock-token"


def test_default():
    response = client.get(f"/{query_params}", headers=headers)
    print(response)
    assert response.status_code == 200
    assert response.json() == "ok"


def test_read_item():
    response = client.get(f"/items{query_params}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Get all items", "limit": 10, "skip": 0}


def test_create_item():
    response = client.post(
        f"/items/{query_params}",
        headers=headers,
        json=[{"name": "item1", "price": 10, "on_stack": 0}, {"name": "item 2", "price": 12, "on_stack": 3.0}],
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "create items",
        "items": [{"name": "item1", "on_stack": 0, "price": 10.0}, {"name": "item 2", "on_stack": 3.0, "price": 12}],
    }


def test_update_item():
    response = client.put(
        f"/items/888{query_params}",
        headers=headers,
        json={"updated_item": {"name": "item 1", "price": 21, "on_stack": 22.3}},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Updated item with id 888",
        "updated": {"name": "item 1", "on_stack": 22.3, "price": 21.0},
    }


def test_delete_item():
    response = client.delete(
        f"/items/888{query_params}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Deleted item with id 888",
    }
