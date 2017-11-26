from django.db import models

import graphene

from graphene_extensions.fields.connections import ModelConnectionField
from graphene_extensions.types.model_type import ModelType


def assert_dynamic_type(object_type, field_name, field_type, to_object_type):
    assert field_name in object_type._meta.fields
    field = object_type._meta.fields[field_name]
    assert isinstance(field, graphene.Dynamic)
    assert isinstance(field.type(), field_type)
    assert field.type().type == to_object_type


def test_one_to_one_rel():
    class OneToOneA(models.Model):
        pass

    class OneToOneB(models.Model):
        one_to_one = models.OneToOneField(OneToOneA, related_name='one_to_one')

    class OneToOneAType(ModelType):
        class Meta:
            model = OneToOneA
            fields = '__all__'

    class OneToOneBType(ModelType):
        class Meta:
            model = OneToOneB
            fields = '__all__'

    assert_dynamic_type(OneToOneAType, 'one_to_one', graphene.Field, OneToOneBType)
    assert_dynamic_type(OneToOneBType, 'one_to_one', graphene.Field, OneToOneAType)


def test_foreign_rel():
    class ForeignA(models.Model):
        pass

    class ForeignB(models.Model):
        foreign = models.ForeignKey(ForeignA, related_name='foreigns')

    class ForeignAType(ModelType):
        class Meta:
            model = ForeignA
            fields = '__all__'

    class ForeignBType(ModelType):
        class Meta:
            model = ForeignB
            fields = '__all__'

    assert_dynamic_type(ForeignBType, 'foreign', graphene.Field, ForeignAType)
    assert_dynamic_type(ForeignAType, 'foreigns', ModelConnectionField, ForeignBType._meta.connection)


def test_many_to_many_rel():
    class ManyToManyA(models.Model):
        pass

    class ManyToManyB(models.Model):
        many_to_many = models.ManyToManyField(ManyToManyA, related_name='many_to_many')

    class ManyToManyAType(ModelType):
        class Meta:
            model = ManyToManyA
            fields = '__all__'

    class ManyToManyBType(ModelType):
        class Meta:
            model = ManyToManyB
            fields = '__all__'

    assert_dynamic_type(ManyToManyAType, 'many_to_many', ModelConnectionField, ManyToManyBType._meta.connection)
    assert_dynamic_type(ManyToManyBType, 'many_to_many', ModelConnectionField, ManyToManyAType._meta.connection)
