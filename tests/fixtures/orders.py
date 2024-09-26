import pytest


@pytest.fixture
def order(mixer):
    return mixer.blend("app.models.order.Order")

@pytest.fixture
def order_list(mixer):
    return mixer.cycle(5).blend("app.models.order.Order")
