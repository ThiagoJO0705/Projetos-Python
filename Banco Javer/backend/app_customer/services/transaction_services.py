import httpx
from fastapi import HTTPException
from decimal import Decimal

BASE_URL = 'http://127.0.0.1:8001/transactions'

class TransactionService:
    @staticmethod
    async def register(data: dict):
        '''Cria extratos e registra transações'''
        if "amount" in data and isinstance(data["amount"], Decimal):
            data["amount"] = float(data["amount"])
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{BASE_URL}/', json=data)
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json().get('detail'))
            return response.json()

    @staticmethod
    async def get_statement(customer_id: int):
        '''Busca todos os extratos de um cliente'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}/customer/{customer_id}')
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao buscar extrato.')
            return response.json()