import pandas as pd
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator

class AnalysisService:
    """Service for financial calculations."""
    
    @staticmethod
    def analyze(data: pd.DataFrame) -> dict:
        """Perform all financial analyses."""
        returns = ReturnsCalculator().calculate(data['Close'])
        return {
            'returns': returns,
            'volatility': VolatilityCalculator().calculate(returns)
        }