from fastapi import APIRouter

investments = APIRouter(prefix='/investments', tags=['investments'])

@investments.get('/me')
async def get_my_investments():
    pass

@investments.post('/buy')
async def buy_investments():
    pass

@investments.post('/register')
async def register_investments():
    pass

@investments.patch('/{investment_id}')
async def get_my_investments():
    pass

@investments.get('/{investment_id}')
async def get_my_investments():
    pass
