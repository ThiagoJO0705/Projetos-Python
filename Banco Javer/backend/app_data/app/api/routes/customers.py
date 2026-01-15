from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app_data.models.customer import Customer 
from app_data.schemas.schemas import CustomerCreate, CustomerResponse
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

@customers.get('/')
async def get_all_customers():
    pass

@customers.get('/{customer_id}')
async def get_customer_by_id():
    pass

@customers.get('/filter')
async def filter_customer():
    pass

@customers.patch('/{customer_id}')
async def update_customer():
    pass