from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.api.dependencies import get_session, verify_token
from app.main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.schemas.schemas import UserCreate, UserResponse, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth = APIRouter(prefix='/auth', tags=['auth'])


def create_token(id_user: int, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    '''
    Função para criação de token JWT
    '''
    expiration_date = datetime.now(timezone.utc) + token_duration
    dict_info = {'sub': str(id_user), 'exp': expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def authenticate_user(email, password, session):
    '''
    Função para autenticação de usuário
    '''
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


@auth.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_create_schema: UserCreate, session: Session = Depends(get_session)):
    '''
    Rota para cadastro de novos usuários
    '''
    user_email = session.query(User).filter(User.email == user_create_schema.email).first()
    if user_email:
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    user_phone = session.query(User).filter(User.phone_number == user_create_schema.phone_number).first()
    if user_phone:
        raise HTTPException(status_code=400, detail='Telefone do usuário já está vinculado a outra conta!')

    encrypted_password = bcrypt_context.hash(user_create_schema.password)
    new_user = User(
        name=user_create_schema.name,
        email=user_create_schema.email,
        password=encrypted_password,
        phone_number=user_create_schema.phone_number,       
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@auth.post('/signin')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    '''
    Rota para login de usuários
    '''
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}
    

@auth.post('/signin-form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    '''
    Rota para login de usuários
    '''
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas!')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))
        return {'access_token': access_token, 
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}


@auth.post('/refresh')
async def refresh_token(user: User = Depends(verify_token)):
    '''
    Rota para renovação de token de acesso
    '''
    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=timedelta(days=7))
    return {'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'}

    