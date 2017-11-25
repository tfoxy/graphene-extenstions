import inspect
from typing import Type, Dict, Callable, Any

import graphene
from django.contrib.postgres import fields
from django.db import models
from graphene.types.base import BaseType
from graphene.types.mountedtype import MountedType

from graphene_extensions.connections import ModelConnectionField
from graphene_extensions.utils.singleton import Singleton


class ModelRegistry(metaclass=Singleton):
    registry: Dict[Type[models.Model], Type[graphene.ObjectType]] = {}

    def register(self, model: Type[models.Model], model_type: Type[graphene.ObjectType]) -> None:
        assert issubclass(model, models.Model)
        assert issubclass(model_type, graphene.ObjectType)
        self.registry[model] = model_type

    def get(self, model: Type[models.Model]) -> Type[graphene.ObjectType]:
        if model not in self.registry:
            raise RuntimeError(f'{model} has no registered ModelObjectType')
        return self.registry[model]

    def clear(self) -> None:
        self.registry = {}


class TypeRegistry(metaclass=Singleton):
    registry: Dict[Type, BaseType] = {}

    related_fields = {models.ManyToManyField}

    def register(self, _type: Type, graphene_type: Type[BaseType]) -> None:
        assert issubclass(graphene_type, BaseType)
        self.registry[_type] = graphene_type

    def get(self, name: str, field: Any) -> MountedType:
        if isinstance(field, models.Field):
            return self.get_model_type(field)
        if isinstance(field, property):
            assert hasattr(field, '_graphene_type'), \
                f'{name}: decorate property with @annotate_type or use @graphene_property'
            return graphene.Field(type=field._graphene_type)
        if inspect.isfunction(field):
            assert hasattr(field, '_graphene_type'), \
                f'{name}: decorate method with @annotate_type to determine graphene type'
            return graphene.Field(type=field._graphene_type)
        raise NotImplementedError(f'{name}: field conversion for type {field.__class__.__name__} are not supported')

    def get_model_type(self, field: models.Field) -> MountedType:
        field_type = field.__class__
        if field_type in self.related_fields:
            return self.get_related_model_type(field)
        if field_type not in self.registry:
            raise NotImplementedError(f'{field_type} field conversion is not implemented')
        return graphene.Field(type=self.registry[field_type])

    def clear(self) -> None:
        self.registry = {}

    @classmethod
    def get_related_model_type(cls, field: models.Field) -> graphene.Dynamic:
        model = field.related_model
        return graphene.Dynamic(cls.get_field_resolver(model))

    @classmethod
    def get_field_resolver(cls, model: Type[models.Model]) -> Callable:
        def lazy_type():
            model_type = ModelRegistry().get(model)
            return ModelConnectionField(model_type)

        return lazy_type


def register(_type: Type, graphene_type: Type[BaseType]) -> None:
    TypeRegistry().register(_type, graphene_type)


register(models.AutoField, graphene.ID)
register(models.IntegerField, graphene.Int)
register(models.PositiveIntegerField, graphene.Int)
register(models.SmallIntegerField, graphene.Int)
register(models.PositiveSmallIntegerField, graphene.Int)
register(models.BigIntegerField, graphene.Int)
register(models.FloatField, graphene.Float)

register(models.CharField, graphene.String)
register(models.TextField, graphene.String)
register(models.FileField, graphene.String)

register(fields.JSONField, graphene.JSONString)
