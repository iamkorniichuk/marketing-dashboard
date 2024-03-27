from typing import Iterable
from django.db.models import QuerySet


def filter_contains_all(queryset: QuerySet, **filters: Iterable) -> QuerySet:
    for field, values in filters.items():
        for item in values:
            kwargs = {field: item}
            queryset = queryset.filter(**kwargs)
    return queryset
