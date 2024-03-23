class GoogleAdsFormatter:
    micros_multiplier = 1_000_000

    def format_date(self, date):
        return date.strftime("%Y-%m-%d")

    def format_micros(self, number: str) -> float:
        divided_number = int(number) / self.micros_multiplier
        return round(divided_number, 2)

    def format_rate(self, number) -> float:
        return round(number * 100, 2)

    def format_float(self, number) -> float:
        return round(number * 100, 2)
