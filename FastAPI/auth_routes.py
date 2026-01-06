from fastapi import APIRouter
from models import User, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def read_auth():
    '''
    Essa é a rota padrão de autenticação
    '''
    return {'message': 'Você acessou a rota de autenticação!'}

@auth_router.post('/signup')
async def signup(email: str, password: str, name : str):
    '''
    Rota para cadastro de novos usuários
    '''
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(User).filter(User.email == email).first()
    if user:
        return {'message': 'Já existe um usuário com esse email!'}
    new_user = User(name, email, password)
    session.add(new_user)
    session.commit()
    return {'message': 'Usuário cadastrado com sucesso!'}

    