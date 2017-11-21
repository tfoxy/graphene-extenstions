from typing import Type, Dict

from django.db.models import Model, QuerySet

from graphene_extensions.utils.selectors import Selector


def optimize_queryset(queryset: QuerySet, selectors: Selector) -> QuerySet:
    return queryset.select_related().prefetch_related()
