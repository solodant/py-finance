from data.csv_loader import CSVDataLoader
from data.excel_loader import ExcelDataLoader
from services.currency_service import CurrencyService
from services.stock_service import StockService


class DataService:
    """Service for loading financial data."""

    @staticmethod
    def load_data(args) -> tuple:
        """Load data based on CLI arguments."""

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
