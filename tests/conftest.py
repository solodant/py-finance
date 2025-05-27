import pytest
import pandas as pd


@pytest.fixture
def args_empty():
    class Args:
        def __init__(self):
            self.csv = None
            self.excel = None
            self.tickers = None
            self.currencies = None
            self.period = None

    return Args()


@pytest.fixture
def args_csv(tmp_path):
    class Args:
        def __init__(self):
            self.csv = str(tmp_path / "test.csv")
            self.excel = None
            self.tickers = None
            self.currencies = None
            self.period = "1y"

    return Args()


@pytest.fixture
def args_excel(tmp_path):
    class Args:
        def __init__(self):
            self.csv = None
            self.excel = str(tmp_path / "test.xlsx")
            self.tickers = None
            self.currencies = None
            self.period = "1y"

    return Args()


@pytest.fixture
def args_ticker():
    class Args:
        def __init__(self):
            self.csv = None
            self.excel = None
            self.tickers = ["AAPL"]
            self.currencies = None
            self.period = "6mo"

    return Args()


@pytest.fixture
def args_currency():
    class Args:
        def __init__(self):
            self.csv = None
            self.excel = None
            self.tickers = None
            self.currencies = ["USDRUB"]
            self.period = "6mo"

    return Args()


@pytest.fixture
def price_data():
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "Close": [100, 102, 101, 105, 107],
    }
    return pd.DataFrame(data).set_index("Date")


@pytest.fixture
def returns_data(price_data):
    from analysis.returns import ReturnsCalculator

    return ReturnsCalculator().calculate(price_data["Close"])


@pytest.fixture
def dummy_df():
    df = pd.DataFrame(
        {
            "Open": [1.0, 2.0],
            "Close": [1.5, 2.5],
            "Date": pd.date_range("2023-01-01", periods=2),
        }
    ).set_index("Date")
    return df
