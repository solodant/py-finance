#!/usr/bin/env python3
"""PyFinance CLI application entry point.

This module provides a command-line interface for basic financial analysis
including data loading, return calculation, and volatility estimation.
"""

import argparse
import matplotlib.pyplot as plt
import pandas as pd
from data.csv_loader import CSVDataLoader
from data.api.yahoo_loader import YahooFinanceLoader
from analysis.returns import ReturnsCalculator
from analysis.volatility import VolatilityCalculator


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments

    Raises:
        SystemExit: If no valid data source is provided
    """
    parser = argparse.ArgumentParser(
        description='PyFinance - Basic Financial Analysis CLI',
        epilog='Example: python app.py --ticker AAPL OR python app.py --csv data.csv'
    )
    parser.add_argument(
        '--ticker',
        help='Stock ticker symbol (e.g., AAPL)',
        type=str
    )
    parser.add_argument(
        '--csv',
        help='Path to CSV file with financial data',
        type=str
    )
    
    args = parser.parse_args()
    
    if not args.ticker and not args.csv:
        parser.error("Either --ticker or --csv must be specified")
        
    return args


def initialize_components(args: argparse.Namespace) -> tuple:
    """Initialize data loader and analysis components based on input arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        tuple: (data_loader, data, title) where:
            - data_loader: Initialized data loader instance
            - data: Loaded financial data
            - title: Title for visualization
            
    Raises:
        SystemExit: If data loading fails
    """
    try:
        if args.csv:
            loader = CSVDataLoader()
            data = loader.load(args.csv)
            title = f"CSV Data: {args.csv}"
        else:
            loader = YahooFinanceLoader()
            data = loader.load(args.ticker)
            title = f"Stock: {args.ticker.upper()}"
            
        return loader, data, title
        
    except Exception as e:
        raise SystemExit(f"Error loading data: {str(e)}")


def perform_analysis(data: pd.DataFrame) -> tuple:
    """Perform financial analysis on loaded data.
    
    Args:
        data: DataFrame containing financial data with 'Close' prices
        
    Returns:
        tuple: (returns, volatility) calculated series
        
    Raises:
        SystemExit: If analysis fails
    """
    try:
        returns_calc = ReturnsCalculator()
        volatility_calc = VolatilityCalculator()
        
        returns = returns_calc.calculate(data['Close'])
        volatility = volatility_calc.calculate(returns)
        
        return returns, volatility
        
    except Exception as e:
        raise SystemExit(f"Analysis error: {str(e)}")


def visualize_results(
    prices: pd.Series,
    returns: pd.Series,
    volatility: pd.Series,
    title: str
) -> None:
    """Visualize financial data and analysis results.
    
    Args:
        prices: Series of closing prices
        returns: Series of calculated returns
        volatility: Series of calculated volatility
        title: Title for the visualization
        
    Returns:
        None: Displays matplotlib plot
    """
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Price plot
        prices.plot(ax=ax1, title=f"{title} - Price", grid=True)
        ax1.set_ylabel("Price ($)")
        
        # Returns and volatility plot
        returns.plot(ax=ax2, label="Returns", color='green', alpha=0.7)
        ax2.set_ylabel("Daily Returns")
        
        # Add volatility on secondary axis
        ax2_vol = ax2.twinx()
        volatility.plot(
            ax=ax2_vol,
            label="Volatility (21d)",
            color='red',
            alpha=0.5
        )
        ax2_vol.set_ylabel("Volatility")
        
        # Combine legends
        lines, labels = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_vol.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        raise SystemExit(f"Visualization error: {str(e)}")


def main() -> None:
    """Execute main application workflow.
    
    1. Parse command line arguments
    2. Initialize data loader and load data
    3. Perform financial analysis
    4. Visualize results
    """
    args = parse_arguments()
    _, data, title = initialize_components(args)
    returns, volatility = perform_analysis(data)
    visualize_results(data['Close'], returns, volatility, title)


if __name__ == "__main__":
    main()