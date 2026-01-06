from fastapi import APIRouter, Depends, HTTPException
from models import User
from sqlalchemy.orm import sessionmaker
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def read_auth():
    '''
    Essa é a rota padrão de autenticação
    '''
    return {'message': 'Você acessou a rota de autenticação!'}

@auth_router.post('/signup')
async def signup(email: str, password: str, name : str, session = Depends(get_session)):
    '''
    Rota para cadastro de novos usuários
    '''
    user = session.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email do usuário já cadastrado!')
    else:
        encrypted_password = bcrypt_context.hash(password)
        new_user = User(name, email, encrypted_password)
        session.add(new_user)
        session.commit()
        return {'message': f'Usuário cadastrado com sucesso: {email}'}

    