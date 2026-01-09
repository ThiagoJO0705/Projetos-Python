from fastapi import APIRouter, Depends, Query
from api.dependencies import verify_admin, get_session
from sqlalchemy.orm import Session
from models.customer import Customer
from schemas.schemas import CustomerResponse
from typing import List, Optional

admin = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(verify_admin)])

@admin.get('/customers', response_model=List[CustomerResponse])
async def get_customers(is_active: Optional[bool] = Query(None), is_account_holder: Optional[bool] = Query(None), name: Optional[str] = Query(None), session: Session = Depends(get_session)):
    """
    Rota para pegar todos os clientes com filtros dinâmicos
    """
    customers = session.query(Customer).filter(Customer.is_admin == False).all()

    if is_active is not None:
        customers = session.query.filter(Customer.is_active == is_active).all()
    
    if is_account_holder is not None:
        customers = session.query.filter(Customer.is_account_holder == is_account_holder).all()
    
    if name:
        customers = session.query.filter(Customer.name.contains(name)).all()
    
    return customers