# Banco JAVER - API de Gestão de Correntistas

## Descrição do Projeto
O sistema Banco JAVER é uma solução de backend robusta desenvolvida para a gestão centralizada de clientes, operações financeiras e análise de crédito automatizada. A aplicação utiliza o framework FastAPI para fornecer alta performance e baixa latência, integrando práticas avançadas de segurança e integridade transacional.

O projeto foi concebido para atender a requisitos rigorosos de lógica de negócio, consolidando camadas de persistência, segurança e processamento de dados em uma arquitetura modular que garante a consistência das operações bancárias.

## Arquitetura e Design de Software
A aplicação adota os princípios de Clean Architecture e Separation of Concerns (SoC), sendo estruturada nas seguintes camadas:

- Camada de API: Gerenciamento de endpoints, protocolos de comunicação e injeção de dependências.
- Camada de Domínio (Models): Definição das entidades de negócio e mapeamento objeto-relacional (ORM).
- Camada de Esquemas (Schemas): Validação estrita de dados e contratos de interface via Pydantic V2.
- Camada de Segurança: Implementação de autenticação OAuth2 com tokens JWT e hashing de credenciais com algoritmo Bcrypt.
- Camada de Persistência: Gerenciamento de banco de dados SQLite com controle de versionamento de esquema via Alembic.

## Funcionalidades Principais

### Gestão de Correntistas (CRUD)
- Cadastro de novos clientes com validação de unicidade para E-mail, CPF e Telefone.
- Atualização parcial de dados via método PATCH com proteção de campos sensíveis.
- Listagem administrativa com filtros dinâmicos de busca por nome e status de conta.

### Motor de Crédito
- Cálculo de Score de Crédito dinâmico e em tempo real, definido como 10% do saldo atual em conta corrente.
- Lógica de persistência efêmera: o score é calculado sob demanda para garantir a precisão dos dados exibidos.

### Operações Bancárias (Banking)
- Depósitos com registro automático no histórico de transações.
- Pagamento de contas com seleção de método (Boleto, Pix, TED, etc.).
- Transferência via Pix entre usuários utilizando o princípio de partida dobrada (Double-entry bookkeeping), onde cada operação gera simultaneamente um registro de débito para o remetente e um de crédito para o destinatário dentro de uma transação atômica.

### Controle Administrativo
- Sistema de Soft Delete: desativação lógica de contas para preservação de histórico e auditoria.
- Mecanismos de segurança contra autodesativação de administradores.
- Trava de continuidade de negócio para garantir a existência de ao menos um administrador ativo no sistema.

## Tecnologias Utilizadas
- Linguagem: Python 3.12+
- Framework Web: FastAPI
- ORM: SQLAlchemy 2.0
- Migrações: Alembic
- Validação: Pydantic V2
- Segurança: Python-jose (JWT) e Passlib (Bcrypt)
- Testes: Pytest e Pytest-Cov

## Configuração e Instalação

### Pré-requisitos
- Python instalado no ambiente de execução.
- Gerenciador de dependências pip.

### Procedimento de Instalação
1. Realize o clone do repositório para sua máquina local.
2. Navegue até o diretório raiz do projeto (`backend`).
3. Execute a instalação global das dependências:
```bash
pip install -r requirements.txt
```

### Gestão do Banco de Dados
Para inicializar a estrutura das tabelas e aplicar as restrições de integridade, execute as migrações:
```bash
alembic upgrade head
```

### Configuração das Variáveis de Ambiente
O projeto utiliza variáveis de ambiente para gerenciar chaves de segurança e conexões.
1. Na pasta `backend`, localize o arquivo `.env.example`.
2. Crie uma cópia deste arquivo e renomeie para `.env`.
3. Preencha a `SECRET_KEY` com uma hash segura.

### Execução da Aplicação
Para iniciar o servidor em ambiente de desenvolvimento, execute o comando abaixo a partir do diretório raiz do backend:
```bash
python -m uvicorn app.main:app --reload
```

### Garantia de Qualidade e Cobertura de Testes
O projeto foi submetido a rigorosos testes unitários e de integração para validar todos os fluxos de sucesso e exceção. Foi atingido o índice de 100% de cobertura de código.

- Para executar a suíte de testes:
```bash
python -m pytest
```

- Para gerar o relatório de cobertura no terminal:
```bash
python -m pytest --cov=app tests/
```

- Para gerar o relatório detalhado em formato HTML:
```bash
python -m pytest --cov=app --cov-report=html tests/
```

## Desenvolvedor
Thiago Jardim de Oliveira