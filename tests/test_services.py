"""
Unit tests for the core service layer of the py-finance project.

Tests cover:
- Data loading logic (from CSV, Excel, Yahoo API)
- Stock and currency data processing
- Analytical computations (returns, volatility)
- Visualization rendering
- Error handling for edge cases

Mocks are used to isolate service behavior from external dependencies.
"""

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from pandas import DataFrame
from core.exceptions import DataLoadError
from services.data_service import DataService
from services.stock_service import StockService
from services.currency_service import CurrencyService
from services.analysis import AnalysisService
from services.visualization import (
    VisualizationService,
    StockVisualizationService,
    CurrencyVisualizationService,
)

# --- Analysis Service Tests ---


def test_analysis_service_analyze() -> None:
    """Test that analyze() returns a dict containing 'returns' and 'volatility'."""
    df = pd.DataFrame({"Close": [100, 101, 102, 104, 107]})
    result = AnalysisService.analyze(df)
    assert "returns" in result
    assert "volatility" in result


def test_analysis_service_analyze_multiple() -> None:
    """Test that analyze_multiple() returns expected results for multiple columns."""
    df = pd.DataFrame({"AAPL": [100, 101, 102], "MSFT": [200, 202, 204]})
    results = AnalysisService.analyze_multiple(df)
    assert set(results.keys()) == {"AAPL", "MSFT"}


# --- Visualization Tests ---


def test_visualization(monkeypatch, price_data: DataFrame) -> None:
    """Test that the base visualization calls plt.show()."""
    analysis = AnalysisService.analyze(price_data)
    shown = {}

    def fake_show():
        shown["called"] = True

    monkeypatch.setattr(plt, "show", fake_show)
    VisualizationService.show(price_data["Close"], analysis, "Test")
    assert shown.get("called")


def test_stock_visualization(monkeypatch, price_data: DataFrame) -> None:
    """Test that stock visualization calls plt.show()."""
    analysis = AnalysisService.analyze_multiple(price_data)
    shown = {}

    def fake_show():
        shown["ok"] = True

    monkeypatch.setattr(plt, "show", fake_show)
    StockVisualizationService.show(price_data, analysis)
    assert shown.get("ok")


def test_currency_visualization(monkeypatch, price_data: DataFrame) -> None:
    """Test that currency visualization calls plt.show()."""
    shown = {}

    def fake_show():
        shown["done"] = True

    monkeypatch.setattr(plt, "show", fake_show)
    CurrencyVisualizationService.show(price_data, "Title")
    assert shown.get("done")


# --- DataService Tests ---


def test_load_data_with_no_args(args_empty) -> None:
    """Test that load_data raises ValueError when no input source is provided."""
    with pytest.raises(ValueError, match="No valid data source specified."):
        DataService.load_data(args_empty)


def test_load_data_csv_mock(args_csv) -> None:
    """Test loading data using a mocked CSV loader."""
    with patch("data.csv_loader.CSVDataLoader.load", return_value="csv"):
        data, title = DataService.load_data(args_csv)
        assert data == "csv"
        assert title.startswith("CSV")


def test_load_data_csv_explicit_true_path(args_csv) -> None:
    """Test CSV path substitution and title format."""
    args_csv.csv = args_csv.csv.replace("test.csv", "file.csv")

    with patch("data.csv_loader.CSVDataLoader.load", return_value="csv"):
        data, title = DataService.load_data(args_csv)
        assert data == "csv"
        assert "CSV" in title


def test_load_data_excel_mock(args_excel) -> None:
    """Test loading data using a mocked Excel loader."""
    with patch("data.excel_loader.ExcelDataLoader.load", return_value="excel"):
        data, title = DataService.load_data(args_excel)
        assert data == "excel"
        assert title.startswith("Excel")


