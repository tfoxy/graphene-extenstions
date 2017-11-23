from django.db import models

from ..callables import get_properties, get_methods


def test_property_names():
    class Foo:
        @property
        def bar(self) -> str:
            return 'bar'

        @property
        def baz(self) -> int:
            return 42

    assert get_properties(Foo).keys() == {'bar', 'baz'}
    assert get_properties(Foo, skip=['bar']).keys() == {'baz'}


def test_method_names():
    class Foo:
        def bar(self) -> str:
            return 'bar'

        def baz(self) -> int:
            return 42

    assert get_methods(Foo).keys() == {'bar', 'baz'}


def test_django_model_properties():
    class Foo(models.Model):
        pass

    assert get_properties(Foo).keys() == {'pk'}
    assert get_methods(Foo).keys() == {'clean', 'get_deferred_fields'}
    assert '__str__' in get_methods(Foo, include_magic_functions=True)
    assert not get_methods(Foo, skip=['clean', 'get_deferred_fields']).keys()
