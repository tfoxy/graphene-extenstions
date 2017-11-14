import graphene
from graphene import relay

from graphene_extensions.types import ModelObjectType
from graphene_extensions.connections import ModelConnectionField

from .models import Pizza, Topping


class PizzaObject(ModelObjectType):
    class Meta:
        model = Pizza
        fields = ('name',)
        interfaces = (relay.Node,)


class ToppingObject(ModelObjectType):
    class Meta:
        model = Topping
        fields = ('name',)
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    pizzas = ModelConnectionField(PizzaObject)
    toppings = ModelConnectionField(ToppingObject)


schema = graphene.Schema(query=Query)
