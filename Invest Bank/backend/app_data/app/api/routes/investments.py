from fastapi import APIRouter, Depends, HTTPException, status
from app_data.app.dbconfig import get_session 
from app_data.models.investments import Investment
from app_data.models.customer import Customer
from app_data.models.asset import Asset
from app_data.schemas.schemas import InvestmentBase, InvestmentResponse
from sqlalchemy.orm import Session

investments = APIRouter(prefix='/investments', tags=['investments'])

@investments.post('/', response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def post_investments(investment_base: InvestmentBase, session: Session = Depends(get_session)):
    '''
    Registrar uma nova compra de um investimento
    '''
    customer = session.query(Customer).filter(Customer.id == investment_base.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Cliente não encontrado para processar a transação.')
    asset = session.query(Asset).filter(Asset.id == investment_base.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail='Ativo não encontrado no catálogo.')
    new_investment = Investment(
        customer_id=investment_base.customer_id,
        asset_id=investment_base.asset_id,
        quantity=investment_base.quantity,
        purchase_price=investment_base.purchase_price,
        is_active=investment_base.is_active
    )
    try:
        session.add(new_investment)
        session.commit()
        session.refresh(new_investment)
        return new_investment
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail=f'Erro ao salvar investimento no banco de dados')

from sqlalchemy.orm import joinedload # Importe isso
from typing import List

@investments.get('/', response_model=List[InvestmentResponse])
async def get_investments(is_active: bool = True, session: Session = Depends(get_session)):
    '''Pega todos os investimentos já feitos'''
    query = session.query(Investment).options(joinedload(Investment.asset), joinedload(Investment.customer))
    query = query.filter(Investment.is_active == is_active)
    return query.all()

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





