"""
Module for loading financial data from Excel files (.xlsx, .xls),
with validation and error handling.
"""

import pandas as pd
from .base_loader import BaseDataLoader
from core.exceptions import DataLoadError


class ExcelDataLoader(BaseDataLoader):
    """Data loader for Excel files (.xlsx, .xls)."""

    def load(self, filepath: str) -> pd.DataFrame:
        """
        Load financial data from Excel file.

        Args:
            filepath: Path to Excel file.

        Returns:
            pd.DataFrame: Loaded financial data.

        Raises:
            DataLoadError: If loading fails.
        """
        try:
            data = pd.read_excel(
                filepath, parse_dates=["Date"], index_col="Date", engine="openpyxl"
            )
            self._validate_data(data)
            return data
        except Exception as e:
            raise DataLoadError(f"Excel loading error: {str(e)}")
