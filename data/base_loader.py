"""
Module defining abstract and base classes for financial data loaders,
including validation and error handling mechanisms.
"""

from abc import ABC, abstractmethod
from typing import Union
import pandas as pd
from core.exceptions import DataLoadError


class AbstractDataLoader(ABC):
    """Abstract base class for data loading strategies."""

    @abstractmethod
    def load(self, source: str) -> pd.DataFrame:
        """
        Load financial data from specified source.

        Args:
            source: Path or identifier of data source.

        Returns:
            pd.DataFrame: Loaded financial data.

        Raises:
            DataLoadError: If loading fails.
        """
        pass


class BaseDataLoader(AbstractDataLoader):
    """Base class with common functionality for data loaders."""

    def _validate_data(self, data: pd.DataFrame) -> None:
        """
        Validate loaded DataFrame structure.

        Args:
            data: DataFrame to validate.

        Raises:
            DataLoadError: If validation fails due to wrong type or empty DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            raise DataLoadError("Loaded data is not a DataFrame")
        if data.empty:
            raise DataLoadError("Loaded DataFrame is empty")
