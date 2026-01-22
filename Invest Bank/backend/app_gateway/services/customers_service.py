import httpx
import uuid
from fastapi import HTTPException, status
from typing import List, Optional

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

