"""
Module for calculating financial returns.

Provides functionality to compute daily returns from price data,
including both logarithmic and simple returns. Raises CalculationError
on invalid input or calculation issues.
"""

import numpy as np
import pandas as pd
from core.exceptions import CalculationError


class ReturnsCalculator:
    """Calculator for financial returns."""

    def calculate(self, prices: pd.Series, log_returns: bool = True) -> pd.Series:
        """
        Calculate daily returns from price data.

        Args:
            prices (pd.Series): Series of closing prices.
            log_returns (bool, optional): If True, calculate log returns; otherwise simple returns. Defaults to True.

        Returns:
            pd.Series: Series of daily returns.

        Raises:
            CalculationError: If calculation fails due to invalid input or computation error.
        """
        try:
            if log_returns:
                return np.log(prices / prices.shift(1)).dropna()
            return prices.pct_change().dropna()
        except Exception as e:
            raise CalculationError(f"Returns calculation error: {str(e)}")
