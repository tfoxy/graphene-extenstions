from ..model_meta import get_fields, get_related_fields, get_model_select, get_model_prefetch, get_model_columns

from graphene_extensions.test_app.models import PizzaType, Pizza, Topping


def test_pizza_type_field_names():
    assert get_fields(PizzaType).keys() == {'id', 'pk', 'name', 'pizza_set'}


def test_pizza_field_names():
    assert get_fields(Pizza).keys() == {'id', 'pk', 'type', 'name', 'toppings'}


def test_topping_field_names():
    assert get_fields(Topping).keys() == {'id', 'pk', 'name', 'pizza_set'}


def test_related_fields():
    assert {field.name for field in get_related_fields(PizzaType)} == {'pizza'}
    assert {field.name for field in get_related_fields(Pizza)} == {'type', 'toppings'}
    assert {field.name for field in get_related_fields(Topping)} == {'pizza'}


def test_model_select():
    assert get_model_select(Pizza) == {'type': PizzaType}


def test_model_prefetch():
    assert get_model_prefetch(Pizza) == {'toppings': Topping, 'type': PizzaType}
    assert get_model_prefetch(PizzaType) == {'pizza_set': Pizza}
    assert get_model_prefetch(Topping) == {'pizza_set': Pizza}


def test_model_columns():
    assert get_model_columns(Pizza) == {'id', 'type_id', 'name'}
    assert get_model_columns(PizzaType) == {'id', 'name'}
    assert get_model_columns(Topping) == {'id', 'name'}
