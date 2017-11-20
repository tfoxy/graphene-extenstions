from typing import Type

from graphene.relay import Connection, ConnectionField

from django.db.models import Manager, Model, QuerySet


class ModelConnectionField(ConnectionField):
    @classmethod
    def resolve_connection(cls, connection_type, args, resolved):
        if isinstance(resolved, Manager):
            resolved = resolved.get_queryset()
        else:
            model: Type[Model] = connection_type._meta.node._meta.model
            resolved = cls.get_initial_queryset(model)
        return super().resolve_connection(connection_type, args, resolved)

    @property
    def type(self) -> Type[Connection]:
        return self._type._meta.connection

    @classmethod
    def get_initial_queryset(cls, model: Type[Model]) -> QuerySet:
        manager: Type[Manager] = model._default_manager
        return manager.get_queryset()
