import pytest

import graphene
from graphene.test import Client

from .models import PizzaType, Pizza, Topping


@pytest.mark.django_db
def test_nested_query(pizza_schema: graphene.Schema):
    assert not Pizza.objects.exists()
    query = '''
    query {
      pizzas {
        edges {
          node {
            toppings {
              edges {
                node {
                  name
                }
              }
            }
          }
        }
      }
    }
    '''
    pizza = Pizza.objects.create(type=PizzaType.objects.create())
    pizza.toppings.set([
        Topping.objects.create(name='mushrooms'),
        Topping.objects.create(name='salami'),
        Topping.objects.create(name='mozzarella'),
    ])

    response = Client(pizza_schema).execute(query)
    assert 'errors' not in response and 'data' in response, response
    pizzas = response['data']['pizzas']['edges']
    assert len(pizzas) == 1
    toppings = pizzas[0]['node']['toppings']['edges']
    assert len(toppings) == 3
    assert {t['node']['name'] for t in toppings} == {'mushrooms', 'salami', 'mozzarella'}
