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
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não existe!')
    update_dict = update_customer_schema.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(customer, key, value)
    session.commit()
    return customer