import httpx
import uuid
from fastapi import HTTPException

ASSET_SERVICE_URL = 'http://localhost:8004/assets'

class AssetDataService:
    @staticmethod
    async def get_all_assets():
        '''Retorna todos os ativos cadastrados no banco'''
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(f'{ASSET_SERVICE_URL}/')
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao listar ativos')
            return response.json()

    @staticmethod
    async def get_asset_by_ticker(ticker: str):
        '''Busca um ativo pelo Ticker'''
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(f'{ASSET_SERVICE_URL}/{ticker.upper()}')
            if response.status_code == 404:
                return None
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail='Erro ao buscar ativo por ticker')
            return response.json()

    @staticmethod
    async def create_asset(asset_data: dict):
        '''Cadastra um novo ativo no banco de dados.'''
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f'{ASSET_SERVICE_URL}/', json=asset_data)
            if response.status_code == 400:
                raise HTTPException(status_code=400, detail='Ativo já cadastrado ou dados inválidos')
            elif response.status_code != 201:
                raise HTTPException(status_code=500, detail='Erro ao cadastrar ativo no Data Service')
            return response.json()
