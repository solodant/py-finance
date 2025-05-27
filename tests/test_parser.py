import sys
import pytest
from cli import parser


def test_parser_valid_ticker(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--tickers", "AAPL"])
    args = parser.parse_arguments()
    assert args.tickers == ["AAPL"]

def test_parser_invalid_ticker(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--tickers", "INVALIDTICKER"])
    with pytest.raises(SystemExit) as e:
        parser.parse_arguments()
    assert e.value.code != 0

def test_parser_valid_currency(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--currencies", "USDRUB"])
    args = parser.parse_arguments()
    assert args.currencies == ["USDRUB"]

def test_parser_invalid_currency(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--currencies", "INVALIDPAIR"])
    with pytest.raises(SystemExit) as e:
        parser.parse_arguments()
    assert e.value.code != 0


def test_parser_valid_csv(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--csv", "file.csv"])
    args = parser.parse_arguments()
    assert args.csv == "file.csv"


def test_parser_valid_excel(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--excel", "file.xlsx"])
    args = parser.parse_arguments()
    assert args.excel == "file.xlsx"


def test_parser_no_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    args = parser.parse_arguments()
    assert args.tickers is None
    assert args.currencies is None
    assert args.csv is None
    assert args.excel is None
    assert args.period == "1y"
