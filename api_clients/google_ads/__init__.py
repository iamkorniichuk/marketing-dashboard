from .builder import GoogleAdsBuilder
from .configer import GoogleAdsConfiger
from .formatter import GoogleAdsFormatter
from .keyword_client import GoogleAdsKeywordClient
from .pandas import GoogleAdsPandas


class GoogleAdsApiClient(
    GoogleAdsBuilder,
    GoogleAdsConfiger,
    GoogleAdsFormatter,
    GoogleAdsKeywordClient,
    GoogleAdsPandas,
):
    pass
