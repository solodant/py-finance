import pytest
import pandas as pd
from unittest.mock import patch
from data.csv_loader import CSVDataLoader
from data.excel_loader import ExcelDataLoader
from data.api.yahoo_loader import YahooFinanceLoader
from data.base_loader import BaseDataLoader
from core.exceptions import DataLoadError


@pytest.fixture
def csv_loader():
    return CSVDataLoader()


@pytest.fixture
def excel_loader():
    return ExcelDataLoader()


# Тесты для base_loader


class DummyLoader(BaseDataLoader):
    def load(self, *args, **kwargs):
        return pd.DataFrame()


def test_base_loader_validate_not_dataframe():

    loader = DummyLoader()
    with pytest.raises(DataLoadError, match="not a DataFrame"):
        loader._validate_data("invalid")


def test_validate_data_empty_dataframe():
    loader = DummyLoader()
    with pytest.raises(DataLoadError):
        loader._validate_data(pd.DataFrame())


# Тесты для csv_loader


def test_csv_loader_file_not_found():
    loader = CSVDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("non_existent_file.csv")


def test_csv_loader_invalid_content(monkeypatch):
    def fake_read_csv(*args, **kwargs):
        raise Exception("fake error")

    monkeypatch.setattr("pandas.read_csv", fake_read_csv)

    loader = CSVDataLoader()
    with pytest.raises(DataLoadError, match="CSV loading error: fake error"):
        loader.load("somefile.csv")


def test_csv_loader_invalid_data_structure(tmp_path, csv_loader):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("wrong,data,structure\n1,2,3\n4,5,6")
    with pytest.raises(DataLoadError, match="CSV loading error"):
        csv_loader.load(str(invalid_csv))


def test_csv_loader_valid(tmp_path):
    # Создаём временный csv-файл
    file = tmp_path / "test.csv"
    file.write_text("Date,Close\n2024-01-01,100\n2024-01-02,101")

    loader = CSVDataLoader()
    df = loader.load(str(file))

    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert df.index.name == "Date"


# Тесты для excel_loader


def test_excel_loader_file_not_found():
    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("non_existent_file.xlsx")


def test_excel_loader_invalid_content(monkeypatch):
    def fake_read_excel(*args, **kwargs):
        raise Exception("excel is broken")

    monkeypatch.setattr("pandas.read_excel", fake_read_excel)

    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError, match="Excel loading error: excel is broken"):
        loader.load("broken.xlsx")


def test_excel_loader_invalid_data_structure(tmp_path, excel_loader):
    invalid_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    invalid_excel = tmp_path / "invalid.xlsx"
    invalid_df.to_excel(invalid_excel)
    with pytest.raises(DataLoadError, match="Excel loading error"):
        excel_loader.load(str(invalid_excel))


def test_excel_loader_valid(tmp_path):
    # Создаём временный Excel-файл
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


# Тесты для yahoo_loader


def test_yahoo_loader_api_error(monkeypatch):
    def fake_download(*args, **kwargs):
        raise Exception("API error")

    monkeypatch.setattr("yfinance.download", fake_download)

    loader = YahooFinanceLoader()
    with pytest.raises(DataLoadError):
        loader.load("AAPL")


def test_yahoo_loader_empty_dataframe():
    loader = YahooFinanceLoader()
    with patch("data.api.yahoo_loader.yf.download") as mock_download:
        mock_download.return_value = pd.DataFrame()
        with pytest.raises(DataLoadError, match="Loaded DataFrame is empty"):
            loader.load("AAPL")


def test_yahoo_loader_success(monkeypatch):
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
