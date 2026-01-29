import pytest
import pandas as pd
import numpy as np
from app_gateway.services.analysis_services import AnalysisService
from app_data.schemas.enums import InvestorProfile, InvestmentType

USD_RATE = 5.0

MOCK_DATA = [
    {
        "quantity": 10,
        "purchase_price": 100,
        "asset": {
            "ticker": "PETR4",
            "current_price": 120,
            "type": InvestmentType.STOCKS,
            "currency": "BRL"
        }
    },
    {
        "quantity": 5,
        "purchase_price": 50,
        "asset": {
            "ticker": "AAPL",
            "current_price": 80,
            "type": InvestmentType.STOCKS,
            "currency": "USD"
        }
    },
    {
        "quantity": 1,
        "purchase_price": 1000,
        "asset": {
            "ticker": "CDB123",
            "current_price": 1,
            "type": InvestmentType.FIXED_INCOME,
            "currency": "BRL"
        }
    }
]

def test_internal_extractors():
    valid_asset = {"ticker": "AAPL", "current_price": 150.0, "type": "AÇÕES", "currency": "USD"}
    
    assert AnalysisService._extract_ticker(valid_asset) == "AAPL"
    assert AnalysisService._extract_price(valid_asset) == 150.0
    assert AnalysisService._extract_type(valid_asset) == "AÇÕES"
    assert AnalysisService._extract_currency(valid_asset) == "USD"

    assert AnalysisService._extract_ticker({}) == "N/A"
    assert AnalysisService._extract_price({}) == 0.0
    assert AnalysisService._extract_type(None) == "OTHER"
    assert AnalysisService._extract_currency(None) == "BRL"

def test_portfolio_analysis_logic():
    res_empty = AnalysisService.get_portfolio_analysis([], InvestorProfile.MODERATE)
    assert res_empty["total_invested"] == 0.0
    assert res_empty["portfolio_items"] == []

    res_full = AnalysisService.get_portfolio_analysis(MOCK_DATA, InvestorProfile.MODERATE, USD_RATE)
    assert res_full["total_invested"] == 2250.0
    assert res_full["current_portfolio_value"] > 0
    assert len(res_full["portfolio_items"]) == 3

def test_visual_charts_data():
    composition = AnalysisService.get_portfolio_composition(MOCK_DATA, USD_RATE)
    assert isinstance(composition, list)
    assert len(composition) > 0

    performance = AnalysisService.get_assets_performance(MOCK_DATA, USD_RATE)
    assert isinstance(performance, list)
    assert "profit_loss_brl" in performance[0]

def test_portfolio_highlights():
    highlights = AnalysisService.get_highlights(MOCK_DATA, USD_RATE)
    assert "best_performer" in highlights
    assert "worst_performer" in highlights
    assert highlights["best_performer"]["ticker"] is not None

def test_financial_projections():
    res = AnalysisService.calculate_future_projection(2000.0, InvestorProfile.BOLD, years=2)
    assert res["projected_value"] > 2000.0
    assert res["profile"] == InvestorProfile.BOLD

def test_volatility_calculations():
    assert AnalysisService.calculate_volatility(pd.DataFrame()) == 0.0
    
    df = pd.DataFrame({"Close": [100, 105, 102, 108, 110]})
    vol = AnalysisService.calculate_volatility(df)
    assert vol > 0

def test_benchmark_comparison():
    assert "error" in AnalysisService.compare_with_benchmark(10.0, pd.DataFrame())
    
    df_market = pd.DataFrame({"Close": [100, 110]})
    res = AnalysisService.compare_with_benchmark(5.0, df_market)
    assert res["benchmark_name"] == "Ibovespa (^BVSP)"
    assert "performance_status" in res