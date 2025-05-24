from cli.parser import parse_arguments
from services.data_service import DataService
from services.analysis import AnalysisService
from services.visualization import VisualizationService, CurrencyVisualizationService
from services.currency_service import SUPPORTED_CURRENCY_PAIRS


def main():
    args = parse_arguments()

    if not any([args.currencies, args.tickers, args.csv, args.excel]):
        print("\n⚠️  No data source specified.")
        print("You can use one of the following options:\n")
        print("  --tickers      Load stock data by ticker(s) (e.g., --tickers AAPL MSFT)")
        print("  --csv          Load market data from a CSV file (e.g., --csv path/to/file.csv)")
        print("  --excel        Load market data from an Excel file (e.g., --excel path/to/file.xlsx)")
        print("  --currencies   Analyze currency pairs (e.g., --currencies USDRUB EURRUB)\n")

        print("💱 Available currency pairs:")
        print("  ", ", ".join(SUPPORTED_CURRENCY_PAIRS))
        return

    try:
        data, title = DataService.load_data(args)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # Валюты (dict[str, pd.Series])
    if args.currencies:
        analysis = AnalysisService.analyze_multiple(data)
        CurrencyVisualizationService.show(data, title)

    # Несколько тикеров (dict[str, pd.Series])
    elif args.tickers:
        tickers = [t.upper() for t in args.tickers]
        # data и title уже получены выше — используем их напрямую
        analysis_results = AnalysisService.analyze_multiple(data)
        
        for ticker, series in data.items():
            analysis = analysis_results[ticker]
            VisualizationService.show(series, analysis, ticker)

    # CSV или Excel (pd.DataFrame)
    else:
        analysis = AnalysisService.analyze(data)
        VisualizationService.show(data["Close"], analysis, title)


if __name__ == "__main__":
    main()
