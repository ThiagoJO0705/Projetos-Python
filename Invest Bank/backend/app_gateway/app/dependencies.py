from fastapi import HTTPException, status
from app_gateway.services.javer_services import JaverService
from app_gateway.services.customers_services import CustomerDataService

async def get_or_create_pyinvest_user(authorization: str):
    '''Auto Cadastro do usuário Javer no banco de dados do PyInvest'''
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Token de autenticação ausente ou inválido.')
    token = authorization.split(' ')[1]
    javer_user = await JaverService.get_user_data_from_javer(token)
    pyinvest_user = await CustomerDataService.get_customer_by_filter(cpf=javer_user['cpf'])
    if not pyinvest_user:
        new_user_payload = {
            'name': javer_user['name'],
            'email': javer_user.get('email', f'{javer_user['cpf']}@javer.com.br'),
            'cpf': javer_user['cpf'],
            'password': 'EXTERNAL_AUTH_JAVER',
            'phone_number': javer_user.get('phone_number') or javer_user['cpf'],
            'investor_profile': 'UNDEFINED',
            'total_assets': 0.0
        }
        pyinvest_user = await CustomerDataService.create_customer(new_user_payload)
    return {'javer': javer_user, 'pyinvest': pyinvest_user}