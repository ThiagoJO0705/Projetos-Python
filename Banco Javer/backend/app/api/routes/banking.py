from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import verify_token, get_session, verify_account_holder, generate_score
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.schemas.schemas import PixSending, PixResponse
from app.schemas.enums import TransactionDirection, TransactionType

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_account_holder)])

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

@banking.post('/pix', response_model=PixResponse)
async def pix(pix: PixSending, session: Session = Depends(get_session), sender: Customer = Depends(verify_token)):
    receiver = session.query(Customer).filter(or_(Customer.email == pix.pix_key, Customer.cpf == pix.pix_key, Customer.phone_number == pix.pix_key)).first()
    if not receiver:
        raise HTTPException(status_code=404, detail='Transação negada. Chave Pix não encontrada.')
    if receiver.id == sender.id:
        raise HTTPException(status_code=400, detail='Transação negada. Não é permitido fazer um Pix para si mesmo.')
    if not receiver.is_active:
        raise HTTPException(status_code=400, detail='Transação negada. Conta do destinatário está desativada.')
    if not receiver.is_account_holder:
        raise HTTPException(status_code=400, detail='Transação negada. O destinatário não é Correntista.')
    if pix.pix_amount <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    if pix.pix_amount > sender.account_balance:
        raise HTTPException(status_code=400, detail='Transação negada. Saldo atual insuficiente para o valor solicitado.')
    new_transaction_sender = Transaction(
        customer_id=sender.id,
        type=TransactionType.PIX,
        amount=pix.pix_amount,
        related_customer_id=receiver.id,
        description=f'Pix enviado para {receiver.name}',
        direction=TransactionDirection.DEBIT
    )
    new_transaction_receiver = Transaction(
        customer_id=receiver.id,
        type=TransactionType.PIX,
        amount=pix.pix_amount,
        related_customer_id=sender.id,
        description=f'Pix recebido de {sender.name}',
        direction=TransactionDirection.CREDIT
    )
    sender.account_balance -= round(pix.pix_amount, 2)
    receiver.account_balance += round(pix.pix_amount, 2)
    session.add(new_transaction_sender)
    session.add(new_transaction_receiver)
    session.commit()
    session.refresh(new_transaction_sender)
    session.refresh(sender) 

    return {
        'message': 'Pix enviado com sucesso!',
        'new_balance': sender.account_balance,
        'new_score': sender.score,
        'extract': new_transaction_sender 
        }