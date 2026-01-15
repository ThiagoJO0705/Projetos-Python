from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app_data.schemas.schemas import TransactionResponse, TransactionCreate
from app_data.models.transaction import Transaction
from app_data.models.customer import Customer
from sqlalchemy.orm import Session
from app_data.app.dbconfig import get_session

transactions = APIRouter(prefix='/transactions', tags=['transactions'])

@transactions.post('/', response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def post_transaction(transaction_create_schema: TransactionCreate, session: Session = Depends(get_session)):
    """
    Registra uma transação e atualiza o saldo do cliente.
    """
    customer = session.query(Customer).filter(Customer.id == transaction_create_schema.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para processar a transação.")
    if transaction_create_schema.direction == 'CREDIT':
        customer.account_balance += transaction_create_schema.amount
    else:
        customer.account_balance -= transaction_create_schema.amount
    new_transaction = Transaction(
        customer_id=transaction_create_schema.customer_id,
        type=transaction_create_schema.type,
        direction=transaction_create_schema.direction,
        amount=transaction_create_schema.amount,
        related_customer_id=transaction_create_schema.related_customer_id,
        description=transaction_create_schema.description
    )
    try:
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
        return new_transaction
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao processar transação financeira")


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