from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import verify_token, get_session, verify_account_holder, generate_score
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.schemas.schemas import PixSending, TransactionResponse, PaymentRequest, TransactionSchema
from app.schemas.enums import TransactionDirection, TransactionType
from typing import List
from decimal import Decimal

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
        customer.account_balance += Decimal(str(round(deposit_value, 2)))
        new_score = generate_score(customer.account_balance)
        session.commit()
        new_transaction = Transaction(
            customer_id=customer.id,
            type=TransactionType.DEPOSIT,
            direction=TransactionDirection.CREDIT,
            amount=deposit_value,
            description="Depósito em dinheiro"
        )
        session.add(new_transaction)
        session.commit()
        return {'deposit_value': deposit_value,
                'new_balance': customer.account_balance,
                'new_score': new_score}
    raise HTTPException(status_code=400, detail='Valor inválido. O depósito deve ser um número positivo.')

@banking.post('/payment', response_model=TransactionResponse)
async def payment(payment_data: PaymentRequest, session: Session = Depends(get_session), customer: Customer = Depends(verify_token)):
    '''
        Rota para efetuar pagamento (Boleto, Conta, etc.)

    '''
    if payment_data.method == TransactionType.DEPOSIT:
        raise HTTPException(status_code=400, detail='Operação inválida. Não é possível usar Depósito como forma de pagamento.')
    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    if payment_data.amount > customer.account_balance:
        raise HTTPException(status_code=400, detail='Transação negada. Saldo atual insuficiente para o valor solicitado.')
    new_transaction = Transaction(
        customer_id=customer.id,
        type=payment_data.method,
        direction=TransactionDirection.DEBIT,
        amount=payment_data.amount,
        description=f"[{payment_data.method.value}] {payment_data.description}"
    )
    customer.account_balance = Decimal(str(round(customer.account_balance - payment_data.amount, 2)))
    session.add(new_transaction)
    session.commit()
    session.refresh(customer)
    session.refresh(new_transaction)
    return {
        'message': 'Pagamento efetuado com sucesso!',
        'new_balance': customer.account_balance,
        'new_score': customer.score,
        'extract': new_transaction
    }

@banking.post('/pix', response_model=TransactionResponse)
async def pix(pix: PixSending, session: Session = Depends(get_session), sender: Customer = Depends(verify_token)):
    if pix.pix_amount <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    receiver = session.query(Customer).filter(or_(Customer.email == pix.pix_key, Customer.cpf == pix.pix_key, Customer.phone_number == pix.pix_key)).first()
    if not receiver:
        raise HTTPException(status_code=404, detail='Transação negada. Chave Pix não encontrada.')
    if receiver.id == sender.id:
        raise HTTPException(status_code=400, detail='Transação negada. Não é permitido fazer um Pix para si mesmo.')
    if not receiver.is_active:
        raise HTTPException(status_code=400, detail='Transação negada. Conta do destinatário está desativada.')
    if not receiver.is_account_holder:
        raise HTTPException(status_code=400, detail='Transação negada. O destinatário não é Correntista.')
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
    sender.account_balance -= Decimal(str(round(pix.pix_amount, 2)))
    receiver.account_balance += Decimal(str(round(pix.pix_amount, 2)))
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


@banking.get('/statement',  response_model=List[TransactionSchema])
async def get_statement(session: Session = Depends(get_session), customer: Customer = Depends(verify_account_holder)):
    """
    Retorna o histórico completo de transações do usuário logado.
    As transações são ordenadas da mais recente para a mais antiga.
    """
    transactions = session.query(Transaction).filter(Transaction.customer_id == customer.id).order_by(Transaction.created_at.desc()).all()
    return transactions