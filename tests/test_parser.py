"""
Unit tests for the command-line interface (CLI) argument parser.

This module tests the argument parsing logic defined in the `parser` module
from the `cli` package. It ensures that the parser correctly handles valid and
invalid inputs for various arguments such as tickers, currencies, CSV and Excel files.

Tests cover:
- Valid and invalid ticker arguments
- Valid and invalid currency arguments
- File path arguments for CSV and Excel
- Behavior when no arguments are provided

All tests use `pytest` and monkeypatch `sys.argv` to simulate command-line input.
"""

import sys
import pytest
from cli import parser


def test_parser_valid_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a valid ticker is parsed correctly."""
    monkeypatch.setattr(sys, "argv", ["prog", "--tickers", "AAPL"])
    args = parser.parse_arguments()
    assert args.tickers == ["AAPL"]


def test_parser_invalid_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that an invalid ticker causes a SystemExit."""
    monkeypatch.setattr(sys, "argv", ["prog", "--tickers", "INVALIDTICKER"])
    with pytest.raises(SystemExit) as e:
        parser.parse_arguments()
    assert e.value.code != 0


def test_parser_valid_currency(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a valid currency pair is parsed correctly."""
    monkeypatch.setattr(sys, "argv", ["prog", "--currencies", "USDRUB"])
    args = parser.parse_arguments()
    assert args.currencies == ["USDRUB"]


def test_parser_invalid_currency(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that an invalid currency pair causes a SystemExit."""
    monkeypatch.setattr(sys, "argv", ["prog", "--currencies", "INVALIDPAIR"])
    with pytest.raises(SystemExit) as e:
        parser.parse_arguments()
    assert e.value.code != 0


def test_parser_valid_csv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a valid CSV file path is parsed correctly."""
    monkeypatch.setattr(sys, "argv", ["prog", "--csv", "file.csv"])
    args = parser.parse_arguments()
    assert args.csv == "file.csv"


def test_parser_valid_excel(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a valid Excel file path is parsed correctly."""
    monkeypatch.setattr(sys, "argv", ["prog", "--excel", "file.xlsx"])
    args = parser.parse_arguments()
    assert args.excel == "file.xlsx"


def test_parser_no_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that default values are set when no arguments are provided."""
    monkeypatch.setattr(sys, "argv", ["prog"])
    args = parser.parse_arguments()
    assert args.tickers is None
    assert args.currencies is None
    assert args.csv is None
    assert args.excel is None
    assert args.period == "1y"
