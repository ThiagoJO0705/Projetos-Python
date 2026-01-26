from fastapi import FastAPI

app = FastAPI(title='PyInvest - Investments API', version='0.0.1', 
              description='API de gerenciamento de investimentos do PyInvest. Oferece endpoints para manipulação e consulta de dados bancários e de mercado.')

from app_gateway.app.api.routes.customers import customers
from app_gateway.app.api.routes.assets import assets
from app_gateway.app.api.routes.investments import investments
from app_gateway.app.api.routes.analytics import analytics

app.include_router(customers)
app.include_router(assets)
app.include_router(investments)
app.include_router(analytics)