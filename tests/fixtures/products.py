import pytest

@pytest.fixture
def product(mixer):
    return mixer.blend("app.models.product.Product")

@pytest.fixture
def product_list(mixer):
    return mixer.cycle(5).blend("app.models.product.Product")

@pytest.fixture
def product_with_certain_stock(mixer):
    return mixer.blend("app.models.product.Product", amount_available=10)
