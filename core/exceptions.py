"""
Module defining custom exceptions for finance-related errors,
including data loading and calculation issues.
"""


class FinanceException(Exception):
    """Base exception for all finance-related errors."""

    pass


class DataLoadError(FinanceException):
    """Exception raised when data loading fails."""

    pass


class CalculationError(FinanceException):
    """Exception raised for calculation errors."""

    pass
