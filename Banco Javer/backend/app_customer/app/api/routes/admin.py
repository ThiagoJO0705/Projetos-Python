from fastapi import APIRouter, Depends, Query, HTTPException, status
from app_customer.app.api.dependencies import verify_admin, verify_token, generate_score
from app_customer.services.customer_service import CustomerService
from app_customer.schemas.schemas import CustomerResponse, CustomerUpdate
from typing import List, Optional
from decimal import Decimal

admin = APIRouter(prefix='/admin', tags=['admin'])

@admin.get('/customers', response_model=List[CustomerResponse])
async def get_customers(is_active: Optional[bool] = Query(None), is_account_holder: Optional[bool] = Query(None), is_admin: Optional[bool] = Query(None), name: Optional[str] = Query(None), current_admin: dict = Depends(verify_admin)):
    '''
    Rota para pegar todos os clientes com filtros dinâmicos
    '''
    filter_params = {
        'is_active': is_active,
        'is_account_holder': is_account_holder,
        'name': name,
        'is_admin': is_admin
    }
    customers = await CustomerService.get_all(filter_params)
    for customer in customers:
        customer['score'] = generate_score(Decimal(str(customer['account_balance'])))
    return customers


@admin.patch('/customers/{customer_id}', response_model=CustomerResponse)
async def update_customer(customer_id: int, update_customer_schema: CustomerUpdate, user: dict = Depends(verify_token)):
    '''
    Rota para alterar dados de um cliente
    '''
    is_admin = user.get('is_admin')
    is_owner = user.get('id') == customer_id
    if not is_admin and not is_owner:
        raise HTTPException(status_code=403, detail='Você não tem permissão para alterar dados de terceiros.')
    update_dict = update_customer_schema.model_dump(exclude_unset=True)
    if not is_admin:
        update_dict.pop('is_admin', None)
        update_dict.pop('is_account_holder', None)
        update_dict.pop('is_active', None)
    updated_user = await CustomerService.update(customer_id, update_dict)
    updated_user['score'] = generate_score(Decimal(str(updated_user['account_balance'])))
    return updated_user


@admin.delete('/customers/disable/{customer_id}')
async def disable_customer(customer_id: int, user: dict = Depends(verify_token)):
    '''
    Rota para desativar um cliente (Soft Delete), impede a autodesativação de e garante a existência de ao menos um administrador ativo.
    '''
    target_customer = await CustomerService.get_by_id(customer_id)
    is_admin = user.get('is_admin')
    is_owner = user.get('id') == customer_id
    if not is_admin and not is_owner:
        raise HTTPException(status_code=403, detail='Acesso negado. É necessário ser o usuário ou admin')
    balance = Decimal(str(target_customer['account_balance']))
    if balance > 0:
        raise HTTPException(status_code=400, detail=f'Não é possível desativar conta com saldo positivo. Saldo atual: R$ {balance}')
    if is_admin and is_owner:
         raise HTTPException(status_code=400, detail='Autodesativação de admin não permitida por esta rota.')
    if target_customer.get('is_admin'):
        active_admins = await CustomerService.get_all({'is_admin': True, 'is_active': True})
        if len(active_admins) <= 1:
            raise HTTPException(status_code=400, detail='Operação negada: Último administrador ativo.')
    disable_customer = {'is_active': False, 'is_account_holder': False}
    await CustomerService.update(customer_id, disable_customer)
    return {
        'message': f'Usuário {target_customer['name']} desativado com sucesso.'
    }


@admin.patch('/customer/activate/{customer_id}', dependencies=[Depends(verify_admin)])
async def activate_customer(customer_id: int):
    '''
    Rota para ativar a conta de um cliente
    '''
    target_customer = await CustomerService.get_by_id(customer_id)
    if not target_customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    if target_customer['is_active']:
        raise HTTPException(status_code=400, detail='A conta deste usuário já está ativa!')
    activate_data = {'is_active': True, 'is_account_holder': True}
    updated_user = await CustomerService.update(customer_id, activate_data)
    return {
        'message': f'A conta do usuário {target_customer} (ID: {target_customer['id']}) foi ativada.'
    }