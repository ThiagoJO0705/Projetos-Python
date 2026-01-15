from fastapi import APIRouter

transactions = APIRouter(prefix='/transactions', tags=['transactions'])

@transactions.post('/')
async def post_transaction():
    pass

@transactions.get('/customer/{customer_id}')
async def get_customer_transactions():
    pass