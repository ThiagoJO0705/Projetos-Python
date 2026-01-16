from fastapi import APIRouter, Depends, HTTPException
from app_customer.app.api.dependencies import verify_token, verify_account_holder, generate_score
from app_customer.services.customer_service import CustomerService
from app_customer.services.transaction_services import TransactionService
from app_customer.schemas.schemas import PixSending, TransactionResponse, PaymentRequest, TransactionSchema
from app_customer.schemas.enums import TransactionDirection, TransactionType
from typing import List
from decimal import Decimal

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_account_holder)])

@banking.get('/balance')
async def get_balance(customer: dict = Depends(verify_token)):
    '''
        Rota para consultar saldo e score atual
    '''
    balance = Decimal(str(customer['account_balance']))
    return {'balance': balance,
            'score': generate_score(balance)}

@banking.post('/deposit')
async def deposit(deposit_value: float, customer: dict = Depends(verify_token)):
    '''
        Rota para depósito de dinheiro
    '''
    if deposit_value <= 0:
        raise HTTPException(status_code=400, detail='O depósito deve ser um número positivo.')
    new_transaction = {
        'customer_id': customer['id'],
        'type': TransactionType.DEPOSIT,
        'direction': TransactionDirection.CREDIT,
        'amount': Decimal(str(round(deposit_value, 2))),
        'description': 'Depósito em dinheiro'
    }
    result = await TransactionService.register(new_transaction)
    updated_customer = await CustomerService.get_by_id(customer['id'])
    return {'deposit_value': deposit_value,
            'new_balance': updated_customer['account_balance'],
            'new_score': generate_score(updated_customer['account_balance'])}

@banking.post('/payment', response_model=TransactionResponse)
async def payment(payment_data: PaymentRequest, customer: dict = Depends(verify_token)):
    '''
        Rota para efetuar pagamento (Boleto, Conta, etc.)

    '''
    balance = Decimal(str(customer['account_balance']))
    if payment_data.method == TransactionType.DEPOSIT:
        raise HTTPException(status_code=400, detail='Operação inválida para pagamentos.')
    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail='O valor deve ser maior que zero.')
    if payment_data.amount > balance:
        raise HTTPException(status_code=400, detail='Saldo insuficiente.')
    new_transaction = {
        'customer_id': customer['id'],
        'type': payment_data.method,
        'direction': TransactionDirection.DEBIT,
        'amount': payment_data.amount,
        'description': f'[{payment_data.method.value}] {payment_data.description}'
    }
    extract = await TransactionService.register(new_transaction)
    new_balance = balance - payment_data.amount
    return {
        'message': 'Pagamento efetuado com sucesso!',
        'new_balance': new_balance,
        'new_score': generate_score(new_balance),
        'extract': extract
    }

@banking.post('/pix', response_model=TransactionResponse)
async def pix(pix: PixSending, sender: dict = Depends(verify_token)):
    '''Realiazação de PIX entre usuários'''
    if pix.pix_amount <= 0:
        raise HTTPException(status_code=400, detail='Transação negada. O valor solicitado deve ser maior que zero.')
    sender_balance = Decimal(str(sender['account_balance']))
    if pix.pix_amount > sender_balance:
        raise HTTPException(status_code=400, detail='Transação negada. Saldo atual insuficiente para o valor solicitado.')
    receiver = await CustomerService.get_by_filter({'email': pix.pix_key, 'cpf': pix.pix_key, 'phone_number': pix.pix_key})
    if not receiver:
        raise HTTPException(status_code=404, detail='Transação negada. Chave Pix não encontrada.')
    if receiver['id'] == sender['id']:
        raise HTTPException(status_code=400, detail='Transação negada. Não é permitido fazer um Pix para si mesmo.')
    if not receiver['is_active'] or not receiver['is_account_holder']:
        raise HTTPException(status_code=400, detail='Transação negada. Conta do destinatário inválida')
    new_transaction_sender = await TransactionService.register({
        'customer_id': sender['id'],
        'type': TransactionType.PIX,
        'direction': TransactionDirection.DEBIT,
        'amount': pix.pix_amount,
        'related_customer_id': receiver['id'],
        'description': f'Pix enviado para {receiver['name']}'
    })
    new_transaction_receiver = await TransactionService.register({
        'customer_id': receiver['id'],
        'type': TransactionType.PIX,
        'direction': TransactionDirection.CREDIT,
        'amount': pix.pix_amount,
        'related_customer_id': sender['id'],
        'description': f'Pix recebido de {sender['name']}'
    })
    new_balance = sender_balance - pix.pix_amount
    return {
        'message': 'Pix enviado com sucesso!',
        'new_balance': new_balance,
        'new_score': generate_score(new_balance),
        'extract': new_transaction_sender 
        }


@banking.get('/statement',  response_model=List[TransactionSchema])
async def get_statement(customer: dict = Depends(verify_account_holder)):
    '''
    Retorna o histórico completo de transações do usuário logado.
    As transações são ordenadas da mais recente para a mais antiga.
    '''
    return await TransactionService.get_statement(customer['id'])