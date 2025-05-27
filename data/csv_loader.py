"""
Module providing CSV data loader implementation for financial data,
with validation and error handling.
"""

import pandas as pd
from data.base_loader import BaseDataLoader
from core.exceptions import DataLoadError


class CSVDataLoader(BaseDataLoader):
    """Data loader for CSV files with financial data."""

    def load(self, filepath: str) -> pd.DataFrame:
        """
        Load financial data from CSV file.

        Args:
            filepath: Path to CSV file.

        Returns:
            pd.DataFrame: Loaded financial data.

        Raises:
            DataLoadError: If file loading or parsing fails.
        """
        try:
            data = pd.read_csv(
                filepath,
                parse_dates=["Date"],
                index_col="Date",
                float_precision="round_trip",
            )
            self._validate_data(data)
            return data
        except Exception as e:
            raise DataLoadError(f"CSV loading error: {str(e)}")
