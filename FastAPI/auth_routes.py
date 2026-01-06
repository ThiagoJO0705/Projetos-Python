from fastapi import APIRouter, Depends, HTTPException
from models import User
from sqlalchemy.orm import sessionmaker
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=['auth'])

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

    