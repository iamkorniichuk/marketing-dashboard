import pandas as pd


class GoogleAdsPandas:
    def merge_keyword_solo_partners_dataframes(
        self,
        solo_dataframe,
        partners_dataframe,
        region_ids=None,
        date=None,
    ) -> pd.DataFrame:
        dataframe = solo_dataframe.merge(
            partners_dataframe, on="keyword", suffixes=("", "_partners")
        )

        if region_ids is not None:
            dataframe["region_ids"] = [region_ids for i in dataframe.index]

        if date is not None:
            dataframe["date"] = self.format_date(date)

        return dataframe
