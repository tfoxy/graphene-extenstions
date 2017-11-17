import pytest

from .models import PizzaType, Pizza


@pytest.fixture(scope='session')
def pizza_types():
    print('create types')
    return (
        PizzaType.objects.create(name='regular'),
        PizzaType.objects.create(name='vegetarian'),
        PizzaType.objects.create(name='hipster'),
    )


@pytest.fixture(scope='session')
def pizzas(pizza_types):
    regular, vegetarian, hipster = pizza_types
    print('create pizzas')
    return (
        Pizza.objects.create(name='margarita', type=vegetarian),
        Pizza.objects.create(name='pepperoni', type=regular),
        Pizza.objects.create(name='ananas', type=hipster),
        Pizza.objects.create(name='american', type=regular),
        Pizza.objects.create(name='meat', type=regular),
    )
