from fastapi import APIRouter
from app_data.app.dbconfig import get_session 


investments = APIRouter(prefix='/investments', tags=['investments'])

@investments.post('/')
async def post_investments():
    '''Registrar uma nova compra de um investimento'''
    pass

@investments.get('/')
async def get_investments():
    '''Pega todos os investimentos já feitos'''
    pass

@investments.get('/customer/{customer_id}')
async def get_customer_investments():
    '''Pega todos os investimentos de um usuário'''
    pass

@investments.get('/investments/{id}')
async def get_investment():
    '''Pega os detalhes de um investimento espefcifico'''
    pass

@investments.patch('/investments/{id}')
async def update_investment():
    '''Atualiza dados de um investimento'''
    pass

@investments.delete('/investments/{id}')
async def delete_investment():
    '''Deleta o ativo do banco de dados'''
    pass





