from data.api.yahoo_loader import YahooFinanceLoader
import pandas as pd

SUPPORTED_STOCK_NAMES = []


class StockService:
    """Service for loading stock market data."""

    def __init__(self, period: str = "1y"):
        self.loader = YahooFinanceLoader()
        self.period = period

    def load_stocks(self, tickers: list[str]) -> dict[str, pd.Series]:
        all_data = self.loader.load(tickers, self.period)

        if isinstance(all_data, dict):  
            return {
                ticker.upper(): df['Close']
                for ticker, df in all_data.items()
                if 'Close' in df.columns
            }

        ticker = tickers[0].upper()
        if 'Close' not in all_data.columns:
            raise ValueError(f"'Close' column missing for ticker {ticker}")
        return {ticker: all_data['Close']}
