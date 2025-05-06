import argparse

def parse_arguments() -> argparse.Namespace:
    """Parse and validate CLI arguments."""
    parser = argparse.ArgumentParser(
        description='PyFinance - Financial Analysis Tool'
    )
    parser.add_argument(
        '--ticker',
        help='Stock ticker symbol (e.g. AAPL)',
        type=str
    )
    parser.add_argument(
        '--csv',
        help='Path to CSV file with market data',
        type=str
    )
    parser.add_argument(
        '--period',
        help='Time period for Yahoo Finance (1d, 1mo, 1y)',
        type=str,
        default='1y'
    )
    
    args = parser.parse_args()
    if not args.ticker and not args.csv:
        parser.error("Either --ticker or --csv must be specified")
    return args