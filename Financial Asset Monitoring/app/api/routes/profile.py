from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_session, verify_token
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.schemas import UserResponse, UserUpdate, ProfileDashboard, AssetPerformance
from app.schemas.enums import TransactionType
import yfinance as yf
from typing import Dict, List


profile = APIRouter(prefix="/profile", tags=["profile"])

@profile.get("/", response_model=UserResponse)
async def get_my_profile(user: User = Depends(verify_token)):
    """
    Retorna os dados básicos do usuário logado através do Token JWT.
    """
    return user

@profile.patch("/", response_model=UserResponse)
async def update_profile( user_data: UserUpdate, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Atualiza informações do perfil.
    """
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    for key, value in update_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@profile.get("/dashboard", response_model=ProfileDashboard)
async def get_profile_dashboard(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Consolida todas as transações, calcula preço médio e busca lucros em tempo real.
    """
    transactions = session.query(Transaction).filter(Transaction.user_id == user.id).all()
    if not transactions:
        return {
            "user_email": user.email,
            "total_transactions": 0,
            "total_invested": 0.0,
            "current_balance": 0.0,
            "overall_profit_loss": 0.0,
            "status": "SEM MOVIMENTAÇÕES",
            "assets": []
        }

    portfolio_map: Dict[int, dict] = {}
    for item in transactions:
        aid = item.asset_id
        if aid not in portfolio_map:
            portfolio_map[aid] = {
                "quantity": 0.0, 
                "total_cost": 0.0, 
                "ticker": item.asset.ticker 
            }
        
        quantity = float(item.quantity)
        price = float(item.price)
        if item.type == TransactionType.BUY:
            portfolio_map[aid]["quantity"] += quantity
            portfolio_map[aid]["total_cost"] += (quantity * price)
        
        elif item.type == TransactionType.SELL:
            if portfolio_map[aid]["quantity"] > 0:
                avg_price = portfolio_map[aid]["total_cost"] / portfolio_map[aid]["quantity"]
                portfolio_map[aid]["quantity"] -= quantity
                portfolio_map[aid]["total_cost"] -= (quantity * avg_price)

    asset_performances = []
    total_invested_portfolio = 0.0
    total_current_value_portfolio = 0.0

    for aid, data in portfolio_map.items():
        if data["quantity"] <= 0:
            continue

        try:
            ticker_info = yf.Ticker(data["ticker"])
            last_price = float(ticker_info.fast_info['last_price'])
        except Exception:
            last_price = 0.0

        avg_price = data["total_cost"] / data["quantity"]
        total_asset_cost = data["total_cost"]
        total_asset_market_value = data["quantity"] * last_price
        profit_loss = total_asset_market_value - total_asset_cost
        profit_loss_pct = (profit_loss / total_asset_cost * 100) if total_asset_cost > 0 else 0
        total_invested_portfolio += total_asset_cost
        total_current_value_portfolio += total_asset_market_value

        asset_performances.append(
            AssetPerformance(
                ticker=data["ticker"],
                quantity=data["quantity"],
                average_price=round(avg_price, 2),
                current_price=round(last_price, 2),
                total_invested=round(total_asset_cost, 2),
                current_value=round(total_asset_market_value, 2),
                profit_loss=round(profit_loss, 2),
                profit_loss_pct=round(profit_loss_pct, 2)
            )
        )

    overall_pl = total_current_value_portfolio - total_invested_portfolio
    if overall_pl > 0:
        performance_status = "LUCRO"
    elif overall_pl < 0:
        performance_status = "PREJUÍZO"
    else:
        performance_status = "ESTÁVEL"

    return {
        "user_email": user.email,
        "total_transactions": len(transactions),
        "total_invested": round(total_invested_portfolio, 2),
        "current_balance": round(total_current_value_portfolio, 2),
        "overall_profit_loss": round(overall_pl, 2),
        "status": performance_status,
        "assets": asset_performances
    }