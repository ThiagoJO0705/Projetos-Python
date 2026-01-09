from fastapi import APIRouter, Depends
from api.dependencies import verify_token, get_session
from sqlalchemy.orm import Session
from models.customer import Customer

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_token)])

def generate_score(balance):
    if balance > 0:
        return balance * 0.1
    else:
        return 0.0

@banking.get('/balance')
async def get_balance(customer: Customer = Depends(verify_token)):
    score = generate_score(customer.account_balance)
    return {'balance': customer.account_balance,
            'score': score}