from django.db import models

from ..model_type import ModelType


class MetaFieldsModel(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()


def test_meta_fields():
    class MetaFields(ModelType):
        class Meta:
            model = MetaFieldsModel
            fields = ('field1', 'field2', 'field3')

    assert MetaFields._meta.fields.keys() == {'field1', 'field2', 'field3'}


def test_meta_exclude_fields():
    class MetaFields(ModelType):
        class Meta:
            model = MetaFieldsModel
            exclude_fields = ('pk', 'field3')

    assert MetaFields._meta.fields.keys() == {'id', 'field1', 'field2'}


def test_meta_all_fields():
    class MetaFields(ModelType):
        class Meta:
            model = MetaFieldsModel
            fields = '__all__'

    assert MetaFields._meta.fields.keys() == {'id', 'pk', 'field1', 'field2', 'field3'}


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
