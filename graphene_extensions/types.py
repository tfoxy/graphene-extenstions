from itertools import chain
from typing import Type, Dict
from inspect import isclass

import graphene
from collections import OrderedDict
from graphene import relay
from graphene.types.objecttype import ObjectType, ObjectTypeOptions

from django.db import models

from .registry import ConversionRegistry, ModelRegistry


class ModelObjectTypeOptions(ObjectTypeOptions):
    model: Type[models.Model] = None
    connection: Type[relay.Connection] = None


class ModelObjectType(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(cls, interfaces=(), possible_types=(), default_resolver=None,
                                    _meta=None, model=None, fields=None, **options):
        if not _meta:
            _meta = ModelObjectTypeOptions(cls)
            _meta.model = cls.resolve_model(model)
            _meta.connection = cls.create_connection()
            _meta.fields = cls.resolve_fields(model, fields)
        cls.validate_meta(_meta)
        ModelRegistry().register(model, cls)
        super().__init_subclass_with_meta__(interfaces, possible_types, default_resolver, _meta, **options)

    def resolve_id(self, info):  # used to determine ID field when using relay.Node interface
        return self.pk

    @classmethod
    def create_connection(cls) -> Type[relay.Connection]:
        return relay.Connection.create_type(class_name=f'{cls.__name__}Connection', node=cls)

    @classmethod
    def validate_meta(cls, _meta: ModelObjectTypeOptions):
        # type: (ModelObjectTypeOptions) -> None
        assert isinstance(_meta, ModelObjectTypeOptions), \
            f'class {_meta.__name__} must derive from ModelObjectTypeOptions'

    @classmethod
    def validate_fields(cls, model_fields: dict, fields) -> None:
        message = f'Meta.fields must be either a Tuple/List of model field names or "__all__"'
        if isinstance(fields, (list, tuple)):
            for field in fields:
                assert isinstance(field, str), f'Field name should be of type str, received {field}'
                assert field in model_fields, f'Invalid field "{field}", options are: {tuple(model_fields.keys())}'
        elif isinstance(fields, str):
            assert fields in ('__all__',), message
        else:
            raise AssertionError(message)

    @classmethod
    def get_model_fields(cls, model: (Type[models.Model])) -> Dict[str, models.Field]:
        return {field.name: field for field in chain(model._meta.fields, model._meta.many_to_many)}

    @classmethod
    def resolve_fields(cls, model: Type[models.Model], fields) -> Dict[str, None]:
        resolved_fields = OrderedDict()
        model_fields = cls.get_model_fields(model)
        cls.validate_fields(model_fields, fields)
        if fields == '__all__':
            fields = model_fields.keys()
        for field in fields:
            resolved_fields[field] = cls.get_graphene_type(model_fields[field])
        return resolved_fields

    @classmethod
    def get_graphene_type(cls, field: models.Field) -> graphene.Field:
        return ConversionRegistry().get(field)

    @classmethod
    def resolve_model(cls, model):
        cls.validate_model(model)
        return model

    @classmethod
    def validate_model(cls, model):
        assert isclass(model) and issubclass(model, models.Model), \
            f'Meta.model must be a valid Django Model class, received {model}'
        assert not isinstance(model, models.Model), f'Meta.model must be a Django Model class, not instance'
