import httpx
from fastapi import HTTPException

JAVER_API_URL = 'http://localhost:8000'

class JaverService:
    @staticmethod
    async def get_javer_data(token: str):
        '''Usa o token do Javer para buscar os dados do usuário logado'''
        headers = {'Authorization': f'Bearer {token}'}
        async with httpx.AsyncClient() as client:
            user_response = await client.get(f'{JAVER_API_URL}/auth/me', headers=headers)
            if user_response.status_code != 200:
                raise HTTPException(status_code=401, detail='Token do Banco Javer inválido ou expirado.')
            user_data = user_response.json()
            return {
                'cpf': user_data['cpf'],
                'balance': float(user_data['account_balance']),
                'name': user_data['name']
            }