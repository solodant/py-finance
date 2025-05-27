import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from core.exceptions import DataLoadError
from services.data_service import DataService
from services.stock_service import StockService
from services.currency_service import CurrencyService
from services.analysis import AnalysisService
from services.visualization import VisualizationService, StockVisualizationService, CurrencyVisualizationService 

def test_load_data_with_no_args(args_empty):
    with pytest.raises(ValueError, match="No valid data source specified."):
        DataService.load_data(args_empty)

def test_load_data_csv_mock(args_csv):
    with patch("data.csv_loader.CSVDataLoader.load", return_value="csv"):
        data, title = DataService.load_data(args_csv)
        assert data == "csv"
        assert title.startswith("CSV")

def test_load_data_csv_explicit_true_path(tmp_path):
    class Args:
        def __init__(self):
            self.csv = str(tmp_path / "file.csv")
            self.excel = None
            self.tickers = None
            self.currencies = None
            self.period = "1y"

    with patch("data.csv_loader.CSVDataLoader.load", return_value="csv"):
        data, title = DataService.load_data(Args())
        assert data == "csv"
        assert "CSV" in title


def test_load_data_excel_mock(args_excel):
    with patch("data.excel_loader.ExcelDataLoader.load", return_value="excel"):
        data, title = DataService.load_data(args_excel)
        assert data == "excel"
        assert title.startswith("Excel")


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_data_ticker_mock(mock_loader, args_ticker):
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "AAPL")])
    df = pd.DataFrame([[100], [101], [102]], index=index, columns=columns)
    mock_loader.return_value = df

    data, title = DataService.load_data(args_ticker)
    assert "AAPL" in data
    assert isinstance(data["AAPL"], pd.Series)
    assert title == "Stocks: AAPL (6mo)"

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_data_currency_mock(mock_loader, args_currency):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_loader.return_value = df

    data, title = DataService.load_data(args_currency)
    assert "USDRUB" in data
    assert isinstance(data["USDRUB"], pd.Series)
    assert title == "Currency Pairs: USDRUB"


def test_analysis_service_analyze():
    df = pd.DataFrame({"Close": [100, 101, 102, 104, 107]})
    result = AnalysisService.analyze(df)
    assert "returns" in result
    assert "volatility" in result


def test_analysis_service_analyze_multiple():
    df = pd.DataFrame({"AAPL": [100, 101, 102], "MSFT": [200, 202, 204]})
    results = AnalysisService.analyze_multiple(df)
    assert set(results.keys()) == {"AAPL", "MSFT"}


def test_visualization(monkeypatch, price_data):
    analysis = AnalysisService.analyze(price_data)
    shown = {}

    def fake_show():
        shown["called"] = True

    monkeypatch.setattr(plt, "show", fake_show)
    VisualizationService.show(price_data["Close"], analysis, "Test")
    assert shown.get("called")


def test_stock_visualization(monkeypatch, price_data):
    analysis = AnalysisService.analyze_multiple(price_data)
    shown = {}
    def fake_show():
        shown["ok"] = True
    monkeypatch.setattr(plt, "show", fake_show)
    StockVisualizationService.show(price_data, analysis)
    assert shown.get("ok")


def test_currency_visualization(monkeypatch, price_data):
    shown = {}
    def fake_show():
        shown["done"] = True
    monkeypatch.setattr(plt, "show", fake_show)
    CurrencyVisualizationService.show(price_data, "Title")
    assert shown.get("done")


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_multiindex_with_close(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "AAPL"), ("Close", "MSFT")])
    df = pd.DataFrame([[100, 200], [101, 201], [102, 202]], index=index, columns=columns)
    mock_load.return_value = df

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_multiindex_missing_close(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Open", "AAPL")])
    df = pd.DataFrame([[100], [101], [102]], index=index, columns=columns)
    mock_load.return_value = df

    service = StockService()
    with pytest.raises(DataLoadError, match="MultiIndex: 'Close' column not found"):
        service.load_stocks(["AAPL"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_flat_columns(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"AAPL": [100, 101, 102], "MSFT": [200, 201, 202]}, index=index)
    mock_load.return_value = df

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_dict_with_close(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df1 = pd.DataFrame({"Close": [100, 101, 102]}, index=index)
    df2 = pd.DataFrame({"Close": [200, 201, 202]}, index=index)
    mock_load.return_value = {"AAPL": df1, "MSFT": df2}

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_dict_missing_close(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Open": [100, 101, 102]}, index=index)
    mock_load.return_value = {"AAPL": df}

    service = StockService()
    with pytest.raises(DataLoadError, match="'Close' column missing for AAPL"):
        service.load_stocks(["AAPL"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_unexpected_format(mock_load):
    mock_load.return_value = None

    service = StockService()
    with pytest.raises(DataLoadError, match="Unexpected format from YahooFinanceLoader"):
        service.load_stocks(["AAPL"])

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_normal_df(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    assert "USDRUB" in result
    assert isinstance(result["USDRUB"], pd.Series)
    assert (result["USDRUB"] == df["Close"]).all()

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_multiindex_df(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "USDRUB=X")])
    df = pd.DataFrame([[80.5], [81.2], [82.0]], index=index, columns=columns)
    mock_load.return_value = df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    assert "USDRUB" in result
    series = result["USDRUB"]
    assert isinstance(series, pd.Series)
    expected_series = df[("Close", "USDRUB=X")]
    assert (series == expected_series).all()

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_close_is_single_col_df(mock_load):
    # Close is a DataFrame with one column, should convert to Series
    index = pd.date_range("2024-01-01", periods=3)
    close_df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = close_df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    assert isinstance(result["USDRUB"], pd.Series)
    assert (result["USDRUB"] == close_df["Close"]).all()

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_missing_close_column_raises(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Open": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = df

    service = CurrencyService()
    with pytest.raises(DataLoadError, match="Data for USDRUB does not contain 'Close' column"):
        service.load_pairs(["USDRUB"])

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_missing_close_multiindex_raises(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Open", "USDRUB=X")])
    df = pd.DataFrame([[80.5], [81.2], [82.0]], index=index, columns=columns)
    mock_load.return_value = df

    service = CurrencyService()
    with pytest.raises(DataLoadError, match="Data for USDRUB does not contain 'Close' column"):
        service.load_pairs(["USDRUB"])

@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_close_is_explicit_dataframe(mock_load):
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    class FakeDF(pd.DataFrame):
        @property
        def shape(self):
            return (3, 1)

        def __getitem__(self, key):
            return pd.DataFrame({key: [80.5, 81.2, 82.0]}, index=index)

    fake_df = FakeDF(df)
    mock_load.return_value = fake_df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])
    
    assert isinstance(result["USDRUB"], pd.Series)
    pd.testing.assert_series_equal(result["USDRUB"], df["Close"])