import numpy as np
import pandas as pd
from core.exceptions import CalculationError


class VolatilityCalculator:
    """Calculator for price volatility."""
    
    def calculate(self, returns: pd.Series, window: int = 21) -> pd.Series:
        """Calculate rolling volatility.
        
        Args:
            returns: Series of daily returns
            window: Rolling window size in days
            
        Returns:
            pd.Series: Rolling volatility
            
        Raises:
            CalculationError: If calculation fails
        """
        try:
            return returns.rolling(window=window).std() * np.sqrt(window)
        except Exception as e:
            raise CalculationError(f"Volatility calculation error: {str(e)}")