import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from app_gateway.services.yfinance_services import YahooService
from app_data.schemas.enums import InvestmentType

@patch("yfinance.Ticker")
def test_get_usd_brl_rate_success(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.fast_info = {"last_price": 4.95}
    mock_ticker.return_value = mock_instance
    rate = YahooService.get_usd_brl_rate()
    assert rate == 4.95

@patch("yfinance.Ticker")
def test_get_usd_brl_rate_fallback(mock_ticker):
    mock_ticker.side_effect = Exception("Erro Yahoo")
    rate = YahooService.get_usd_brl_rate()
    assert rate == 5.0

@patch("yfinance.Ticker")
def test_get_asset_details_fast_price(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": 150.123}
    mock_asset.info = {
        "longName": "Apple Inc",
        "quoteType": "EQUITY",
        "currency": "USD"
    }
    mock_ticker.return_value = mock_asset
    result = YahooService.get_asset_details("aapl")
    assert result["ticker"] == "AAPL"
    assert result["name"] == "Apple Inc"
    assert result["type"] == InvestmentType.STOCKS
    assert result["current_price"] == 150.12
    assert result["currency"] == "USD"

@patch("yfinance.Ticker")
def test_get_asset_details_history_price(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": np.nan}
    mock_asset.history.return_value = pd.DataFrame({
        "Close": [100.0]
    })
    mock_asset.info = {
        "shortName": "ETF Test",
        "quoteType": "ETF",
        "currency": "BRL"
    }
    mock_ticker.return_value = mock_asset
    result = YahooService.get_asset_details("ivvb11")
    assert result["type"] == InvestmentType.FUNDS
    assert result["current_price"] == 100.0

@patch("yfinance.Ticker")
def test_get_asset_details_no_history(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": None}
    mock_asset.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_asset
    result = YahooService.get_asset_details("XXXX")
    assert result is None

@patch("yfinance.Ticker")
def test_get_asset_details_info_exception(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": 10}
    type(mock_asset).info = property(
        lambda _: (_ for _ in ()).throw(Exception("Erro info"))
    )
    mock_ticker.return_value = mock_asset
    result = YahooService.get_asset_details("TEST")
    assert result is None

@patch("yfinance.Ticker")
def test_get_asset_details_exception(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info.side_effect = Exception("Erro geral")
    mock_ticker.return_value = mock_asset
    result = YahooService.get_asset_details("FAIL")
    assert result is None

@patch("yfinance.Ticker")
def test_get_current_price_success(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": 42.567}
    mock_ticker.return_value = mock_asset
    price = YahooService.get_current_price("AAPL")
    assert price == 42.57

@patch("yfinance.Ticker")
def test_get_current_price_nan(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.fast_info = {"last_price": np.nan}
    mock_ticker.return_value = mock_asset
    price = YahooService.get_current_price("AAPL")
    assert price == 0.0

@patch("yfinance.Ticker")
def test_get_current_price_exception(mock_ticker):
    mock_ticker.side_effect = Exception()
    price = YahooService.get_current_price("AAPL")
    assert price == 0.0

@patch("yfinance.Ticker")
def test_get_historical_data_success(mock_ticker):
    mock_asset = MagicMock()
    df = pd.DataFrame({"Close": [1, 2, 3]})
    mock_asset.history.return_value = df
    mock_ticker.return_value = mock_asset
    result = YahooService.get_historical_data("AAPL")
    assert not result.empty

@patch("yfinance.Ticker")
def test_get_historical_data_empty(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_asset
    result = YahooService.get_historical_data("AAPL")
    assert result.empty

@patch("yfinance.Ticker")
def test_get_historical_data_exception(mock_ticker):
    mock_ticker.side_effect = Exception()
    result = YahooService.get_historical_data("AAPL")
    assert result.empty

@patch("yfinance.Ticker")
def test_get_market_variation_success(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame({
        "Close": [100, 110]
    })
    mock_ticker.return_value = mock_asset
    variation = YahooService.get_market_variation("AAPL")
    assert variation == 10.0

@patch("yfinance.Ticker")
def test_get_market_variation_insufficient_data(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame({"Close": [100]})
    mock_ticker.return_value = mock_asset
    variation = YahooService.get_market_variation("AAPL")
    assert variation == 0.0

@patch("yfinance.Ticker")
def test_get_market_variation_exception(mock_ticker):
    mock_ticker.side_effect = Exception()
    variation = YahooService.get_market_variation("AAPL")
    assert variation == 0.0

@patch("yfinance.Ticker")
def test_get_price_on_date_success(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame({
        "Low": [90],
        "High": [110]
    })
    mock_ticker.return_value = mock_asset
    result = YahooService.get_price_on_date("AAPL", "2024-01-01")
    assert result["day_low"] == 90
    assert result["day_high"] == 110

@patch("yfinance.Ticker")
def test_get_price_on_date_empty(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_asset
    result = YahooService.get_price_on_date("AAPL", "2024-01-01")
    assert result is None

@patch("yfinance.Ticker")
def test_get_price_on_date_exception(mock_ticker):
    mock_ticker.side_effect = Exception()
    result = YahooService.get_price_on_date("AAPL", "2024-01-01")
    assert result is None

@patch("yfinance.Ticker")
def test_get_usd_brl_rate_on_date_success(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame({"Close": [5.2]})
    mock_ticker.return_value = mock_asset
    rate = YahooService.get_usd_brl_rate_on_date("2024-01-01")
    assert rate == 5.2

@patch("yfinance.Ticker")
def test_get_usd_brl_rate_on_date_empty(mock_ticker):
    mock_asset = MagicMock()
    mock_asset.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_asset
    with patch.object(YahooService, "get_usd_brl_rate", return_value=4.9):
        rate = YahooService.get_usd_brl_rate_on_date("2024-01-01")
    assert rate == 4.9

@patch("yfinance.Ticker")
def test_get_usd_brl_rate_on_date_exception(mock_ticker):
    mock_ticker.side_effect = Exception()
    rate = YahooService.get_usd_brl_rate_on_date("2024-01-01")
    assert rate == 5.0