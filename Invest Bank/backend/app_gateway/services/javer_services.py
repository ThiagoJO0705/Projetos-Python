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
                    'email': user_data['email'],
                    'phone_number': user_data['phone_number'],
                    'is_admin': user_data.get('is_admin', False),
                    'id': user_data['id']
                }
            except httpx.ConnectError:
                raise HTTPException(status_code=503, detail='O serviço do Banco Javer está temporariamente indisponível. Não foi possível validar seu saldo.')
            except Exception:
                raise HTTPException(status_code=500, detail=f'Erro ao integrar com o Banco Javer')
            
    @staticmethod
    async def debit_account(token: str, amount: float, ticker: str):
        '''Método para chamar a api do banco javer e realizar um debito na conta do usuario'''
        headers = {'Authorization': f'Bearer {token}'}
        payment_payload = {
            "method": "PIX",
            "amount": amount,
            "description": f"Compra do ativo: {ticker} via PYInvest"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{JAVER_API_URL}/banking/payment", 
                    json=payment_payload, 
                    headers=headers
                )
                if response.status_code != 200:
                    error_detail = response.json().get('detail', 'Erro no débito')
                    raise HTTPException(status_code=400, detail=f"Javer Bank: {error_detail}")
                return response.json() 
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro de comunicação com Javer: {str(e)}")
            
    @staticmethod
    async def credit_account(token: str, amount: float):
        '''Realiza o depósito do valor da venda do ativo no Banco Javer.'''
        headers = {'Authorization': f'Bearer {token}'}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{JAVER_API_URL}/banking/deposit",
                params={"deposit_value": amount},
                headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Erro ao creditar valor no Banco Javer.")
            return response.json()