import pandas as pd
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator


class AnalysisService:
    """Service for financial calculations."""

    @staticmethod
    def analyze(data: pd.DataFrame) -> dict:
        """Perform all financial analyses."""
        returns = ReturnsCalculator().calculate(data["Close"])
        return {
            "returns": returns,
            "volatility": VolatilityCalculator().calculate(returns),
        }

    @staticmethod
    def analyze_multiple(data_dict: dict[str, pd.Series]) -> dict[str, dict]:
        """Analysis for several series."""
        results = {}
        for pair, series in data_dict.items():
            returns = ReturnsCalculator().calculate(series)
            volatility = VolatilityCalculator().calculate(returns)
            results[pair] = {"returns": returns, "volatility": volatility}
        return results
