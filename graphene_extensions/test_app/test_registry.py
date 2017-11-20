import pytest

from django.db import models

from graphene_extensions.registry import ModelRegistry
from graphene_extensions.types import ModelObjectType


def test_model_registry():
    class TestModel(models.Model):
        pass

    with pytest.raises(RuntimeError):
        ModelRegistry().get(TestModel)

    class TestModelType(ModelObjectType):
        class Meta:
            model = TestModel
            fields = '__all__'

    assert ModelRegistry().get(TestModel) == TestModelType
