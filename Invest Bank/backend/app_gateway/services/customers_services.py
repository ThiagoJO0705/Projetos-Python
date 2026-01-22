import httpx
import uuid
from fastapi import HTTPException
from typing import Optional

DATA_SERVICE_URL = 'http://localhost:8001/customers'

class CustomerDataService:
    @staticmethod
    async def get_all_customers(name: Optional[str] = None, is_active: Optional[bool] = None):
        async with httpx.AsyncClient() as client:
            params = {'name': name, 'is_active': is_active}
            params = {k: v for k, v in params.items() if v is not None}
            response = await client.get(f'{DATA_SERVICE_URL}/', params=params)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao buscar clientes no Data Service')
            return response.json()

    @staticmethod
    async def get_customer_by_id(customer_id: uuid.UUID):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{DATA_SERVICE_URL}/{customer_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Cliente não encontrado no sistema de dados')
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao buscar cliente')
            return response.json()

    @staticmethod
    async def create_customer(customer_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{DATA_SERVICE_URL}/', json=customer_data)
            if response.status_code == 400:
                raise HTTPException(status_code=400, detail=response.json().get('detail', 'Erro de validação'))
            elif response.status_code != 201:
                raise HTTPException(status_code=500, detail='Erro interno ao criar cliente no Data Service')
            return response.json()

    @staticmethod
    async def update_customer(customer_id: uuid.UUID, update_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{DATA_SERVICE_URL}/{customer_id}', json=update_data)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Cliente não encontrado para atualização')
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao atualizar cliente')
            return response.json()

    @staticmethod
    async def get_customer_by_filter(email: Optional[str] = None, cpf: Optional[str] = None):
        async with httpx.AsyncClient() as client:
            params = {'email': email, 'cpf': cpf}
            params = {k: v for k, v in params.items() if v is not None}
            response = await client.get(f'{DATA_SERVICE_URL}/filter', params=params)
            if response.status_code == 404:
                return None 
            return response.json()