import httpx
from fastapi import HTTPException
from decimal import Decimal

BASE_URL = "http://127.0.0.1:8001/customers"

class CustomerService:
    @staticmethod
    def calculate_score(balance: Decimal) -> Decimal:
        """Cálculo do score do cliente"""
        return round(Decimal(str(balance)) * Decimal('0.1'), 2)

    @staticmethod
    async def create(data: dict):
        '''Cadastra o cliente no banco de dados'''
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/", json=data)
            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
            return response.json()
