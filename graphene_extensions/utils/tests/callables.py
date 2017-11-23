from ..callables import get_property_names, get_method_names


def test_property_names():
    class Foo:
        @property
        def bar(self) -> str:
            return 'bar'

        @property
        def baz(self) -> int:
            return 42

    assert get_property_names(Foo) == {'bar', 'baz'}


def test_method_names():
    class Foo:
        def bar(self) -> str:
            return 'bar'

        def baz(self) -> int:
            return 42

    assert get_method_names(Foo) == {'bar', 'baz'}
