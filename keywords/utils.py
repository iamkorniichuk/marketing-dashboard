from typing import Dict, Tuple

from django.db.models import QuerySet

from keywords.models import Keyword


def extract_regions_groups(
    keywords: QuerySet[Keyword],
) -> Dict[Tuple[str], str]:
    results = {}
    for obj in keywords.all():
        regions = tuple(obj.regions.values_list("id", flat=True))
        try:
            results[regions].append(obj.text)
        except KeyError:
            results[regions] = [obj.text]

    return results
