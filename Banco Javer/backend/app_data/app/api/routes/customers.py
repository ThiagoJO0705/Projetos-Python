from fastapi import APIRouter

customers = APIRouter(prefix='/customers', tags=['customers'])

@customers.post('/')
async def create_customer():
    pass

@customers.get('/')
async def get_all_customers():
    pass

@customers.get('/{customer_id}')
async def get_customer_by_id():
    pass

@customers.get('/filter')
async def filter_customer():
    pass

@customers.patch('/{customer_id}')
async def update_customer():
    pass