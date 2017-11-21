from typing import Type, List

from django.db.models import Model, QuerySet

from graphene_extensions.utils.model_meta import get_model_prefetch
from graphene_extensions.utils.selectors import Selector


def optimize_queryset(queryset: QuerySet, selectors: Selector) -> QuerySet:
    return queryset.prefetch_related(*get_prefetch(queryset.model, selectors))


def get_prefetch(model: Type[Model], selectors: Selector) -> List[str]:
    prefatchable_fields = get_model_prefetch(model)
    prefetch = []
    for field, selection in selectors.items():
        if selection and field in prefatchable_fields:
            sub_prefetches = get_prefetch(prefatchable_fields[field], selection)
            if sub_prefetches:
                for sub_field in sub_prefetches:
                    prefetch.append(field + '__' + sub_field)
            else:
                prefetch.append(field)
    return prefetch
