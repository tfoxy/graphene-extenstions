import graphene
from graphene import relay

from graphene_extensions.types import ModelType
from graphene_extensions.connections import ModelConnectionField

from .models import Pizza, Topping


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


schema = graphene.Schema(query=Query)
