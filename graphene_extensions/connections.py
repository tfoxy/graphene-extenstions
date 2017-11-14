from typing import Type

from graphene.relay import Connection, ConnectionField

from django.db.models import Manager, Model, QuerySet


def resolve_queryset(model: Type[Model]) -> QuerySet:
    manager: Type[Manager] = model._default_manager
    return manager.get_queryset()


class ModelConnectionField(ConnectionField):
    @classmethod
    def resolve_connection(cls, connection_type, args, resolved):
        if not resolved:
            model: Type[Model] = connection_type._meta.node._meta.model
            resolved = resolve_queryset(model)
        return super().resolve_connection(connection_type, args, resolved)

    @property
    def type(self) -> Type[Connection]:
        return self._type._meta.connection
