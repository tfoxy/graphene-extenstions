import pytest
from django.db import models

from graphene_extensions.types import ModelObjectType
from graphene_extensions.types.registry import ModelRegistry


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
