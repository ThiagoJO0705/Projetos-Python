from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema
from models import Order, User

order_router = APIRouter(prefix='/orders', tags=['orders'], dependencies=[Depends(verify_token)])

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


@order_router.post('/order/cancel/{order_id}')
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User =Depends(verify_token)):
    '''
    Rota para cancelamento de pedidos
    '''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    if not user.admin and order.user != user.id:
        raise HTTPException(status_code=401, detail='Você não tem permissão para cancelar este pedido!')
    order.status = 'CANCELADO'
    session.commit()
    return {'message': f'Pedido número: {order.id} cancelado com sucesso!',
            'order': order}

@order_router.get('/list')
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    '''
    Rota para listagem de pedidos
    '''
    if not user.admin:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação!')
    else:
        orders = session.query(Order).all()
        return {
            'orders': orders
        }