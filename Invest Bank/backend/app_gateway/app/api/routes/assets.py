from fastapi import APIRouter

assets = APIRouter(prefix='/assets', tags=['assets'])

@assets.get('/search/{ticker}')
async def serch_investment_by_ticker():
    pass

@assets.get('/search/{name}')
async def serch_investment_by_name():
    pass

@assets.get('/trending')
async def get_trends():
    pass