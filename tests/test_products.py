from http import HTTPStatus

import pytest

PRODUCTS_URL = "/products"

def test_create_product_valid_data(client):
    product_data = {
        "name": "test",
        "price": 100,
        "amount_available": 10,
        "description": "test description",
    }
    response = client.post(PRODUCTS_URL, json=product_data)
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при POST-запросе по адресу "
        f"{PRODUCTS_URL} с корректными данными создается новый продукт."
    )
    response_data = response.json()
    for field in product_data:
        assert response_data[field] == product_data[field], (
            "Проверьте, что при POST-запросе по адресу "
            f"{PRODUCTS_URL} с корректными данными создается новый продукт, и "
            f"в ответе присутствует поле {field}."
        )


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("price", -100),
        ("amount_available", -10),
    ]
)
def test_create_product_invalid_data(client, field, invalid_value):
    product_invalid_data = dict(
        name="test",
        field=invalid_value,
        description="test description",
    )
    response = client.post(PRODUCTS_URL, json=product_invalid_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
        "Проверьте, что при POST-запросе по адресу "
        f"{PRODUCTS_URL} с некорректными данными не создается новый продукт."
    )


def test_get_product_by_id(client, product):
    response = client.get(f"{PRODUCTS_URL}/{product.id}")
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при GET-запросе по адресу "
        f"/products/<int:product_id> возвращаются данные"
        f" о конкретном продукте."
    )


def test_get_products_list(client, product_list):
    response = client.get(PRODUCTS_URL)
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при GET-запросе по адресу "
        f"{PRODUCTS_URL} возвращается список продуктов."
    )
    assert len(response.json()) == len(product_list), (
        "Проверьте, что при GET-запросе по адресу "
        f"{PRODUCTS_URL} возвращается весь список существующих продуктов."
    )


def test_update_product(client, product):
    new_product_data = dict(
        name="test",
        price=100,
        amount_available=10,
        description="test description",
    )
    response = client.put(f"{PRODUCTS_URL}{product.id}", json=new_product_data)
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при PUT-запросе по адресу "
        f"{PRODUCTS_URL}{product.id} изменяется информация о продукте."
    )
    response_data = response.json()
    for field in new_product_data:
        assert response_data[field] == new_product_data[field], (
            "Проверьте, что при PUT-запросе по адресу "
            f"{PRODUCTS_URL}/<int:product_id> изменяется информация о продукте, "
            f"и в ответе присутствует поле {field} с измененным значением."
        )


def test_delete_product(client, product):
    response = client.delete(f"/products/{product.id}")
    assert response.status_code == HTTPStatus.OK, (
        "Проверьте, что при DELETE-запросе по адресу "
        f"/products/{product.id} возвращается информация"
        f" об удалённом продукте."
    )
    check_whether_product_exists = client.get(f"/products/{product.id}")
    assert check_whether_product_exists.status_code == HTTPStatus.NOT_FOUND, (
        "Проверьте, что при DELETE-запросе по адресу "
        f"{PRODUCTS_URL}/<int:product_id> продукт удаляется."
    )
