from django.db import models

from ..model_type import ModelType


def test_model_type_pk_auto_field():
    class AutoFieldPK(models.Model):
        pass

    fields = ModelType.get_model_fields(AutoFieldPK)
    assert 'pk' in fields
    assert isinstance(fields['pk'], models.AutoField)


def test_model_type_pk_char_field():
    class CharFieldPK(models.Model):
        uid = models.CharField(primary_key=True, max_length=16)

    fields = ModelType.get_model_fields(CharFieldPK)
    assert fields.keys() == {'uid', 'pk'}
    assert isinstance(fields['pk'], models.CharField)
