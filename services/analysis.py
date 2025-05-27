"""
Module providing the AnalysisService class for financial calculations.

This service performs computations of log returns, percentage returns,
and rolling volatility for single or multiple financial time series.
"""

import pandas as pd
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator


class AnalysisService:
    """
    Service for performing financial calculations such as returns and volatility.

    Provides methods to analyze a single price series or multiple series.
    """

    @staticmethod
    def analyze(data: pd.DataFrame) -> dict[str, pd.Series]:
        """
        Perform financial analysis on a single DataFrame containing price data.

        Calculates returns and volatility based on the 'Close' price column.

        Args:
            data (pd.DataFrame): DataFrame with at least a 'Close' column representing price data.

        Returns:
            dict[str, pd.Series]: Dictionary with keys 'returns' and 'volatility',
                each mapped to a pandas Series of calculated values.
        """
        returns = ReturnsCalculator().calculate(data["Close"])
        volatility = VolatilityCalculator().calculate(returns)
        return {
            "returns": returns,
            "volatility": volatility,
        }

    @staticmethod
    def analyze_multiple(
        data_dict: dict[str, pd.Series]
    ) -> dict[str, dict[str, pd.Series]]:
        """
        Perform financial analysis on multiple price series.

        Args:
            data_dict (dict[str, pd.Series]): Dictionary mapping asset names or pairs
                to pandas Series of price data.

        Returns:
            dict[str, dict[str, pd.Series]]: Nested dictionary where the first key is the asset/pair name,
                and the value is another dictionary with keys 'returns' and 'volatility' mapped to Series.
        """
        results: dict[str, dict[str, pd.Series]] = {}
        for pair, series in data_dict.items():
            returns = ReturnsCalculator().calculate(series)
            volatility = VolatilityCalculator().calculate(returns)
            results[pair] = {"returns": returns, "volatility": volatility}
        return results
