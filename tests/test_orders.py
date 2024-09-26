from http import HTTPStatus

ORDER_URL = "/orders"

def test_get_order_by_id(client, order):
    response = client.get(f"{ORDER_URL}/{order.id}")
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при GET-запросе по адресу "
        "/orders/<int:order_id> возвращаются данные о конкретном заказе."
    )
    order_data = response.json()
    assert all(
        field in order_data
        for field in ("id", "created_at", "status", "order_items")
    ), (
        "Проверьте, что при GET-запросе по адресу "
        "/orders/<int:order_id> возвращаются все необходимые поля."
    )


def test_get_orders_list(client, order_list):
    response = client.get(ORDER_URL)
    assert response.status_code == HTTPStatus.OK    , (
        "Проверьте, что при GET-запросе по адресу "
        "/orders возвращается список заказов."
    )
    orders_data = response.json()
    assert isinstance(orders_data, list), (
        "Проверьте, что при GET-запросе по адресу "
        "/orders возвращается список заказов."
    )
    assert len(orders_data) == len(order_list), (
        "Проверьте, что при GET-запросе по адресу "
        "/orders возвращается весь список существующих заказов."
    )


def test_create_order_valid_data(client, product_with_certain_stock):
    valid_order_data = {
        "status": "in_process",
        "order_items": [
            {
                "product_id": 1,
                "quantity": 5
            }
        ]
    }
    response = client.post(ORDER_URL, json=valid_order_data)
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при POST-запросе по адресу "
        "/orders успешно создается новый заказ."
    )
    assert product_with_certain_stock.amount_available == 5, (
        "Проверьте, что при успешном создании заказа у продукта, "
        "добавленного в заказ, отнимается запрашиваемое количество единиц "
        "товара на складе."
    )

def test_create_order_multiple_order_items_of_same_product(
    client, product_with_certain_stock
):
    valid_order_data = {
        "status": "in_process",
        "order_items": [
            {
                "product_id": 1,
                "quantity": 5
            },
            {
                "product_id": 1,
                "quantity": 5
            }
        ]
    }
    response = client.post(ORDER_URL, json=valid_order_data)
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при POST-запросе по адресу "
        f"{ORDER_URL} при наличии нескольких продуктов"
        f" успешно создается новый заказ."
    )
    assert product_with_certain_stock.amount_available == 0, (
        "Проверьте, что при успешном создании заказа у продукта, "
        "добавленного в заказ несколько раз, отнимается общее запрашиваемое"
        " количество единиц товара на складе."
    )

def test_create_order_insufficient_stock(client, product_with_certain_stock):
    invalid_order_data = {
        "status": "in_process",
        "order_items": [
            {
                "product_id": 1,
                "quantity": 100
            }
        ]
    }
    response = client.post(ORDER_URL, json=invalid_order_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        "Проверьте, что при POST-запросе по адресу "
        f"{ORDER_URL} при отсутствии запрашиваемого количества товара"
        f" на складе возвращается код 400."
    )
    assert product_with_certain_stock.amount_available == 10, (
        "Проверьте, что при неуспешном создании заказа у товара не"
        " отнимается запрашиваемое количество единиц товара на складе."
    )


def test_change_order_status_valid_data(client, order):
    response = client.patch(f"/orders/{order.id}/status",
                            params={"status": "delivered"})
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при PATCH-запросе по адресу "
        "/orders/<int:order_id>/status изменяется статус заказа."
    )


def test_change_order_status_invalid_data(client, order):
    response = client.patch(f"/orders/{order.id}/status",
                            params={"status": "invalid"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
        "Проверьте, что при PATCH-запросе по адресу "
        "/orders/<int:order_id>/status с некорректным значением статуса "
        "возвращается код 422."
    )
