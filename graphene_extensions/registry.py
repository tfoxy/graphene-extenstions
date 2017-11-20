from typing import Type, Dict, Callable
from functools import partial

import graphene
from graphene.types.base import BaseType

from django.db import models
from django.contrib.postgres import fields
from graphene.types.mountedtype import MountedType

from graphene_extensions.connections import ModelConnectionField

from .singleton import Singleton


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
    _registry: Dict[Type, graphene.Field] = {}

    _related_fields = {models.ManyToManyField}

    def register(self, _type: Type, graphene_type: Type[BaseType]) -> None:
        assert issubclass(graphene_type, BaseType)
        self._registry[_type] = graphene.Field(type=graphene_type)

    def get(self, field: models.Field) -> MountedType:
        type_ = field.__class__
        if type_ in self._related_fields:
            return self.get_related_model_type(field)
        if type_ not in self._registry:
            raise NotImplementedError(f'{type_} field conversion is not implemented')
        return self._registry[type_]

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
