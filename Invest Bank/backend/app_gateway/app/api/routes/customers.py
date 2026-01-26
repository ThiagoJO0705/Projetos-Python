from fastapi import APIRouter, Header, HTTPException, status, Depends
from app_gateway.app.dependencies import get_or_create_pyinvest_user
from app_gateway.schemas.schemas import CustomerUpdate
from app_gateway.services.customers_services import CustomerDataService

customers = APIRouter(prefix='/customer', tags=['customers'])

@customers.get('/me')
async def get_customer(user_context: dict = Depends(get_or_create_pyinvest_user)):
    '''Retorna os dados do investidor logado e, caso seja o primeiro acesso vindo do Banco Javer, realiza o auto-cadastro.'''
    return user_context['pyinvest']

@customers.patch('/me')
async def update_customer(update_data: CustomerUpdate, user_context: dict = Depends(get_or_create_pyinvest_user)):
    '''Atualiza dados do investidor logado'''
    customer_id = user_context['pyinvest']['id']
    update_payload = update_data.model_dump(exclude_unset=True)
    if not update_payload:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    updated_user = await CustomerDataService.update_customer(customer_id, update_payload)
    return {
        "message": "Perfil atualizado com sucesso.",
        "user": updated_user
    }

@customers.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_my_investor_account(user_context: dict = Depends(get_or_create_pyinvest_user)):
    '''Desativa a conta do investidor no sistema PYInvest.'''
    customer_id = user_context['pyinvest']['id']
    if not user_context['pyinvest']['is_active']:
        raise HTTPException(status_code=400, detail="Sua conta de investidor já está desativada.")
    await CustomerDataService.soft_delete_investor(customer_id)
    return None

@customers.get('/all')
async def list_all_investors(user_context: dict = Depends(get_or_create_pyinvest_user)):
    '''Lista todos os investidores cadastrados. '''
    if not user_context.get('is_admin'):
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem listar todos os investidores.")
    return await CustomerDataService.get_all_customers()
