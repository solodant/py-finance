"""
Module providing CurrencyService for loading and validating currency exchange rate data.

This service uses YahooFinanceLoader to fetch currency pair data and ensures
that the 'Close' price column is present for further analysis.
"""

import pandas as pd
from core.exceptions import DataLoadError
from data.api.yahoo_loader import YahooFinanceLoader


class CurrencyService:
    """
    Service for loading and validating currency exchange rate data.

    Attributes:
        loader (YahooFinanceLoader): Loader instance for fetching data.
        period (str): Data retrieval period (e.g., '1y', '6mo').
    """

    def __init__(self, period: str = "1y") -> None:
        """
        Initialize CurrencyService with an optional period.

        Args:
            period (str): The time period for data retrieval (default is '1y').
        """
        self.loader = YahooFinanceLoader()
        self.period = period

    def load_pairs(self, pairs: list[str]) -> dict[str, pd.Series]:
        """
        Load currency exchange rate data for specified currency pairs.

        Args:
            pairs (list[str]): List of currency pair symbols (e.g., ['USDRUB']).

        Returns:
            dict[str, pd.Series]: Dictionary mapping each currency pair symbol
                to its 'Close' price series.

        Raises:
            DataLoadError: If 'Close' column is missing in the loaded data.
        """
        result: dict[str, pd.Series] = {}
        for pair in pairs:
            df = self.loader.load(f"{pair}=X", self.period)
            print(f"Loaded data for {pair}:")
            print(df.head())

            if "Close" not in df.columns and not (
                isinstance(df.columns, pd.MultiIndex)
                and "Close" in df.columns.get_level_values(0)
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
