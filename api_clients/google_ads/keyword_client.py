from typing import Iterable
from datetime import datetime
import pandas as pd

from .utils import safe_google_request


class GoogleAdsKeywordClient:
    def get_keyword_level(self, is_partners_included: bool):
        if is_partners_included:
            result = (
                self.api_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
            )
        else:
            result = self.api_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        return result

    def request_historical_keywords_metrics(
        self, keywords: Iterable[str], region_ids: Iterable[str]
    ):
        solo_response = self.request_one_level_historical_keywords_metrics(
            keywords,
            region_ids,
            is_partners_included=False,
        )
        partners_response = self.request_one_level_historical_keywords_metrics(
            keywords,
            region_ids,
            is_partners_included=True,
        )
        solo_dataframe = pd.DataFrame(solo_response)
        partners_dataframe = pd.DataFrame(partners_response)

        dataframe = self.merge_keyword_solo_partners_dataframes(
            solo_dataframe,
            partners_dataframe,
            region_ids,
        )
        return dataframe.to_dict("records")

    @safe_google_request
    def request_one_level_historical_keywords_metrics(
        self,
        keywords: Iterable[str],
        region_ids: Iterable[str],
        is_partners_included: bool,
    ):
        request = self.api_client.get_type("GenerateKeywordHistoricalMetricsRequest")
        request.historical_metrics_options.include_average_cpc = True
        request.customer_id = self.request_config["customer_id"]
        request.language = self.build_one_language(self.request_config["language_id"])
        request.geo_target_constants.extend(self.build_regions(region_ids))
        request.include_adult_keywords = self.request_config["include_adult_keywords"]
        request.keyword_plan_network = self.get_keyword_level(is_partners_included)
        request.keywords.extend(keywords)

        response = self.keyword_service.generate_keyword_historical_metrics(
            request=request
        )

        data = [
            {
                "keyword": element.text,
                "avg_month_search": element.keyword_metrics.avg_monthly_searches,
                "avg_cpc": self.format_micros(
                    element.keyword_metrics.average_cpc_micros
                ),
                "low_page_bid": self.format_micros(
                    element.keyword_metrics.low_top_of_page_bid_micros
                ),
                "high_page_bid": self.format_micros(
                    element.keyword_metrics.high_top_of_page_bid_micros
                ),
            }
            for element in response.results
        ]
        return data

    def request_forecast_keywords_metrics(
        self,
        keywords: Iterable[str],
        region_ids: Iterable[str],
        start_date: datetime,
        end_date: datetime,
    ):
        solo_responses = []
        partners_responses = []
        for text in keywords:
            solo_responses.append(
                self.request_one_level_forecast_keywords_metrics(
                    text,
                    region_ids,
                    start_date,
                    end_date,
                    is_partners_included=False,
                )
            )
            partners_responses.append(
                self.request_one_level_forecast_keywords_metrics(
                    text,
                    region_ids,
                    start_date,
                    end_date,
                    is_partners_included=True,
                )
            )

        solo_dataframe = pd.DataFrame(solo_responses)
        partners_dataframe = pd.DataFrame(partners_responses)
        dataframe = self.merge_keyword_solo_partners_dataframes(
            solo_dataframe,
            partners_dataframe,
            region_ids,
        )

        dataframe["start_date"] = self.format_date(start_date)
        dataframe["end_date"] = self.format_date(end_date)

        return dataframe.to_dict("records")

    @safe_google_request
    def request_one_level_forecast_keywords_metrics(
        self,
        keyword: str,
        region_ids: Iterable[str],
        start_date: datetime,
        end_date: datetime,
        is_partners_included: bool,
    ):
        campaign = self.api_client.get_type("CampaignToForecast")
        campaign.language_constants.append(
            self.build_one_language(self.request_config["language_id"])
        )
        campaign.keyword_plan_network = self.get_keyword_level(is_partners_included)
        campaign.bidding_strategy.maximize_clicks_bidding_strategy.daily_target_spend_micros = (
            self.request_config["dollars_per_day"] * self.micros_multiplier
        )

        bid_modifiers = []
        for region in region_ids:
            modifier = self.api_client.get_type("CriterionBidModifier")
            modifier.geo_target_constant = self.build_one_region(region)
            bid_modifiers.append(modifier)

        campaign.geo_modifiers.extend(bid_modifiers)

        ad_group = self.api_client.get_type("ForecastAdGroup")

        bid_keyword = self.api_client.get_type("BiddableKeyword")
        bid_keyword.keyword.text = keyword
        bid_keyword.keyword.match_type = (
            self.api_client.enums.KeywordMatchTypeEnum.EXACT
        )

        ad_group.biddable_keywords.append(bid_keyword)
        campaign.ad_groups.append(ad_group)

        request = self.api_client.get_type("GenerateKeywordForecastMetricsRequest")
        request.customer_id = self.request_config["customer_id"]
        request.forecast_period.start_date = self.format_date(start_date)
        request.forecast_period.end_date = self.format_date(end_date)
        request.campaign.CopyFrom(campaign)

        response = self.keyword_service.generate_keyword_forecast_metrics(
            request=request
        )

        metrics = response.campaign_forecast_metrics
        data = {
            "keyword": keyword,
            "impressions": self.format_float(metrics.impressions),
            "ctr": self.format_rate(metrics.click_through_rate),
            "avg_cpc": self.format_micros(metrics.average_cpc_micros),
            "clicks": self.format_float(metrics.clicks),
            "cost": self.format_micros(metrics.cost_micros),
            "conversions": self.format_float(metrics.conversions),
            "conversion_rate": self.format_rate(metrics.conversion_rate),
            "avg_cpa": self.format_micros(metrics.average_cpa_micros),
        }
        return data
