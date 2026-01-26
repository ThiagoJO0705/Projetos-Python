from fastapi import HTTPException, Depends, Header
from app_gateway.services.javer_services import JaverService
from app_gateway.services.customers_services import CustomerDataService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app_data.schemas.enums import InvestorProfile

security = HTTPBearer()

async def get_or_create_pyinvest_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    '''Auto Cadastro do usuário Javer no banco de dados do PyInvest'''
    token = auth.credentials
    javer_user = await JaverService.get_user_data_from_javer(token)
    pyinvest_user = await CustomerDataService.get_customer_by_filter(cpf=javer_user['cpf'])
    if not pyinvest_user:
        new_user_payload = {
            'name': javer_user['name'],
            'email': javer_user['email'],
            'cpf': javer_user['cpf'],
            'password': 'EXTERNAL_AUTH_JAVER',
            'phone_number': javer_user.get('phone_number') or javer_user['cpf'],
            'investor_profile': InvestorProfile.UNDEFINED,
            'total_assets': 0.0,
            'is_active': True
        }
        pyinvest_user = await CustomerDataService.create_customer(new_user_payload)
    else:
        update_payload = {}
        if pyinvest_user['name'] != javer_user['name']:
            update_payload['name'] = javer_user['name']
        if pyinvest_user['email'] != javer_user['email']:
            update_payload['email'] = javer_user['email']
        if update_payload:
            pyinvest_user = await CustomerDataService.update_customer(pyinvest_user['id'], update_payload)
    return {
        'javer': javer_user, 
        'pyinvest': pyinvest_user,
        'is_admin': javer_user['is_admin']
    }

async def validate_active_investor(user_context: dict = Depends(get_or_create_pyinvest_user)):
    '''Valida se a conta do investidor está ativa.'''
    if not user_context['pyinvest']['is_active']:
        raise HTTPException(status_code=403, detail='Acesso negado. Sua conta de investidor no PYInvest está desativada.')
    return user_context