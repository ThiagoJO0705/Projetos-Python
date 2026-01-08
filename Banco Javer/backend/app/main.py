from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

app = FastAPI(title='Banco Javer - API de Gerenciamento de Correntistas', version='0.0.1', 
              description='API de gerenciamento de correntistas do Banco JAVER, projetada para realizar operações completas de CRUD e cálculo automatizado de score de crédito.', )

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/signin-form')


from api.routes.auth import auth

app.include_router(auth)