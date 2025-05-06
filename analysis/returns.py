import numpy as np
import pandas as pd
from core.exceptions import CalculationError


class ReturnsCalculator:
    """Calculator for financial returns."""
    
    def calculate(self, prices: pd.Series, log_returns: bool = True) -> pd.Series:
        """Calculate daily returns.
        
        Args:
            prices: Series of closing prices
            log_returns: If True, calculate log returns
            
        Returns:
            pd.Series: Daily returns
            
        Raises:
            CalculationError: If calculation fails
        """
        try:
            if log_returns:
                return np.log(prices / prices.shift(1)).dropna()
            return prices.pct_change().dropna()
        except Exception as e:
            raise CalculationError(f"Returns calculation error: {str(e)}")