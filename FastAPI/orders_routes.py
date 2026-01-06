from fastapi import APIRouter

order_router = APIRouter(prefix='/orders', tags=['orders'])

@order_router.get('/')
async def get_orders():
    '''
    Essa é a rota padrão de pedidos. Todas as rotas dos pedidos precisam de autenticação
    '''
    return {'message': 'Você acessou a rota de pedidos!'}