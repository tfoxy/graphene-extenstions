import graphene
from graphene_extensions.fields.connections import ModelConnectionField

from graphene_extensions import ModelType

from .models import Owner, Restaurant, Pizza, Topping


class OwnerType(ModelType):
    class Meta:
        model = Owner
        fields = '__all__'


class RestaurantType(ModelType):
    class Meta:
        model = Restaurant
        fields = '__all__'


class PizzaType(ModelType):
    class Meta:
        model = Pizza
        fields = '__all__'


class ToppingType(ModelType):
    class Meta:
        model = Topping
        fields = '__all__'


class Query(graphene.ObjectType):
    owners = ModelConnectionField(OwnerType)
    restaurants = ModelConnectionField(RestaurantType)
    pizzas = ModelConnectionField(PizzaType)
    toppings = ModelConnectionField(ToppingType)


schema = graphene.Schema(query=Query)
