from typing import List, Iterable

import pytest
from random import randint

import graphene
from graphene import relay

from graphene_extensions import ModelConnectionField
from graphene_extensions import ModelType

from .models import PizzaType, Pizza, PandorasBox, Topping


@pytest.fixture(scope='session')
def empty_schema():
    class Query(graphene.ObjectType):
        data = graphene.Field(type=graphene.String)

        def resolve_data(self, info) -> str:
            return 'dummy data'
    return graphene.Schema(query=Query)


@pytest.fixture(scope='session')
def toppings() -> List[Topping]:
    return [
        Topping.objects.create(name='mushrooms'),
        Topping.objects.create(name='salami'),
        Topping.objects.create(name='mozzarella'),
    ]


@pytest.fixture(scope='session')
def pizza_types() -> List[PizzaType]:
    return [
        PizzaType.objects.create(name='regular'),
        PizzaType.objects.create(name='vegetarian'),
        PizzaType.objects.create(name='hipster'),
    ]


@pytest.fixture(scope='session')
def pizzas(pizza_types: List[PizzaType], toppings: List[Topping]) -> Iterable[Pizza]:
    regular, vegetarian, hipster = pizza_types
    for pizza in [
        Pizza.objects.create(name='margarita', type=vegetarian),
        Pizza.objects.create(name='pepperoni', type=regular),
        Pizza.objects.create(name='ananas', type=hipster),
        Pizza.objects.create(name='american', type=regular),
        Pizza.objects.create(name='meat', type=regular),
    ]:
        pizza.toppings.set(toppings)
        yield pizza


@pytest.fixture(scope='session')
def pizza_schema() -> graphene.Schema:
    class PizzaObject(ModelType):
        class Meta:
            model = Pizza
            fields = ('name', 'toppings')
            interfaces = (relay.Node,)

    class ToppingObject(ModelType):
        class Meta:
            model = Topping
            fields = ('name',)
            interfaces = (relay.Node,)

    class Query(graphene.ObjectType):
        pizzas = ModelConnectionField(PizzaObject)
        toppings = ModelConnectionField(ToppingObject)

    return graphene.Schema(query=Query)


@pytest.fixture(scope='session')
def pandoras_box() -> PandorasBox:
    return PandorasBox(
        int=randint(-2 ** 31 + 1, 2 ** 31),
        small_int=randint(-2 ** 16 + 1, 2 ** 16),
    )


@pytest.fixture(scope='session')
def pandoras_box_schema(pandoras_box: PandorasBox) -> graphene.Schema:
    class PandorasBoxObject(ModelType):
        class Meta:
            model = PandorasBox
            fields = '__all__'

    class Query(graphene.ObjectType):
        pandoras_box = graphene.Field(PandorasBoxObject)

        def resolve_pandoras_box(self, info):
            return pandoras_box

    return graphene.Schema(query=Query, auto_camelcase=False)
