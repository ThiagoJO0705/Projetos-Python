from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema
from models import Order

order_router = APIRouter(prefix='/orders', tags=['orders'])

@order_router.get('/')
async def get_orders():
    '''
    Essa é a rota padrão de pedidos. Todas as rotas dos pedidos precisam de autenticação
    '''
    return {'message': 'Você acessou a rota de pedidos!'}

@order_router.post('/order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    '''
    Rota para criação de novos pedidos
    '''
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {'message': f'Pedido criado com sucesso! ID do pedido: {new_order.id}'}