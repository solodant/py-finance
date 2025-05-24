import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse and validate CLI arguments."""
    parser = argparse.ArgumentParser(description="PyFinance - Financial Analysis Tool")
    parser.add_argument(
        "--tickers", nargs="+", help="Stock ticker symbol (e.g. AAPL MSFT)", type=str
    )
    parser.add_argument("--csv", help="Path to CSV file with market data", type=str)
    parser.add_argument("--excel", help="Path to Excel file (.xlsx, .xls)", type=str)
    parser.add_argument(
        "--period",
        help="Time period for Yahoo Finance (1d, 1mo, 1y)",
        type=str,
        default="1y",
    )
    parser.add_argument(
        "--currencies",
        nargs="+",
        help="List of currency pairs (e.g., USDRUB EURRUB)",
        type=str,
    )

    args = parser.parse_args()
    return args
