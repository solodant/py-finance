"""
Unit tests for data loaders used in the py-finance application.

This module contains test cases for the following data loader classes:
- CSVDataLoader
- ExcelDataLoader
- YahooFinanceLoader
- BaseDataLoader (abstract validation logic)

Tests cover:
- Successful and unsuccessful data loading from CSV, Excel, and Yahoo Finance API
- File not found and invalid file content
- Proper handling of invalid DataFrame structure or content
- Internal validation errors raised by the base loader
"""

import pytest
import pandas as pd
from unittest.mock import patch
from typing import Any
from pathlib import Path

from data.csv_loader import CSVDataLoader
from data.excel_loader import ExcelDataLoader
from data.api.yahoo_loader import YahooFinanceLoader
from data.base_loader import BaseDataLoader
from core.exceptions import DataLoadError


@pytest.fixture
def csv_loader() -> CSVDataLoader:
    """Fixture that returns a CSVDataLoader instance."""
    return CSVDataLoader()


@pytest.fixture
def excel_loader() -> ExcelDataLoader:
    """Fixture that returns an ExcelDataLoader instance."""
    return ExcelDataLoader()


# -----------------------------
# BaseDataLoader Tests
# -----------------------------


class DummyLoader(BaseDataLoader):
    """Dummy implementation of BaseDataLoader for validation testing."""

    def load(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """Stub load method returning empty DataFrame."""
        return pd.DataFrame()


def test_base_loader_validate_not_dataframe() -> None:
    """Test that _validate_data raises DataLoadError when input is not a DataFrame."""
    loader = DummyLoader()
    with pytest.raises(DataLoadError, match="not a DataFrame"):
        loader._validate_data("invalid")


def test_validate_data_empty_dataframe() -> None:
    """Test that _validate_data raises DataLoadError when input DataFrame is empty."""
    loader = DummyLoader()
    with pytest.raises(DataLoadError):
        loader._validate_data(pd.DataFrame())


# -----------------------------
# CSVDataLoader Tests
# -----------------------------


def test_csv_loader_file_not_found() -> None:
    """Test that CSVDataLoader raises DataLoadError when file does not exist."""
    loader = CSVDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("non_existent_file.csv")


def test_csv_loader_invalid_content(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that CSVDataLoader raises DataLoadError when pandas.read_csv fails."""

    def fake_read_csv(*args: Any, **kwargs: Any) -> None:
        raise Exception("fake error")

    monkeypatch.setattr("pandas.read_csv", fake_read_csv)

    loader = CSVDataLoader()
    with pytest.raises(DataLoadError, match="CSV loading error: fake error"):
        loader.load("somefile.csv")


def test_csv_loader_invalid_data_structure(
    tmp_path: Path, csv_loader: CSVDataLoader
) -> None:
    """Test that CSVDataLoader raises DataLoadError when file has invalid column structure."""
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("wrong,data,structure\n1,2,3\n4,5,6")
    with pytest.raises(DataLoadError, match="CSV loading error"):
        csv_loader.load(str(invalid_csv))


def test_csv_loader_valid(tmp_path: Path) -> None:
    """Test that CSVDataLoader correctly loads a well-structured CSV file."""
    file = tmp_path / "test.csv"
    file.write_text("Date,Close\n2024-01-01,100\n2024-01-02,101")

    loader = CSVDataLoader()
    df = loader.load(str(file))

    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert df.index.name == "Date"


# -----------------------------
# ExcelDataLoader Tests
# -----------------------------


def test_excel_loader_file_not_found() -> None:
    """Test that ExcelDataLoader raises DataLoadError when file does not exist."""
    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("non_existent_file.xlsx")


def test_excel_loader_invalid_content(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that ExcelDataLoader raises DataLoadError when pandas.read_excel fails."""

    def fake_read_excel(*args: Any, **kwargs: Any) -> None:
        raise Exception("excel is broken")

    monkeypatch.setattr("pandas.read_excel", fake_read_excel)

    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError, match="Excel loading error: excel is broken"):
        loader.load("broken.xlsx")


def test_excel_loader_invalid_data_structure(
    tmp_path: Path, excel_loader: ExcelDataLoader
) -> None:
    """Test that ExcelDataLoader raises DataLoadError for files missing expected structure."""
    invalid_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    invalid_excel = tmp_path / "invalid.xlsx"
    invalid_df.to_excel(invalid_excel)
    with pytest.raises(DataLoadError, match="Excel loading error"):
        excel_loader.load(str(invalid_excel))


def test_excel_loader_valid(tmp_path: Path) -> None:
    """Test that ExcelDataLoader correctly loads a well-structured Excel file."""
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame(
        {"Date": pd.date_range("2024-01-01", periods=2), "Close": [100.0, 101.5]}
    )
    df.to_excel(file_path, index=False)

    loader = ExcelDataLoader()
    loaded_df = loader.load(str(file_path))

    assert isinstance(loaded_df, pd.DataFrame)
    assert "Close" in loaded_df.columns
    assert loaded_df.index.name == "Date"


# -----------------------------
# YahooFinanceLoader Tests
# -----------------------------


def test_yahoo_loader_api_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that YahooFinanceLoader raises DataLoadError when yfinance throws an API error."""

    def fake_download(*args: Any, **kwargs: Any) -> None:
        raise Exception("API error")

    monkeypatch.setattr("yfinance.download", fake_download)

    loader = YahooFinanceLoader()
    with pytest.raises(DataLoadError):
        loader.load("AAPL")


def test_yahoo_loader_empty_dataframe() -> None:
    """Test that YahooFinanceLoader raises DataLoadError when yfinance returns an empty DataFrame."""
    loader = YahooFinanceLoader()
    with patch("data.api.yahoo_loader.yf.download") as mock_download:
        mock_download.return_value = pd.DataFrame()
        with pytest.raises(DataLoadError, match="Loaded DataFrame is empty"):
            loader.load("AAPL")


def test_yahoo_loader_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that YahooFinanceLoader successfully loads a non-empty DataFrame with 'Close' column."""
    dummy_df = pd.DataFrame(
        {
            "Open": [1.0, 2.0],
            "Close": [1.5, 2.5],
            "Date": pd.date_range("2023-01-01", periods=2),
        }
    )
    dummy_df.set_index("Date", inplace=True)

    monkeypatch.setattr("yfinance.download", lambda *args, **kwargs: dummy_df)

    loader = YahooFinanceLoader()
    result = loader.load("AAPL")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "Close" in result.columns
