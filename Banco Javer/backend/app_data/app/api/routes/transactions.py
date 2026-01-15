from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app_data.schemas.schemas import TransactionResponse
from app_data.models.transaction import Transaction
from app_data.models.customer import Customer
from sqlalchemy.orm import Session
from app_data.app.dbconfig import get_session


transactions = APIRouter(prefix='/transactions', tags=['transactions'])

@transactions.post('/')
async def post_transaction():
    pass


@transactions.get('/customer/{customer_id}', response_model=List[TransactionResponse])
async def get_customer_transactions(customer_id: int, session: Session = Depends(get_session)):
    """
    Retorna a lista de todas as transações de um cliente específico, sendo que as transações são ordenadas da mais recente para a mais antiga.
    """
    customer = session.query(Customer.id).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    transactions_list = session.query(Transaction).filter(Transaction.customer_id == customer_id).order_by(Transaction.created_at.desc()).all()
    return transactions_list