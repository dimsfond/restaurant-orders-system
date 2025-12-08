import pytest

def test_create_order_success(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 2},
            {"menu_item_id": 2, "quantity": 1} 
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["customer_id"] == 1
    assert data["status"] == "pending"
    expected_total = 2 * 8.5 + 1 * 2.5
    assert abs(data["total"] - expected_total) < 1e-6
    assert isinstance(data["items"], list) and len(data["items"]) == 2

def test_create_order_invalid_quantity(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 0},
            {"menu_item_id": 2, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 400, response.text
    data = response.json()
    assert "Invalid quantity" in data["detail"]

def test_create_order_non_existent_menu_item(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 999, "quantity": 1},
            {"menu_item_id": 2, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Menu Item not found"

def test_patch_order_status_success(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 1}
        ]
    }
    order_response = client.post("/orders/", json = creating_order_payload)
    order_id = order_response.json()["id"]

    payload = {"status": "preparing"}
    response = client.patch(f"/orders/{order_id}/status", json = payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "preparing"

def test_patch_order_status_invalid(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 1}
        ]
    }
    order_response = client.post("/orders/", json = creating_order_payload)
    order_id = order_response.json()["id"]

    payload = {"status": "cooking"}
    response = client.patch(f"/orders/{order_id}/status", json = payload)
    assert response.status_code == 422, response.text
    data = response.json()
    assert "Input should be" in data["detail"][0]["msg"]

def test_get_order_details_success(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 2},
            {"menu_item_id": 2, "quantity": 1}
        ]
    }
    order_response = client.post("/orders/", json=creating_order_payload)
    order_id = order_response.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == 1
    assert data["status"] == "pending"
    expected_total = 2 * 8.5 + 1 * 2.5
    assert abs(data["total"] - expected_total) < 1e-6
    assert isinstance(data["items"], list) and len(data["items"]) == 2

def test_get_order_details_not_found(client):
    response = client.get("/orders/9999")
    assert response.status_code == 404, response.text
    data = response.json()
    assert "Order not found" in data["detail"]

def test_list_order_with_filter_status(client):
    creating_order_payload1 = {
        "customer_id": 1,
        "items": [{"menu_item_id": 1, "quantity": 1}]
    }
    creating_order_payload2 = {
        "customer_id": 1,
        "items": [{"menu_item_id": 2, "quantity": 2}]
    }

    order_response1 = client.post("/orders/", json=creating_order_payload1)
    order1_id = order_response1.json()["id"]
    order_response2 = client.post("/orders/", json=creating_order_payload2)
    order2_id = order_response2.json()["id"]
    client.patch(f"/orders/{order2_id}/status", json={"status": "preparing"})

    #GET all orders
    response_all = client.get("/orders/")
    assert response_all.status_code == 200, response_all.text
    data_all = response_all.json()
    assert len(data_all) >= 2

    #GET orders with status preparing
    response_preparing = client.get("/orders/", params = {"status": "preparing"})
    assert response_preparing.status_code == 200, response_preparing.text
    data_preparing = response_preparing.json()
    assert any(order["id"] == order2_id for order in data_preparing)
    assert all(order["status"] == "preparing" for order in data_preparing)

    #GET orders with status pending
    response_pending = client.get("/orders/", params = {"status": "pending"})
    assert response_pending.status_code == 200, response_pending.text
    data_pending = response_pending.json()
    assert any(order["id"] == order1_id for order in data_pending)
    assert all(order["status"] == "pending" for order in data_pending)

def test_delete_order_success(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [{"menu_item_id": 1, "quantity": 1}]
    }
    order_response = client.post("/orders/", json=creating_order_payload)
    order_id = order_response.json()["id"]

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert f"Order {order_id} has been deleted" in data["detail"]

    order_response = client.get(f"/orders/{order_id}")
    assert order_response.status_code == 404

def test_delete_order_failure(client):
    response = client.delete("/orders/9999")
    assert response.status_code == 404, response.text
    data = response.json()
    assert "Order not found" in data["detail"]