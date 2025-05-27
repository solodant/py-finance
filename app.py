"""
Main application script for PyFinance financial analysis tool.

Parses CLI arguments to load financial data from various sources (CSV, Excel,
Yahoo Finance for stocks or currencies), performs analysis, and visualizes
results accordingly.

Usage examples:
    python app.py --csv data_example/test_data.csv
    python app.py --excel data_example/test_data.xlsx
    python app.py --tickers AAPL MSFT --period 6mo
    python app.py --currencies USDRUB EURRUB --period 1y
"""

from cli.parser import parse_arguments
from cli.parser import (
    VALID_PERIODS,
    SUPPORTED_CURRENCY_PAIRS,
    SUPPORTED_STOCK_NAMES,
)
from services.analysis import AnalysisService
from services.data_service import DataService
from services.visualization import (
    VisualizationService,
    CurrencyVisualizationService,
    StockVisualizationService,
)


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()

    if not any([args.currencies, args.tickers, args.csv, args.excel]):
        print("\n⚠️  No data source specified.")
        print("Please specify one of the following options to load data:\n")

        print("📄 CSV File:")
        print("  --csv path/to/file.csv")
        print("  Load market data from a local CSV file.\n")

        print("📊 Excel File:")
        print("  --excel path/to/file.xlsx")
        print("  Load market data from a local Excel file.\n")

        print("💱 Currency Analysis:")
        print("  --currencies USDRUB EURRUB")
        print("  Analyze currency exchange rate pairs.\n")
        print("  ✅ Supported currency pairs:")
        print("    ", ", ".join(SUPPORTED_CURRENCY_PAIRS), "\n")

        print("📈 Stock Market Analysis:")
        print("  --tickers AAPL MSFT")
        print("  Analyze stock data by specifying ticker symbols.\n")
        print("  ✅ Supported stock tickers:")
        print("    ", ", ".join(SUPPORTED_STOCK_NAMES), "\n")

        print("⏱️  Period Option (optional):")
        print("  --period 1mo")
        print("  Time period for Yahoo Finance data (default is 1y).\n")
        print("  ✅ Supported periods:")
        print("    ", ", ".join(VALID_PERIODS), "\n")

        print("💡 Example:")
        print("  python app.py --csv data_example/test_data.csv")
        print("  python app.py --excel data_example/test_data.xlsx")
        print("  python app.py --tickers AAPL MSFT --period 6mo")
        print("  python app.py --currencies USDRUB EURRUB --period 1y")

        return

    try:
        data, title = DataService.load_data(args)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    if args.currencies:
        CurrencyVisualizationService.show(data, title)

    elif args.tickers:
        analysis_results = AnalysisService.analyze_multiple(data)
        StockVisualizationService.show(data, analysis_results)

    else:
        analysis = AnalysisService.analyze(data)
        VisualizationService.show(data["Close"], analysis, title)


if __name__ == "__main__":
    main()
