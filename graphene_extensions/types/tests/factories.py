import graphene

from ..factories import CallableScalarFactory


def test_callable_factory():
    callable_string = CallableScalarFactory().get(graphene.String)

    assert issubclass(callable_string, graphene.String)
    assert callable_string.__name__ == 'CallableString'
    assert callable_string.serialize(lambda: 'string') == 'string'
