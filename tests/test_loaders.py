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
    def load(self, source):
        pass


def test_validate_data_not_dataframe():
    loader = DummyLoader()
    with pytest.raises(DataLoadError):
        loader._validate_data("not a dataframe")


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
    with pytest.raises(DataLoadError):
        loader.load("somefile.csv")


def test_csv_loader_invalid_data_structure(tmp_path, csv_loader):
    # Запишем файл с неправильной структурой (без колонки Date)
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("wrong,data,structure\n1,2,3\n4,5,6")
    with pytest.raises(DataLoadError, match="CSV loading error"):
        csv_loader.load(str(invalid_csv))


# Тесты для excel_loader


def test_excel_loader_file_not_found():
    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("non_existent_file.xlsx")


def test_excel_loader_invalid_content(monkeypatch):
    def fake_read_excel(*args, **kwargs):
        raise Exception("fake error")

    monkeypatch.setattr("pandas.read_excel", fake_read_excel)

    loader = ExcelDataLoader()
    with pytest.raises(DataLoadError):
        loader.load("somefile.xlsx")


def test_excel_loader_invalid_data_structure(tmp_path, excel_loader):
    # Создадим файл Excel без колонки Date (с помощью pandas)
    invalid_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    invalid_excel = tmp_path / "invalid.xlsx"
    invalid_df.to_excel(invalid_excel)
    with pytest.raises(DataLoadError, match="Excel loading error"):
        excel_loader.load(str(invalid_excel))


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
        mock_download.return_value = pd.DataFrame()  # пустой DF
        with pytest.raises(DataLoadError, match="Loaded DataFrame is empty"):
            loader.load("AAPL")
