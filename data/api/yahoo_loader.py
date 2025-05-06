import yfinance as yf
import pandas as pd
from data.base_loader import BaseDataLoader
from core.exceptions import DataLoadError


class YahooFinanceLoader(BaseDataLoader):
    """Data loader for Yahoo Finance API."""
    
    def load(self, ticker: str, period: str = '1y') -> pd.DataFrame:
        """Load financial data from Yahoo Finance.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            period: Time period to load (1d, 1mo, 1y, etc.)
            
        Returns:
            pd.DataFrame: Loaded market data
            
        Raises:
            DataLoadError: If API request fails
        """
        try:
            data = yf.download(ticker, period=period)
            self._validate_data(data)
            return data
        except Exception as e:
            raise DataLoadError(f"Yahoo Finance error: {str(e)}")