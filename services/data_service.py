"""
Module providing DataService for loading financial data from various sources.

Supports loading currency pairs, CSV files, Excel files, and stock tickers
based on the provided arguments.
"""

from typing import Any, Tuple
from data.csv_loader import CSVDataLoader
from data.excel_loader import ExcelDataLoader
from services.currency_service import CurrencyService
from services.stock_service import StockService


class DataService:
    """Service for loading financial data from multiple sources."""

    @staticmethod
    def load_data(args: Any) -> Tuple[Any, str]:
        """
        Load financial data based on CLI or function arguments.

        Args:
            args: An object with attributes specifying data sources:
                  - currencies (list[str] | None): currency pairs to load
                  - csv (str | None): path to CSV file
                  - excel (str | None): path to Excel file
                  - tickers (list[str] | None): stock ticker symbols
                  - period (str | None): data period (e.g., '1y', '6mo')

        Returns:
            Tuple containing:
                - Loaded data (varies by source; e.g., dict, DataFrame)
                - Title string describing the data source

        Raises:
            ValueError: If no valid data source is specified in args.
        """
        if args.currencies:
            service = CurrencyService(period=args.period or "1y")
            currency_data = service.load_pairs(args.currencies)
            title = f"Currency Pairs: {', '.join(currency_data.keys())}"
            return currency_data, title

        elif args.csv:
            data = CSVDataLoader().load(args.csv)
            title = f"CSV: {args.csv}"
            return data, title

        elif args.excel:
            data = ExcelDataLoader().load(args.excel)
            title = f"Excel: {args.excel}"
            return data, title

        elif args.tickers:
            service = StockService(period=args.period or "1y")
            stock_data = service.load_stocks(args.tickers)
            title = f"Stocks: {', '.join(stock_data.keys())} ({args.period})"
            return stock_data, title

        else:
            raise ValueError("No valid data source specified.")
