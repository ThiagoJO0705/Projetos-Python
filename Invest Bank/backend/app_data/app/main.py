from fastapi import FastAPI

app = FastAPI(title='PyInvest - Database API', version='0.0.1', 
              description='API para realizar CRUD do banco de dados do PyInvest', )

from app_data.app.api.routes.customers import customers
from app_data.app.api.routes.assets import assets
from app_data.app.api.routes.investments import investments

app.include_router(customers)
app.include_router(assets)
app.include_router(investments)