import pytest
import pandas as pd

data = {
    'Date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
    'Close': [100, 102, 101, 105, 107]
}

test_df = pd.DataFrame(data).set_index('Date')

@pytest.fixture
def price_data():
    return test_df.copy()

@pytest.fixture
def returns_data(price_data):
    from analysis.returns import ReturnsCalculator
    return ReturnsCalculator().calculate(price_data['Close'])