# --- StockService Tests ---


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_data_ticker_mock(mock_loader, args_ticker) -> None:
    """Test stock data loading with MultiIndex format and valid 'Close' column."""
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "AAPL")])
    df = pd.DataFrame([[100], [101], [102]], index=index, columns=columns)
    mock_loader.return_value = df

    data, title = DataService.load_data(args_ticker)
    assert "AAPL" in data
    assert isinstance(data["AAPL"], pd.Series)
    assert title == "Stocks: AAPL (6mo)"


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_multiindex_with_close(mock_load) -> None:
    """Test MultiIndex input with 'Close' columns for each ticker."""
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "AAPL"), ("Close", "MSFT")])
    df = pd.DataFrame(
        [[100, 200], [101, 201], [102, 202]], index=index, columns=columns
    )
    mock_load.return_value = df

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_multiindex_missing_close(mock_load) -> None:
    """Test missing 'Close' in MultiIndex raises DataLoadError."""
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Open", "AAPL")])
    df = pd.DataFrame([[100], [101], [102]], index=index, columns=columns)
    mock_load.return_value = df

    service = StockService()
    with pytest.raises(DataLoadError, match="MultiIndex: 'Close' column not found"):
        service.load_stocks(["AAPL"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_flat_columns(mock_load) -> None:
    """Test flat column DataFrame with ticker symbols."""
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"AAPL": [100, 101, 102], "MSFT": [200, 201, 202]}, index=index)
    mock_load.return_value = df

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_dict_with_close(mock_load) -> None:
    """Test dict of DataFrames each with a 'Close' column."""
    index = pd.date_range("2024-01-01", periods=3)
    df1 = pd.DataFrame({"Close": [100, 101, 102]}, index=index)
    df2 = pd.DataFrame({"Close": [200, 201, 202]}, index=index)
    mock_load.return_value = {"AAPL": df1, "MSFT": df2}

    service = StockService()
    result = service.load_stocks(["AAPL", "MSFT"])

    assert "AAPL" in result and "MSFT" in result
    assert all(isinstance(series, pd.Series) for series in result.values())


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_dict_missing_close(mock_load) -> None:
    """Test missing 'Close' column in dict format raises error."""
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Open": [100, 101, 102]}, index=index)
    mock_load.return_value = {"AAPL": df}

    service = StockService()
    with pytest.raises(DataLoadError, match="'Close' column missing for AAPL"):
        service.load_stocks(["AAPL"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_stocks_unexpected_format(mock_load) -> None:
    """Test handling of None as unexpected loader return format."""
    mock_load.return_value = None

    service = StockService()
    with pytest.raises(
        DataLoadError, match="Unexpected format from YahooFinanceLoader"
    ):
        service.load_stocks(["AAPL"])


# --- CurrencyService Tests ---


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_data_currency_mock(mock_loader, args_currency) -> None:
    """Test currency data loading using mocked Yahoo loader."""
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_loader.return_value = df

    data, title = DataService.load_data(args_currency)
    assert "USDRUB" in data
    assert isinstance(data["USDRUB"], pd.Series)
    assert title == "Currency Pairs: USDRUB"


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_normal_df(mock_load) -> None:
    """Test currency pair loading from a normal single-level DataFrame."""
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    assert "USDRUB" in result
    assert isinstance(result["USDRUB"], pd.Series)
    assert (result["USDRUB"] == df["Close"]).all()


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_multiindex_df(mock_load) -> None:
    """Test currency pair loading from MultiIndex DataFrame."""
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Close", "USDRUB=X")])
    df = pd.DataFrame([[80.5], [81.2], [82.0]], index=index, columns=columns)
    mock_load.return_value = df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    series = result["USDRUB"]
    assert isinstance(series, pd.Series)
    expected_series = df[("Close", "USDRUB=X")]
    assert (series == expected_series).all()


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_close_is_single_col_df(mock_load) -> None:
    """Test handling of a single-column DataFrame with 'Close'."""
    index = pd.date_range("2024-01-01", periods=3)
    close_df = pd.DataFrame({"Close": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = close_df

    service = CurrencyService()
    result = service.load_pairs(["USDRUB"])

    assert isinstance(result["USDRUB"], pd.Series)
    assert (result["USDRUB"] == close_df["Close"]).all()


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_missing_close_column_raises(mock_load) -> None:
    """Test missing 'Close' column raises DataLoadError."""
    index = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"Open": [80.5, 81.2, 82.0]}, index=index)
    mock_load.return_value = df

    service = CurrencyService()
    with pytest.raises(
        DataLoadError, match="Data for USDRUB does not contain 'Close' column"
    ):
        service.load_pairs(["USDRUB"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_missing_close_multiindex_raises(mock_load) -> None:
    """Test missing 'Close' column in MultiIndex raises error."""
    index = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_tuples([("Open", "USDRUB=X")])
    df = pd.DataFrame([[80.5], [81.2], [82.0]], index=index, columns=columns)
    mock_load.return_value = df

    service = CurrencyService()
    with pytest.raises(
        DataLoadError, match="Data for USDRUB does not contain 'Close' column"
    ):
        service.load_pairs(["USDRUB"])


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_pairs_close_is_explicit_dataframe(mock_load) -> None:
    """Test overridden DataFrame type that returns another DataFrame on column access."""
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
