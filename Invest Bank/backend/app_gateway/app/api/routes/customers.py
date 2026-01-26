from fastapi import APIRouter, Header, HTTPException
from app_gateway.app.dependencies import get_or_create_pyinvest_user
from app_gateway.schemas.schemas import CustomerUpdate
from app_gateway.services.customers_services import CustomerDataService

customers = APIRouter(prefix='/customer', tags=['customers'])

@customers.get('/me')
async def get_customer(authorization: str = Header(...)):
    '''Retorna os dados do investidor logado e, caso seja o primeiro acesso vindo do Banco Javer, realiza o auto-cadastro.'''
    user_context = await get_or_create_pyinvest_user(authorization)
    return user_context['pyinvest']

@customers.patch('/me')
async def update_customer(update_data: CustomerUpdate, authorization: str = Header(...)):
    '''Atualiza dados do investidor logado'''
    user_context = await get_or_create_pyinvest_user(authorization)
    customer_id = user_context['pyinvest']['id']
    update_payload = update_data.model_dump(exclude_unset=True)
    if not update_payload:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    updated_user = await CustomerDataService.update_customer(customer_id, update_payload)
    return {
        "message": "Perfil atualizado com sucesso.",
        "user": updated_user
    }

@customers.delete('/me')
async def deactivate_customer():
    pass

