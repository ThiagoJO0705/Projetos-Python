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
async def update_customer(customer_id: int, update_customer_schema: CustomerUpdate, session: Session = Depends(get_session)):
    '''
    Rota para alterar dados de um cliente
    '''
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    update_dict = update_customer_schema.model_dump(exclude_unset=True)
    if 'email' in update_dict:
        existing_email = session.query(Customer).filter(Customer.email == update_dict['email'],  Customer.id != customer_id).first()
        if existing_email:
            raise HTTPException(status_code=400, detail='Este e-mail já está cadastrado em outra conta.')

    if 'cpf' in update_dict:
        existing_cpf = session.query(Customer).filter(Customer.cpf == update_dict['cpf'], Customer.id != customer_id).first()
        if existing_cpf:
            raise HTTPException(status_code=400, detail='Este CPF já está vinculado a outra conta.')

    for key, value in update_dict.items():
        setattr(customer, key, value)
    session.commit()
    session.refresh(customer)
    return customer


@admin.delete('/customers/disable/{customer_id}')
async def disable_customer(customer_id: int, session: Session = Depends(get_session), admin: Customer = Depends(verify_admin)):
    '''
    Rota para desativar um cliente (Soft Delete), impede a autodesativação de e garante a existência de ao menos um administrador ativo.
    '''
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    if not customer.is_active:
        raise HTTPException(status_code=400, detail='A conta deste usuário já está desativada!')
    if customer_id == admin.id:
        raise HTTPException(status_code=400, detail='Autodesativação de conta não permitida. Entre em contato com outro admin.')
    if customer.is_admin:
        active_admins_count = session.query(Customer).filter(Customer.is_admin == True, Customer.is_active == True).count() 
        if active_admins_count <= 1:
            raise HTTPException(status_code=400, detail='Operação negada: Este é o último administrador ativo no sistema.')
        
    customer.is_account_holder = False
    customer.is_active = False
    session.commit()
    return {
        'message': f'A conta do usuário {customer.name} (ID: {customer.id}) foi desativada.'
    }


@admin.patch('/customer/activate/{customer_id}')
async def activate_customer(customer_id: int, session: Session = Depends(get_session), admin: Customer = Depends(verify_admin)):
    '''
    Rota para ativar a conta de um cliente
    '''
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    if customer.is_active:
        raise HTTPException(status_code=400, detail='A conta deste usuário já está ativa!')
    customer.is_account_holder = True
    customer.is_active = True
    session.commit()
    return {
        'message': f'A conta do usuário {customer.name} (ID: {customer.id}) foi ativada.'
    }