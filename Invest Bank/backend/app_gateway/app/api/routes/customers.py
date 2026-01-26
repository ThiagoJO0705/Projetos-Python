from fastapi import APIRouter, Header
from app_gateway.app.dependencies import get_or_create_pyinvest_user

customers = APIRouter(prefix='/customer', tags=['customers'])

@customers.get('/me')
async def get_customer(authorization: str = Header(...)):
    '''Retorna os dados do investidor logado e, caso seja o primeiro acesso vindo do Banco Javer, realiza o auto-cadastro.'''
    user_context = await get_or_create_pyinvest_user(authorization)
    return user_context['pyinvest']

@customers.patch('/me')
async def update_customer():
    pass

@customers.delete('/me')
async def deactivate_customer():
    pass

