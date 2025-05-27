"""
Module providing StockService for loading stock market data
using YahooFinanceLoader and handling various data formats.
"""

import pandas as pd
from core.exceptions import DataLoadError
from data.api.yahoo_loader import YahooFinanceLoader


class StockService:
    """Service for loading stock market data."""

    def __init__(self, period: str = "1y") -> None:
        """
        Initialize StockService with a data loading period.

        Args:
            period: Data period string (e.g., '1y', '6mo').
        """
        self.loader = YahooFinanceLoader()
        self.period = period

    def load_stocks(self, tickers: list[str]) -> dict[str, pd.Series]:
        """
        Load stock price data for given tickers.

        Uses YahooFinanceLoader to fetch data. Supports multiple formats:
        - DataFrame with MultiIndex columns (expects 'Close' price)
        - DataFrame with flat columns
        - Dictionary of DataFrames keyed by ticker symbol

        Args:
            tickers: List of stock ticker symbols.

        Returns:
            Dictionary mapping ticker symbols (uppercase) to their
            closing price pandas Series with NaNs dropped.

        Raises:
            DataLoadError: If the data format is unexpected or required
            'Close' column is missing.
        """
        all_data = self.loader.load(tickers, self.period)

        if isinstance(all_data, pd.DataFrame):
            if isinstance(all_data.columns, pd.MultiIndex):
                if "Close" not in all_data.columns.levels[0]:
                    raise DataLoadError("MultiIndex: 'Close' column not found")

                return {
                    ticker.upper(): all_data["Close"][ticker].dropna()
                    for ticker in all_data["Close"].columns
                }
            else:
                return {
                    ticker.upper(): all_data[ticker].dropna()
                    for ticker in all_data.columns
                }

        if isinstance(all_data, dict):
            result = {}
            for ticker, df in all_data.items():
                if "Close" not in df.columns:
                    raise DataLoadError(f"'Close' column missing for {ticker}")
                result[ticker.upper()] = df["Close"].dropna()
            return result

        raise DataLoadError("Unexpected format from YahooFinanceLoader")
