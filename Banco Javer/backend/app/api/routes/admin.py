from fastapi import APIRouter, Depends, Query, HTTPException
from api.dependencies import verify_admin, get_session, generate_score
from sqlalchemy.orm import Session
from models.customer import Customer
from schemas.schemas import CustomerResponse, CustomerUpdate
from typing import List, Optional

admin = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(verify_admin)])

@admin.get('/customers', response_model=List[CustomerResponse])
async def get_customers(is_active: Optional[bool] = Query(None), is_account_holder: Optional[bool] = Query(None), name: Optional[str] = Query(None), session: Session = Depends(get_session)):
    """
    Rota para pegar todos os clientes com filtros dinâmicos
    """

    query = session.query(Customer).filter(Customer.is_admin == False)

    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)
    if is_account_holder is not None:
        query = query.filter(Customer.is_account_holder == is_account_holder)
    if name:
        query = query.filter(Customer.name.contains(name))

    customers = query.all()
    return customers


@admin.patch('/customers/{customer_id}', response_model=CustomerResponse)
async def update_customer(customer_id: int, update_customer_schema: CustomerUpdate, session: Session = Depends(get_session)):
    """
    Rota para alterar dados de um cliente
    """
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    update_dict = update_customer_schema.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(customer, key, value)
    session.commit()
    return customer


@admin.delete('/customers/disable/{customer_id}')
async def disable_customer(customer_id: int, session: Session = Depends(get_session), admin: Customer = Depends(verify_admin)):
    """
    Rota para desativar um cliente (Soft Delete), impede a autodesativação de e garante a existência de ao menos um administrador ativo.
    """
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
    """
    Rota para ativar a conta de um cliente
    """
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