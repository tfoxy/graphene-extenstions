from typing import Type

import graphene
from graphene.types.base import BaseType

from django.db import models
from django.contrib.postgres import fields

from .singleton import Singleton


class ConversionRegistry(metaclass=Singleton):
    _registry = {}

    def register(self, _type, graphene_type):
        assert issubclass(graphene_type, BaseType)
        self._registry[_type] = graphene.Field(type=graphene_type)

    def get(self, _type: Type):
        if _type not in self._registry:
            raise NotImplementedError(f'{_type} field conversion is not implemented')
        return self._registry[_type]


def register(_type: Type, graphene_type):
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
