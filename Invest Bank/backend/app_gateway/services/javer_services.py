import httpx
from fastapi import HTTPException

JAVER_API_URL = 'http://localhost:8000'

class JaverService:
    @staticmethod
    async def get_user_data_from_javer(token: str):
        '''Consome a API do Banco Javer para obter os dados do usuário autenticado.'''
        headers = {'Authorization': f'Bearer {token}'}
        async with httpx.AsyncClient() as client:
            try:
                user_response = await client.get(f'{JAVER_API_URL}/auth/me', headers=headers)
                if user_response.status_code != 200:
                    raise HTTPException(status_code=401, detail='Sua sessão no Banco Javer expirou ou o token é inválido.')
                user_data = user_response.json()
                return {
                    'cpf': user_data['cpf'],
                    'balance': float(user_data['account_balance']),
                    'name': user_data['name'],
                    'id': user_data['id']
                }
            except httpx.ConnectError:
                raise HTTPException(status_code=503, detail='O serviço do Banco Javer está temporariamente indisponível. Não foi possível validar seu saldo.')
            except Exception:
                raise HTTPException(status_code=500, detail=f'Erro ao integrar com o Banco Javer')