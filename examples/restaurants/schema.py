import graphene
from graphene_extensions import ModelListField

from graphene_extensions import ModelType
from graphene_extensions.mutations.model import ModelMutation

from .models import Owner, Restaurant, Pizza, Topping


# Queries
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
    owners = ModelListField(OwnerType)
    restaurants = ModelListField(RestaurantType)
    pizzas = ModelListField(PizzaType)
    toppings = ModelListField(ToppingType)


# Mutations
class CreateRestaurant(ModelMutation):
    class Meta:
        model = Restaurant
        fields = ('name',)

    restaurant = graphene.Field(lambda: RestaurantType)
    errors = graphene.Field(graphene.List(graphene.String))

    @classmethod
    def mutate(cls, root, info, **kwargs):
        return CreateRestaurant(
            restaurant=Restaurant(name=kwargs.pop('name', None)),
            errors=['err', 'whatever'],
        )


class Mutations(graphene.ObjectType):
    create_restaurant = CreateRestaurant.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
