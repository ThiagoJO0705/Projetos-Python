import httpx
import uuid
from fastapi import HTTPException


INVESTMENT_SERVICE_URL = 'http://localhost:8001/investments'

class InvestmentDataService:
    @staticmethod
    async def get_all_investments():
        '''Lista todos os investimentos (Admin)'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{INVESTMENT_SERVICE_URL}/')
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao listar todos os investimentos')
            return response.json()

    @staticmethod
    async def get_customer_investments(customer_id: uuid.UUID):
        '''
        Busca os investimentos um cliente específico. 
        '''
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{INVESTMENT_SERVICE_URL}/customer/{customer_id}') 
            if response.status_code == 404:
                return []
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao buscar carteira do cliente')
            return response.json()

    @staticmethod
    async def get_investment_by_id(investment_id: uuid.UUID):
        '''Busca detalhes de um investimento específico'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{INVESTMENT_SERVICE_URL}/investment/{investment_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Investimento não encontrado')
            return response.json()

    @staticmethod
    async def create_investment(investment_data: dict):
        '''Registra um novo investimento no banco de dados'''
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{INVESTMENT_SERVICE_URL}/', json=investment_data)
            if response.status_code == 400:
                raise HTTPException(status_code=400, detail=response.json().get('detail', 'Dados inválidos'))
            elif response.status_code != 201:
                raise HTTPException(status_code=500, detail='Erro interno ao registrar investimento')
            return response.json()

    @staticmethod
    async def update_investment(investment_id: uuid.UUID, update_data: dict):
        '''Atualiza um investimento existente (venda parcial ou desativação)'''
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{INVESTMENT_SERVICE_URL}/investment/{investment_id}', json=update_data)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Investimento não encontrado para atualização')
            return response.json()

    @staticmethod
    async def delete_investment(investment_id: uuid.UUID):
        '''Remove permanentemente um investimento'''
        async with httpx.AsyncClient() as client:
            response = await client.delete(f'{INVESTMENT_SERVICE_URL}/investment/{investment_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Investimento não encontrado para deleção')
            return response.status_code == 204