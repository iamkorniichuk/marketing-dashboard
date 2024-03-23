from typing import Iterable


class GoogleAdsBuilder:
    def build_regions(self, region_ids: Iterable[str]):
        results = []
        for region in region_ids:
            results.append(self.build_one_region(region))

        return results

    def build_one_region(self, region_id: str):
        return self.geo_service.geo_target_constant_path(region_id)

    def build_languages(self, language_ids: Iterable[str]):
        results = []
        for language in language_ids:
            results.append(self.build_one_language(language))

        return results

    def build_one_language(self, language_id: str):
        return self.ads_service.language_constant_path(language_id)
