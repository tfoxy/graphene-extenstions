import pytest
from random import randint

import graphene
from graphene_extensions.types import ModelObjectType

from .models import PizzaType, Pizza, PandorasBox


@pytest.fixture(scope='session')
def pizza_types():
    return (
        PizzaType.objects.create(name='regular'),
        PizzaType.objects.create(name='vegetarian'),
        PizzaType.objects.create(name='hipster'),
    )


@pytest.fixture(scope='session')
def pizzas(pizza_types):
    regular, vegetarian, hipster = pizza_types
    return (
        Pizza.objects.create(name='margarita', type=vegetarian),
        Pizza.objects.create(name='pepperoni', type=regular),
        Pizza.objects.create(name='ananas', type=hipster),
        Pizza.objects.create(name='american', type=regular),
        Pizza.objects.create(name='meat', type=regular),
    )


@pytest.fixture(scope='session')
def pandoras_box():
    return PandorasBox(
        int=randint(-2 ** 31 + 1, 2 ** 31),
        small_int=randint(-2 ** 16 + 1, 2 ** 16),
    )


@pytest.fixture(scope='session')
def pandoras_box_schema(pandoras_box):
    class PandorasBoxObject(ModelObjectType):
        class Meta:
            model = PandorasBox
            fields = '__all__'

    class Query(graphene.ObjectType):
        pandoras_box = graphene.Field(PandorasBoxObject)

        def resolve_pandoras_box(self, info):
            return pandoras_box

    return graphene.Schema(query=Query, auto_camelcase=False)
