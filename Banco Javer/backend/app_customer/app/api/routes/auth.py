from fastapi import APIRouter, Depends, HTTPException, status
from app_customer.services.customer_service import CustomerService
from app_customer.app.main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app_customer.schemas.schemas import CustomerCreate, CustomerResponse, LoginSchema
from jose import jwt
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


async def authenticate_customer(email, password):
    '''
    Função para autenticação de usuário
    '''
    customer = await CustomerService.get_by_filter({"email": email})
    if not customer:
        return False
    elif not bcrypt_context.verify(password, customer.password):
        return False
    return customer


@auth.post('/signup', response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def signup(customer_create_schema: CustomerCreate):
    '''
    Rota para cadastro de novos usuários
    '''
    if await CustomerService.get_by_filter({"email": customer_create_schema.email}):
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    if await CustomerService.get_by_filter({"cpf": customer_create_schema.cpf}):
        raise HTTPException(status_code=400, detail='CPF do usuário já está vinculado a outra conta!')
    if await CustomerService.get_by_filter({"phone_number": customer_create_schema.phone_number}):
        raise HTTPException(status_code=400, detail='Telefone do usuário já está vinculado a outra conta!')
    encrypted_password = bcrypt_context.hash(customer_create_schema.password)
    new_customer = {
        "name": customer_create_schema.name,
        "email": customer_create_schema.email,
        "password": encrypted_password,
        "phone_number": customer_create_schema.phone_number,
        "cpf": customer_create_schema.cpf,
        "account_balance": 0.0,
        "is_account_holder": True,
        "is_active": True,
        "is_admin": False
    }
    return await CustomerService.create(new_customer)


@auth.post('/signin')
async def login(login_schema: LoginSchema):
    '''
    Rota para login de usuários
    '''
    customer = await authenticate_customer(login_schema.email, login_schema.password)
    if not customer:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    if not customer['is_active']:
        raise HTTPException(status_code=401, detail='Acesso Negado. Usuário está com a conta desativada!')
    else:
        access_token = create_token(customer['id'])
        refresh_token = create_token(customer['id'], token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}
    

@auth.post('/signin-form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    '''
    Rota para login de usuários
    '''
    customer = await authenticate_customer(form_data.username, form_data.password)
    if not customer:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    else:
        access_token = create_token(customer['id'])
        refresh_token = create_token(customer['id'], token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}


@auth.post('/refresh')
async def refresh_token(customer: Customer = Depends(verify_token)):
    '''
    Rota para renovação de token de acesso
    '''
    access_token = create_token(customer.id)
    refresh_token = create_token(customer.id, token_duration=timedelta(days=7))
    return {'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'}

    