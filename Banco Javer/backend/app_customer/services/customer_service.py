import httpx
from fastapi import HTTPException
from decimal import Decimal

BASE_URL = 'http://127.0.0.1:8001/customers'

class CustomerService:
    @staticmethod
    def calculate_score(balance: Decimal) -> Decimal:
        '''Cálculo do score do cliente'''
        return round(Decimal(str(balance)) * Decimal('0.1'), 2)

    @staticmethod
    async def create(data: dict):
        '''Cadastra o cliente no banco de dados'''
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{BASE_URL}/', json=data)
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json().get('detail'))
            return response.json()

    @staticmethod
    async def get_by_id(customer_id: int):
        '''Busca o cliente pelo ID'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}/{customer_id}')
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Usuário não encontrado na base de dados.')
            customer = response.json()
            customer['score'] = CustomerService.calculate_score(Decimal(customer['account_balance']))
            return customer

    @staticmethod
    async def get_by_filter(params: dict):
        '''Busca por email, cpf ou telefone para Login/Pix'''
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f'{BASE_URL}/filter', params=params)
            if response.status_code != 200:
                return None
            return response.json()

    @staticmethod
    async def update(customer_id: int, data: dict):
        '''Atualiza dados do cliente'''
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{BASE_URL}/{customer_id}', json=data)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json().get('detail'))
            return response.json()
        
    @staticmethod
    async def get_all(params: dict):
        '''
        Lista todos os clientes
        '''
        cleaned_params = {k: v for k, v in params.items() if v is not None and v != ""}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{BASE_URL}/", params=cleaned_params)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail="Erro ao recuperar lista de clientes."
                )
            return response.json()