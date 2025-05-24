import pandas as pd
from data.api.yahoo_loader import YahooFinanceLoader
from core.exceptions import DataLoadError


SUPPORTED_CURRENCY_PAIRS = [
    "USDRUB", "EURRUB", "GBPRUB", "CNYRUB", "JPYRUB",
    "CHFRUB", "AUDRUB", "CADRUB", "HKDRUB", "SGDRUB"
]


class CurrencyService:
    """Service for loading and validating currency exchange rate data."""

    def __init__(self, period: str = "1y"):
        self.loader = YahooFinanceLoader()
        self.period = period

    def validate_pairs(self, pairs: list[str]) -> list[str]:
        """Validate currency pairs against whitelist."""
        valid = []
        invalid = []
        for pair in pairs:
            if pair.upper() in SUPPORTED_CURRENCY_PAIRS:
                valid.append(pair.upper())
            else:
                invalid.append(pair)
        if invalid:
            raise ValueError(f"Unsupported currency pairs: {', '.join(invalid)}")
        return valid

    def load_pairs(self, pairs: list[str]) -> dict[str, pd.Series]:
        valid_pairs = self.validate_pairs(pairs)
        result = {}
        for pair in valid_pairs:
            df = self.loader.load(f"{pair}=X", self.period)
            print(f"Loaded data for {pair}:")
            print(df.head())
            
            if 'Close' not in df.columns and not (isinstance(df.columns, pd.MultiIndex) and 'Close' in df.columns.get_level_values(1)):
                raise DataLoadError(f"Data for {pair} does not contain 'Close' column")
            
            if isinstance(df.columns, pd.MultiIndex):
                close = df[('Close', f"{pair}=X")]
            else:
                close = df['Close']
            
            if isinstance(close, pd.DataFrame) and close.shape[1] == 1:
                close = close.iloc[:, 0]
            
            result[pair] = close
        return result

