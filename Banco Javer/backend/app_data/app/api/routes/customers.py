from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app_data.models.customer import Customer 
from app_data.schemas.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from app_data.app.dbconfig import get_session 

customers = APIRouter(prefix='/customers', tags=['customers'])

@customers.post('/', response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_create_schema: CustomerCreate, session: Session = Depends(get_session)):
    """
    Cria um novo cliente no banco de dados.
    """
    new_customer = Customer(
        name=customer_create_schema.name,
        email=customer_create_schema.email,
        password=customer_create_schema.password, 
        phone_number=customer_create_schema.phone_number,
        cpf=customer_create_schema.cpf,
        account_balance=customer_create_schema.account_balance,
        is_account_holder=customer_create_schema.is_account_holder,
        is_active=customer_create_schema.is_active,
        is_admin=customer_create_schema.is_admin
    )
    try:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Ocorreu um erro ao tentar salvar no banco de dados.")

@customers.get('/', response_model=List[CustomerResponse])
async def get_all_customers(is_active: Optional[bool] = Query(None), is_account_holder: Optional[bool] = Query(None), name: Optional[str] = Query(None), is_admin: Optional[bool] = Query(None), session: Session = Depends(get_session)):
    """
    Retorna todos os clientes com opção de filtros
    """
    query = session.query(Customer)
    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)
    if is_account_holder is not None:
        query = query.filter(Customer.is_account_holder == is_account_holder)
    if name:
        query = query.filter(Customer.name.contains(name))
    if is_admin is not None:
        query = query.filter(Customer.is_admin == is_admin)
    return query.all()

@customers.get('/filter', response_model=CustomerResponse)
async def filter_customer(email: Optional[str] = Query(None), cpf: Optional[str] = Query(None), phone_number: Optional[str] = Query(None), session: Session = Depends(get_session)):
    """
    Busca um único cliente por e-mail, CPF ou Telefone.
    """
    if not any([email, cpf, phone_number]):
        raise HTTPException(status_code=400, detail="É necessário informar ao menos um critério de busca (email, cpf ou phone_number).")
    customer = session.query(Customer).filter(or_(Customer.email == email, Customer.cpf == cpf, Customer.phone_number == phone_number)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado com os critérios fornecidos.")
    return customer

@customers.get('/{customer_id}', response_model=CustomerResponse)
async def get_customer_by_id(customer_id: int, session: Session = Depends(get_session)):
    """
    Busca um cliente específico pelo ID.
    """
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não encontrado!')
    return customer


@customers.patch('/{customer_id}', response_model=CustomerResponse)
async def update_customer(customer_id: int, customer_in: CustomerUpdate, session: Session = Depends(get_session)):
    """
    Atualiza dados pessoais do cliente e status de conta
    """
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Usuário não encontrado!')
    update_dict = customer_in.model_dump(exclude_unset=True)
    for field in ["email", "cpf", "phone_number"]:
        if field in update_dict:
            value = update_dict[field]
            existing_value = session.query(Customer).filter(getattr(Customer, field) == value, Customer.id != customer_id).first()
            if existing_value:
                raise HTTPException(status_code=400, detail=f"Este {field} já está sendo usado por outro usuário.")
    for field, value in update_dict.items():
        setattr(customer, field, value)
    try:
        session.commit()
        session.refresh(customer)
        return customer
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar o usuário {customer.name} (ID: {customer_id})")