"""
Module for calculating financial price volatility.

Provides functionality to compute rolling volatility from return data,
using a specified rolling window. Raises CalculationError on invalid input
or calculation errors.
"""

import numpy as np
import pandas as pd
from core.exceptions import CalculationError


class VolatilityCalculator:
    """Calculator for price volatility."""

    def calculate(self, returns: pd.Series, window: int = 21) -> pd.Series:
        """
        Calculate rolling volatility over a specified window.

        Args:
            returns (pd.Series): Series of daily returns.
            window (int, optional): Rolling window size in days. Defaults to 21.

        Returns:
            pd.Series: Rolling volatility series.

        Raises:
            CalculationError: If calculation fails due to invalid input or computation error.
        """
        try:
            return returns.rolling(window=window).std() * np.sqrt(window)
        except Exception as e:
            raise CalculationError(f"Volatility calculation error: {str(e)}")
