from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import verify_token, get_session
from sqlalchemy.orm import Session
from models.customer import Customer

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_token)])

def generate_score(balance):
    if balance > 0:
        return round(balance * 0.1, 2)
    else:
        return 0.0

@banking.get('/balance')
async def get_balance(customer: Customer = Depends(verify_token)):
    score = generate_score(customer.account_balance)
    return {'balance': customer.account_balance,
            'score': score}

@banking.post('/deposit')
async def deposit(deposit_value: float, session: Session = Depends(get_session), customer: Customer = Depends(verify_token)):
    if deposit_value > 0:
        customer.account_balance += deposit_value
        session.commit()
        new_score = generate_score(customer.account_balance)
        return {'deposit': deposit_value,
                'new_balance': customer.account_balance,
                'new_score': new_score}
    raise HTTPException(status_code=400, detail='Valor inválido. O depósito deve ser um número positivo.')
        