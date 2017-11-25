import pytest

import graphene

from ..decorators import annotate_type, graphene_property


def test_type_annotation_validation():
    with pytest.raises(AssertionError):
        class Foo:
            @annotate_type(str)
            def bar(self) -> str:
                return 'bar'


def test_type_annotation():
    class Foo:
        @annotate_type(graphene.String)
        def bar(self) -> str:
            return 'bar'

        @annotate_type(graphene.String)
        @property
        def baz(self) -> str:
            return 'baz'

        @graphene_property(graphene.Int)
        def bazaz(self) -> int:
            return 42

    assert issubclass(Foo.bar._graphene_type, graphene.String)
    assert Foo.baz._graphene_type == graphene.String
    assert Foo.bazaz._graphene_type == graphene.Int

    assert Foo().bar() == 'bar'
    assert Foo().baz == 'baz'
    assert Foo().bazaz == 42
