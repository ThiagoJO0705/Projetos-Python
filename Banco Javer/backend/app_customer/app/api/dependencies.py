from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app_customer.app.main import SECRET_KEY, ALGORITHM, oauth2_schema
from app_customer.services.customer_service import CustomerService
from decimal import Decimal

async def verify_token(token: str = Depends(oauth2_schema)):
    '''
    Decodifica o JWT e busca o usuário na App 2 para validar o acesso.
    '''
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        customer_id = int(dict_info.get('sub'))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Acesso Negado! Verifique a validade do token.')
    customer = await CustomerService.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=401, detail='Acesso Inválido!')
    if not customer.get('is_active'):
        raise HTTPException(status_code=401, detail='Acesso Negado! Sua conta está desativada!')
    return customer


def verify_account_holder(customer: Customer = Depends(verify_token)):
    '''Valida se o usuário é correntista.'''
    if not customer.get('is_account_holder'):
        raise HTTPException(status_code=403, detail='Você não tem permissão para fazer essa operação, é necessário ser Correntista.')
    return customer


def verify_admin(customer: dict = Depends(verify_token)):
    '''Valida se o usuário é administrador.'''
    if not customer.get('is_admin'):
        raise HTTPException(status_code=403, detail='Você não tem permissão para fazer essa operação, é necessário ser Admin.')
    return customer


def generate_score(balance):
    '''Calcula o score do cliente'''
    if balance and float(balance) > 0:
        return round(Decimal(str(balance)) * Decimal('0.1'), 2)
    return 0.0