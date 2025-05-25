import pandas as pd
from core.exceptions import DataLoadError
from data.api.yahoo_loader import YahooFinanceLoader


class CurrencyService:
    """Service for loading and validating currency exchange rate data."""

    def __init__(self, period: str = "1y"):
        self.loader = YahooFinanceLoader()
        self.period = period

    def load_pairs(self, pairs: list[str]) -> dict[str, pd.Series]:
        result = {}
        for pair in pairs:
            df = self.loader.load(f"{pair}=X", self.period)
            print(f"Loaded data for {pair}:")
            print(df.head())

            if "Close" not in df.columns and not (
                isinstance(df.columns, pd.MultiIndex)
                and "Close" in df.columns.get_level_values(1)
            ):
                raise DataLoadError(f"Data for {pair} does not contain 'Close' column")

            if isinstance(df.columns, pd.MultiIndex):
                close = df[("Close", f"{pair}=X")]
            else:
                close = df["Close"]

            if isinstance(close, pd.DataFrame) and close.shape[1] == 1:
                close = close.iloc[:, 0]

            result[pair] = close
        return result
