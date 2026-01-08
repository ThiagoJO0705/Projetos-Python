from fastapi import APIRouter
from models.customer import Customer, db
from sqlalchemy.orm import sessionmaker

auth = APIRouter(prefix='/auth', tags=['auth'])

@auth.post('/signup')
async def signup(email: str, password: str, name : str):
    '''
    Rota para cadastro de novos usuários
    '''
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(Customer).filter(Customer.email == email).first()
    if user:
        return {'message': 'Já existe um usuário com esse email!'}
    new_user = Customer(name, email, password)
    session.add(new_user)
    session.commit()
    return {'message': 'Usuário cadastrado com sucesso!'}

    