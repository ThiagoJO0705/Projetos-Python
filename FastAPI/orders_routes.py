from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema
from models import Order, User, OrderItem

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
    

@order_router.post('/order/add-item/{order_id}')
async def add_item_to_order(order_id: int, order_item_schema: OrderItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    ''' 
    Rota para adicionar itens ao pedido
    '''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='Pedido não existe!')
    if not user.admin and order.user != user.id:
        raise HTTPException(status_code=401, detail='Você não tem permissão para adicionar itens a este pedido!')
    order_item = OrderItem(quantity=order_item_schema.quantity, flavor=order_item_schema.flavor, size=order_item_schema.size,
                            unit_price=order_item_schema.unit_price, order=order_id)
    session.add(order_item)
    order.price_update()
    session.commit()
    return {'message': f'Item adicionado ao pedido {order.id} com sucesso!',
            'order_item': order_item.flavor,
            'order_price': order.price}


@order_router.post('/order/remove-item/{order_item_id}')
async def remove_item_from_order(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    ''' 
    Rota para remover itens do pedido
    '''
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    order = session.query(Order).filter(Order.id == order_item.order).first()
    if not order_item:
        raise HTTPException(status_code=400, detail='Item do pedido não existe!')
    if not user.admin and order.user != user.id :
        raise HTTPException(status_code=401, detail='Você não tem permissão para remover itens deste pedido!')
    session.delete(order_item)
    order.price_update()
    session.commit()
    return {'message': f'Item removido do pedido {order.id} com sucesso!',
            'quantity_itens': len(order.itens),
            'order': order}


@order_router.post('/order/finalize/{order_id}')
async def finalize_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    ''' 
    Rota para finalizar o pedido
    '''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    if not user.admin and order.user != user.id:
        raise HTTPException(status_code=401, detail='Você não tem permissão para finalizar este pedido!')
    order.status = 'FINALIZADO'
    session.commit()
    return {'message': f'Pedido número: {order.id} finalizado com sucesso!',
            'order': order}

@order_router.get('/order/{order_id}')
async def get_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    '''
    Rota para obter os detalhes de um pedido específico
    '''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    if not user.admin and order.user != user.id:
        raise HTTPException(status_code=401, detail='Você não tem permissão para ver este pedido!')
    return {
        'quantity_itens': len(order.itens),
        'order': order
    }


@order_router.get('/list/user-orders')
async def list_user_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    '''
    Rota para listagem de pedidos do usuário autenticado
    '''
    orders = session.query(Order).filter(Order.user == user.id).all()
    return {
        'orders': orders
    }
    