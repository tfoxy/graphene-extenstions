from typing import Type, Set, Dict

from django.db.models import Model, Field
from django.db.models.fields.reverse_related import ForeignObjectRel


def get_related_fields(model: Type[Model]) -> Set[Field]:
    return {field for field in model._meta.get_fields() if field.related_model}


def get_relation_name(field: Field) -> str:
    if isinstance(field, ForeignObjectRel):
        return field.related_query_name or field.name + ('_set' if field.multiple else '')
    return field.name


def get_field_names(model: Type[Model]) -> Set[str]:
    return {get_relation_name(field) for field in model._meta.get_fields()}


def is_selectable(field: Field) -> bool:
    return field.many_to_one or field.one_to_one and not field.auto_created


def is_prefetchable(field: Field) -> bool:
    return field.many_to_many or field.one_to_one or field.one_to_many or is_selectable(field)


def get_model_select(model: Type[Model]) -> Dict[str, Model]:
    return {get_relation_name(field): field.related_model
            for field in get_related_fields(model) if is_selectable(field)}


def get_model_prefetch(model: Type[Model]) -> Dict[str, Model]:
    return {get_relation_name(field): field.related_model
            for field in get_related_fields(model) if is_prefetchable(field)}
