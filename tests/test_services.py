import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from services.data_service import DataService
from services.analysis import AnalysisService
from services.visualization import VisualizationService


class Args:
    def __init__(self, csv=None, excel=None, ticker=None, period="1y"):
        self.csv = csv
        self.excel = excel
        self.ticker = ticker
        self.period = period


@patch("data.csv_loader.CSVDataLoader.load")
def test_load_data_csv(mock_load):
    mock_load.return_value = "csv_data"
    args = Args(csv="file.csv")
    data, title = DataService.load_data(args)
    assert data == "csv_data"
    assert title == "CSV: file.csv"


@patch("data.excel_loader.ExcelDataLoader.load")
def test_load_data_excel(mock_load):
    mock_load.return_value = "excel_data"
    args = Args(excel="file.xlsx")
    data, title = DataService.load_data(args)
    assert data == "excel_data"
    assert title == "Excel: file.xlsx"


@patch("data.api.yahoo_loader.YahooFinanceLoader.load")
def test_load_data_ticker(mock_load):
    mock_load.return_value = "api_data"
    args = Args(ticker="AAPL", period="1mo")
    data, title = DataService.load_data(args)
    assert data == "api_data"
    assert title == "AAPL (1mo)"


def test_analysis_service_analyze():

    data = pd.DataFrame({"Close": pd.Series([100, 101, 102, 103])})

    result = AnalysisService.analyze(data)
    assert "returns" in result
    assert "volatility" in result

    assert hasattr(result["returns"], "plot")
    assert hasattr(result["volatility"], "plot")


def test_visualization_service(monkeypatch, price_data):
    analysis = AnalysisService.analyze(price_data)

    called = {}

    def mock_show():
        called["show"] = True

    monkeypatch.setattr(plt, "show", mock_show)

    VisualizationService.show(price_data["Close"], analysis, "Test")
    assert called.get("show") is True
