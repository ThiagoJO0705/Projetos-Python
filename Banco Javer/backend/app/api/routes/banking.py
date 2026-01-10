from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import verify_token, get_session, verify_account_holder, generate_score
from sqlalchemy.orm import Session
from models.customer import Customer

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_token)])

@banking.get('/balance')

async def get_balance(customer: Customer = Depends(verify_token)):
    '''
        Rota para consultar saldo e score atual
    '''
    score = generate_score(customer.account_balance)
    return {'balance': customer.account_balance,
            'score': score}

@banking.post('/deposit')
async def deposit(deposit_value: float, session: Session = Depends(get_session), customer: Customer = Depends(verify_token)):
    '''
        Rota para depósito de dinheiro
    '''
    if deposit_value > 0:
        customer.account_balance += round(deposit_value, 2)
        session.commit()
        new_score = generate_score(customer.account_balance)
        return {'deposit_value': deposit_value,
                'new_balance': customer.account_balance,
                'new_score': new_score}
    raise HTTPException(status_code=400, detail='Valor inválido. O depósito deve ser um número positivo.')

@banking.post('/payment')
async def payment(payment_value: float, session: Session = Depends(get_session), customer: Customer = Depends(verify_token)):
    '''
        Rota para efetuar pagamento algo ou alguém
    '''
    if payment_value <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    if payment_value > customer.account_balance:
        raise HTTPException(status_code=400, detail='Transação negada. Saldo atual insuficiente para o valor solicitado.')
    customer.account_balance -= round(payment_value, 2)
    session.commit()
    new_score = generate_score(customer.account_balance)
    return {'payment_value': payment_value,
            'new_balance': customer.account_balance,
            'new_score': new_score}

@banking.post('/pix')
async def pix(pix_value: float, session: Session = Depends(get_session), customer: Customer = Depends(verify_token)):
    if pix_value <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    if pix_value > customer.account_balance:
        raise HTTPException(status_code=400, detail='Transação negada. Saldo atual insuficiente para o valor solicitado.')
    customer.account_balance -= round(pix_value, 2)
    session.commit()
    new_score = generate_score(customer.account_balance)
    return {'payment_value': pix_value,
            'new_balance': customer.account_balance,
            'new_score': new_score}