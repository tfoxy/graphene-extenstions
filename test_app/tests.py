from typing import List

import pytest

from graphene.test import Client

from .models import PandorasBox
from .schema import schema


@pytest.mark.django_db
def test_setup(pizzas):
    response = Client(schema=schema).execute('''
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


def test_number_conversion(pandoras_box_schema, pandoras_box: PandorasBox):
    field_names = [f.name for f in pandoras_box._meta.fields]  # type: List[str]
    response = Client(pandoras_box_schema).execute(
        'query {'
        '  pandoras_box {'
        f'    {", ".join(field_names)}'
        '  }'
        '}'
    )
    assert 'errors' not in response, response['errors']
    data: dict = response['data']['pandoras_box']
    for field, value in data.items():
        assert getattr(pandoras_box, field) == value
