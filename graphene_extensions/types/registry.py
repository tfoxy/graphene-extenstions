import inspect
from typing import Type, Dict, Callable, Any

import graphene
from django.contrib.postgres import fields
from django.db import models
from graphene.types.base import BaseType
from graphene.types.mountedtype import MountedType

from graphene_extensions.connections import ModelConnectionField
from graphene_extensions.types.decorators import GrapheneProperty
from graphene_extensions.utils.singleton import Singleton


class ModelRegistry(metaclass=Singleton):
    _registry: Dict[Type[models.Model], Type[graphene.ObjectType]] = {}

    def register(self, model: Type[models.Model], model_type: Type[graphene.ObjectType]) -> None:
        assert issubclass(model, models.Model)
        assert issubclass(model_type, graphene.ObjectType)
        self._registry[model] = model_type

    def get(self, model: Type[models.Model]) -> Type[graphene.ObjectType]:
        if model not in self._registry:
            raise RuntimeError(f'{model} has no registered ModelObjectType')
        return self._registry[model]

    def clear(self) -> None:
        self._registry = {}


class ConversionRegistry(metaclass=Singleton):
    _registry: Dict[Type, BaseType] = {}

    _related_fields = {models.ManyToManyField}

    def register(self, _type: Type, graphene_type: Type[BaseType]) -> None:
        assert issubclass(graphene_type, BaseType)
        self._registry[_type] = graphene_type

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
        type_ = field.__class__
        if type_ in self._related_fields:
            return self.get_related_model_type(field)
        if type_ not in self._registry:
            raise NotImplementedError(f'{type_} field conversion is not implemented')
        return graphene.Field(type=self._registry[type_])

    def clear(self) -> None:
        self._registry = {}

    @classmethod
    def get_related_model_type(cls, field: models.Field) -> graphene.Dynamic:
        model = field.related_model
        return graphene.Dynamic(cls.get_field_resolver(model))

    @classmethod
    def get_field_resolver(cls, model: Type[models.Model]) -> Callable:
        def lazy_type():
            return ModelConnectionField(ModelRegistry().get(model))
        return lazy_type


def register(_type: Type, graphene_type: Type[BaseType]) -> None:
    ConversionRegistry().register(_type, graphene_type)


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
