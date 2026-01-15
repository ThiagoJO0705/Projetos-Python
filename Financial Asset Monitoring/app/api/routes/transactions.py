from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_session, verify_token
from app.models.transaction import Transaction
from app.models.asset import Asset
from app.models.user import User
from app.schemas.schemas import TransactionCreate, TransactionResponse
import yfinance as yf
from datetime import timedelta, datetime

transactions = APIRouter(prefix="/transactions", tags=["transactions"])

def validate_market_price(ticker: str, price_sent: float, date: datetime):
    """ Valida se o preço enviado está na faixa de mercado do dia """
    tck = yf.Ticker(ticker)
    start = date.strftime('%Y-%m-%d')
    end = (date + timedelta(days=1)).strftime('%Y-%m-%d')    
    hist = tck.history(start=start, end=end)
    if hist.empty:
        return True
    low = float(hist['Low'].iloc[0])
    high = float(hist['High'].iloc[0])
    margin = 0.02
    if not (low * (1 - margin) <= price_sent <= high * (1 + margin)):
        raise HTTPException(
            status_code=400, 
            detail=f"Preço R${price_sent} fora da realidade. No dia {start} variou entre R${low:.2f} e R${high:.2f}"
        )
    return True

@transactions.post("/", response_model=TransactionResponse)
async def create_transaction(data: TransactionCreate, session: Session = Depends(get_session),user: User = Depends(verify_token)):
    '''
    Rota para criar uma transação feita em algum momento
    '''
    asset = session.query(Asset).filter(Asset.ticker == data.ticker.upper()).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não cadastrado. Cadastre o ativo em /assets primeiro.")
    transaction_date = data.timestamp or datetime.now()
    validate_market_price(asset.ticker, data.price, transaction_date)
    new_transaction = Transaction(
        user_id=user.id,
        asset_id=asset.id,
        quantity=data.quantity,
        price=data.price,
        type=data.type,
        timestamp=transaction_date
    )

    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    transaction_response = TransactionResponse(
        id=new_transaction.id,
        ticker=asset.ticker,
        quantity=float(new_transaction.quantity),
        price=float(new_transaction.price),
        type=new_transaction.type,
        timestamp=new_transaction.timestamp
    )
    return transaction_response

@transactions.get("/", response_model=list[TransactionResponse])
async def list_user_transactions(session: Session = Depends(get_session), user: User = Depends(verify_token)
):
    """ Lista apenas as transações do usuário logado """
    transactions = session.query(Transaction).filter(Transaction.user_id == user.id).all()
    if not transactions:
        raise HTTPException(status_code=400, detail="Nenhuma transação encontrada para este usuário.")
    transaction_response = [
            TransactionResponse(
                id=t.id,
                ticker=t.asset.ticker,
                quantity=float(t.quantity),
                price=float(t.price),
                type=t.type,
                timestamp=t.timestamp
            ) for t in transactions
        ]

    return transaction_response