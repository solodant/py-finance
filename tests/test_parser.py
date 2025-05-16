import sys
from cli import parser


def test_parser_valid(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--ticker", "AAPL"])
    args = parser.parse_arguments()
    assert args.ticker == "AAPL"


def test_parser_invalid(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    try:
        parser.parse_arguments()
    except SystemExit as e:
        assert e.code == 2
