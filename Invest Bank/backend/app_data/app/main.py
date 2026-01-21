from fastapi import FastAPI

app = FastAPI(title='Invest Bank - Database API', version='0.0.1', 
              description='API para realizar CRUD do banco de dados do Invest Bank', )

from app_data.app.api.routes.customers import customers
from app_data.app.api.routes.assets import assets

app.include_router(customers)
app.include_router(assets)