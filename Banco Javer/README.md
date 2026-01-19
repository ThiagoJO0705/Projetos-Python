# Banco JAVER - Sistema de Gestão de Correntistas
<div align="center">
  <img src="./frontend/images/logo-readme.png" width="500px">
</div>
<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?logo=fastapi&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)
![Coverage](https://img.shields.io/badge/Coverage-100%25-success)

</div>


## Descrição do Sistema
O Banco JAVER é uma plataforma para gerenciamento de correntistas, controle transacional e análise de crédito. O projeto foi desenvolvido sob uma arquitetura distribuída de microsserviços, garantindo o desacoplamento entre a interface de usuário, a lógica de negócio e a camada de persistência de dados.

## Arquitetura de Software
A solução é dividida em três camadas principais, seguindo padrões modernos de comunicação assíncrona e segurança.

### Aplicação Gateway (Porta 8000)
Atua como o ponto de entrada único para o usuário final. Suas responsabilidades incluem:
*   **Autenticação e Segurança:** Gestão de tokens JWT e controle de permissões de acesso diferenciados para Perfis de Administrador e Clientes.
*   **Lógica de Negócio Transacional:** Validação de integridade financeira e regras de movimentação.
*   **Motor de Crédito:** Realiza o cálculo do score de crédito (definido como 10% do saldo atual) de forma dinâmica, consumindo os dados brutos da camada de persistência.
*   **Comunicação Externa:** Utiliza o cliente assíncrono `HTTPX` para realizar requisições REST à aplicação de dados.

### Aplicação de Dados (Porta 8001)
Responsável exclusivamente pela persistência e integridade das informações no banco de dados:
*   **Operações CRUD:** Gerenciamento centralizado das entidades Clientes e Transações.
*   **Integridade Transacional:** As operações de crédito e débito são executadas em transações atômicas, garantindo a sincronia entre o saldo da conta e o registro no extrato.
*   **Armazenamento:** Utilização de SQLite para persistência local.

### Interface de Usuário (Front-end)
Interface desenvolvida com foco em usabilidade, performance e feedback visual ao usuário, utilizando JavaScript Vanilla para controle total do fluxo de eventos e requisições. O sistema implementa:
*   **Design Responsivo:** Adaptável a diferentes resoluções e dispositivos.
*   **Efeitos Visuais:** Uso de Skeleton Loading para carregamento de dados e Toasts para notificações de sistema.
*   **Segurança Visual:** Máscara de privacidade para ocultação de valores sensíveis.

## Regras de Negócio e Funcionalidades

### Gestão de Clientes
*   **Validação via Regex:** Implementação de expressões regulares para garantir a higienização dos dados. O campo Nome aceita apenas caracteres alfabéticos, enquanto CPF e Telefone são restritos a caracteres numéricos.
*   **Edição Inteligente (PATCH):** Otimização de rede através do envio exclusivo de campos que sofreram alteração no formulário.
*   **Soft Delete:** Desativação lógica de contas (campo `is_active`), preservando a integridade referencial e permitindo auditorias futuras.
*   **Trava de Segurança:** Impedimento técnico de encerramento de contas que possuam saldo residual superior a zero.

### Operações Bancárias
*   **Partida Dobrada:** Sistema de transferências onde cada débito no remetente corresponde a um crédito no destinatário, gerando registros individuais e rastreáveis.
*   **Pagamentos Multimodais:** Suporte a diferentes métodos de pagamento (Pix, TED, Boleto) com registro de descrição personalizada no extrato.

## Tecnologias Utilizadas

### Backend
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-CC0000?logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)

### Segurança & Comunicação
![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white)
![Passlib](https://img.shields.io/badge/Passlib-Bcrypt-4B8BBE)
![HTTPX](https://img.shields.io/badge/HTTPX-Async-000000)

### Front-end
![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-Grid%20%26%20Flexbox-1572B6?logo=css3&logoColor=white)

### Testes & Qualidade
![Pytest](https://img.shields.io/badge/Pytest-Testes-0A9EDC?logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-100%25-success)
![RESPX](https://img.shields.io/badge/RESPX-Mocking-000000)


## Garantia de Qualidade (Testes)
O projeto atingiu o índice de **100% de cobertura de código** (Code Coverage) em ambas as aplicações backend, validando fluxos de sucesso e exceção.
*   **Aplicação 1:** Testada via Mocks de serviço e simulação de rede com RESPX.
*   **Aplicação 2:** Testada utilizando banco de dados em memória (SQLite :memory:) para isolamento total.

## Instruções de Execução
Antes de iniciar, crie um arquivo `.env` na pasta `backend` baseando-se no `.env.example`, preenchendo obrigatoriamente a chave de segurança. As demais variáveis, como o método de criptografia e o tempo de expiração do token, já possuem valores padrão definidos para o funcionamento imediato da aplicação.

### Instalação de Dependências
```bash
cd '.\Banco Javer\
pip install -r requirements.txt
```

### Inicialização dos Serviços
Ambos os servidores devem ser iniciados simultaneamente em terminais distintos:

#### Aplicação de Dados
```bash
cd '.\Banco Javer\backend\'
uvicorn app_data.app.main:app --reload --port 8001
```

#### Aplicação Gateway
```bash
cd '.\Banco Javer\backend\'
uvicorn app_customer.app.main:app --reload --port 8000
```

### Frontend
Abra o arquivo `index.html` com a extensão do VSCode chamada Live Server

### Execução de Testes
```bash
cd '.\Banco Javer\backend\'
python -m pytest --cov=app_customer --cov=app_data
```

## Desenvolvedor
Thiago Jardim de Oliveira
