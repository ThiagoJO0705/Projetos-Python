from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


app = FastAPI(title='API de Monitoramento de Ativos Financeiros', version='0.0.1', 
              description='API de monitoramento de ativos financeir, oferecendo cotações em tempo real e dados históricos para ações, FIIs e criptomoedas.')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/signin-form')


from app.api.routes.auth import auth
from app.api.routes.assets import assets
from app.api.routes.transactions import transactions 
from app.api.routes.profile import profile 

app.include_router(auth)
app.include_router(assets)
app.include_router(transactions)
app.include_router(profile)
