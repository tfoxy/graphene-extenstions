from django import test

from graphene.test import Client

from .models import Pizza, Topping, PizzaType
from .schema import schema


class TestCase(test.TestCase):
    def setUp(self):
        pizza_type = PizzaType.objects.create(name='fuck')
        self.client = Client(schema)
        toppings = [
            Topping.objects.create(name=''),
            Topping.objects.create(name=''),
            Topping.objects.create(name=''),
        ]
        pizza1 = Pizza.objects.create(name='', type=pizza_type)
        pizza1.toppings.set(toppings)
        pizza2 = Pizza.objects.create(name='', type=pizza_type)
        pizza2.toppings.set(toppings)

    def test_query_count(self):
        with self.assertNumQueries(0):
            response = self.client.execute('''
query {
  pizzas {
    edges {
      node {
        toppings {
          edges {
            node {
              id
            }
          }
        }
      }
    }
  }
}
            ''')
