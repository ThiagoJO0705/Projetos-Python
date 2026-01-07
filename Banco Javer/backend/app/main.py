from fastapi import FastAPI

app = FastAPI(title='Banco Javer - API de Gerenciamento de Correntistas', version='0.0.1', 
              description='API de gerenciamento de correntistas do Banco JAVER, projetada para realizar operações completas de CRUD e cálculo automatizado de score de crédito.', )