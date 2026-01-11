from fastapi import APIRouter, Depends, HTTPException, status
from app.models.customer import Customer
from app.api.dependencies import get_session, verify_token
from app.main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.schemas.schemas import CustomerCreate, CustomerResponse, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth = APIRouter(prefix='/auth', tags=['auth'])


def create_token(id_customer: int, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    '''
    Função para criação de token JWT
    '''
    expiration_date = datetime.now(timezone.utc) + token_duration
    dict_info = {'sub': str(id_customer), 'exp': expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def authenticate_customer(email, password, session):
    '''
    Função para autenticação de usuário
    '''
    customer = session.query(Customer).filter(Customer.email == email).first()
    if not customer:
        return False
    elif not bcrypt_context.verify(password, customer.password):
        return False
    return customer


@auth.post('/signup', response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def signup(customer_create_schema: CustomerCreate, session: Session = Depends(get_session)):
    '''
    Rota para cadastro de novos usuários
    '''
    customer_email = session.query(Customer).filter(Customer.email == customer_create_schema.email).first()
    if customer_email:
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    customer_cpf = session.query(Customer).filter(Customer.cpf == customer_create_schema.cpf).first()
    if customer_cpf:
        raise HTTPException(status_code=400, detail='CPF do usuário já está vinculado a outra conta!')

    encrypted_password = bcrypt_context.hash(customer_create_schema.password)
    new_customer = Customer(
        name=customer_create_schema.name,
        email=customer_create_schema.email,
        password=encrypted_password,
        phone_number=customer_create_schema.phone_number,
        cpf=customer_create_schema.cpf,
        account_balance=customer_create_schema.account_balance,
        is_account_holder=True,
        is_active=True, 
        is_admin=False           
    )
    session.add(new_customer)
    session.commit()
    return new_customer


@auth.post('/signin')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    '''
    Rota para login de usuários
    '''
    customer = authenticate_customer(login_schema.email, login_schema.password, session)
    if not customer:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    else:
        access_token = create_token(customer.id)
        refresh_token = create_token(customer.id, token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}
    

@auth.post('/signin-form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    '''
    Rota para login de usuários
    '''
    user = authenticate_customer(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}


@auth.post('/refresh')
async def refresh_token(customer: Customer = Depends(verify_token)):
    '''
    Rota para renovação de token de acesso
    '''
    access_token = create_token(customer.id)
    return {'access_token': access_token,
            'token_type': 'Bearer'}

    