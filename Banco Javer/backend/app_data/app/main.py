from fastapi import FastAPI

app = FastAPI(title='Banco Javer - Database API', version='0.0.1', 
              description='API para realizar CRUD do banco de dados do Banco Javer', )


from app.api.routes.customers import customers
from app.api.routes.transactions import transactions

app.include_router(customers)
app.include_router(transactions)