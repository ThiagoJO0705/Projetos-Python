from fastapi import APIRouter, Depends, HTTPException
from models import User
from sqlalchemy.orm import sessionmaker
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])


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


@auth_router.get('/')
async def read_auth():
    '''
    Essa é a rota padrão de autenticação
    '''
    return {'message': 'Você acessou a rota de autenticação!'}

@auth_router.post('/signup')
async def signup(user_schema: UserSchema, session = Depends(get_session)):
    '''
    Rota para cadastro de novos usuários
    '''
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(name=user_schema.name, email=user_schema.email, password=encrypted_password, active=user_schema.active, admin=user_schema.admin)
        session.add(new_user)
        session.commit()
        return {'message': f'Usuário cadastrado com sucesso: {user_schema.email}'}


@auth_router.post('/signin')
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
    

@auth_router.post('/refresh')
async def refresh_token(usuario: User = Depends(verify_token)):
    '''
    Rota para renovação de token de acesso
    '''
    access_token = create_token(usuario.id)
    return {'access_token': access_token,
            'token_type': 'Bearer'}