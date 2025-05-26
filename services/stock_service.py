import pandas as pd
from core.exceptions import DataLoadError
from data.api.yahoo_loader import YahooFinanceLoader


class StockService:
    """Service for loading stock market data."""

    def __init__(self, period: str = "1y"):
        self.loader = YahooFinanceLoader()
        self.period = period

    # def load_stocks(self, tickers: list[str]) -> dict[str, pd.Series]:
    #     all_data = self.loader.load(tickers, self.period)

    #     if isinstance(all_data, dict):
    #         result = {}
    #         for ticker, df in all_data.items():
    #             if "Close" not in df.columns:
    #                 raise DataLoadError(f"'Close' column missing for {ticker}")
    #             result[ticker.upper()] = df["Close"]
    #         return result

    #     ticker = tickers[0].upper()
    #     if "Close" not in all_data.columns:
    #         raise DataLoadError(f"'Close' column missing for ticker {ticker}")
    #     return {ticker: all_data["Close"]}

    def load_stocks(self, tickers: list[str]) -> dict[str, pd.Series]:
        """Load info about stocks using YahooFinanceLoader"""
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
