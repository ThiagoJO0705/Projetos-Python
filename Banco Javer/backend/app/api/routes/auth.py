from fastapi import APIRouter, Depends, HTTPException
from models.customer import Customer
from sqlalchemy.orm import sessionmaker
from api.dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.schemas import CustomerSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

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
    if not Customer:
        return False
    elif not bcrypt_context.verify(password, Customer.password):
        return False
    return Customer


@auth.post('/signup')
async def signup(customer_schema: CustomerSchema, session = Depends(get_session)):
    '''
    Rota para cadastro de novos usuários
    '''
    customer = session.query(Customer).filter(Customer.email == customer_schema.email).first()
    if customer:
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    else:
        encrypted_password = bcrypt_context.hash(customer_schema.password)
        new_customer = Customer(name=customer_schema.name, email=customer_schema.email, password=encrypted_password, phone_number=customer_schema.phone_number, account_balance=customer_schema.account_balance, is_account_holder=customer_schema.is_account_holder, is_admin=customer_schema.is_admin)
        session.add(new_customer)
        session.commit()
        return {'message': f'Usuário cadastrado com sucesso: {customer_schema.email}'}


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
    

@auth.post('/refresh')
async def refresh_token(customer: Customer = Depends(verify_token)):
    '''
    Rota para renovação de token de acesso
    '''
    access_token = create_token(customer.id)
    return {'access_token': access_token,
            'token_type': 'Bearer'}

    