from data.csv_loader import CSVDataLoader
from data.api.yahoo_loader import YahooFinanceLoader

class DataService:
    """Service for loading financial data."""
    
    @staticmethod
    def load_data(args) -> tuple:
        """Load data based on CLI arguments."""
        if args.csv:
            data = CSVDataLoader().load(args.csv)
            title = f"CSV: {args.csv}"
        else:
            data = YahooFinanceLoader().load(args.ticker, args.period)
            title = f"{args.ticker.upper()} ({args.period})"
        return data, title