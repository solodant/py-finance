import argparse

VALID_PERIODS = ["1d", "5d", "1mo", "6mo", "ytd", "1y", "5y", "max"]

SUPPORTED_CURRENCY_PAIRS = [
    "USDRUB",
    "EURRUB",
    "GBPRUB",
    "CNYRUB",
    "JPYRUB",
    "CHFRUB",
    "AUDRUB",
    "CADRUB",
    "HKDRUB",
    "SGDRUB",
]

SUPPORTED_STOCK_NAMES = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSLA",
    "META",
    "NVDA",
    "BRK-B",
    "JPM",
    "V",
]


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
        choices=VALID_PERIODS,
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

    if args.currencies:
        invalid = [
            c for c in args.currencies if c.upper() not in SUPPORTED_CURRENCY_PAIRS
        ]
        if invalid:
            parser.error(f"❌ Unsupported currency pairs: {', '.join(invalid)}")
        args.currencies = [c.upper() for c in args.currencies]

    if args.tickers:
        invalid = [t for t in args.tickers if t.upper() not in SUPPORTED_STOCK_NAMES]
        if invalid:
            parser.error(f"❌ Unsupported stock tickers: {', '.join(invalid)}")
        args.tickers = [t.upper() for t in args.tickers]

    return args
