import pytest

from graphene.test import Client

from .schema import schema

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCase:
    pytestmark = pytest.mark.django_db

    @classmethod
    def setup_class(cls):
        cls.client = Client(schema=schema)

    def test_setup(self, pizzas):
        response = self.client.execute('''
        query {
          pizzas {
            edges {
              node {
                id
              }
            }
          }
        }
        ''')
        assert len(response['data']['pizzas']['edges']) == len(pizzas)
