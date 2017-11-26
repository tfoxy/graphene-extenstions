import graphene
import pytest

from django.db import models

from .. import ModelType
from ..registry import TypeRegistry, ModelRegistry


def test_model_registry():
    class TestModel(models.Model):
        pass

    with pytest.raises(RuntimeError):
        ModelRegistry().get(TestModel)

    class TestModelType(ModelType):
        class Meta:
            model = TestModel
            fields = '__all__'

    assert ModelRegistry().get(TestModel) == TestModelType


def test_number_conversion():
    assert TypeRegistry().get(models.SmallIntegerField())._type == graphene.Int
    assert TypeRegistry().get(models.PositiveSmallIntegerField())._type == graphene.Int
    assert TypeRegistry().get(models.IntegerField())._type == graphene.Int
    assert TypeRegistry().get(models.PositiveIntegerField())._type == graphene.Int
    assert TypeRegistry().get(models.BigIntegerField())._type == graphene.Int
    assert TypeRegistry().get(models.FloatField())._type == graphene.Float


def test_id_conversion():
    assert TypeRegistry().get(models.AutoField())._type == graphene.ID


def test_text_conversion():
    assert TypeRegistry().get(models.CharField())._type == graphene.String
    assert TypeRegistry().get(models.TextField())._type == graphene.String
    assert TypeRegistry().get(models.EmailField())._type == graphene.String


def test_datetime_conversion():
    assert TypeRegistry().get(models.DateField())._type == graphene.String
    assert TypeRegistry().get(models.DateTimeField())._type == graphene.String
