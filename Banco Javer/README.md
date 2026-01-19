# Banco JAVER - Sistema de Gestão de Correntistas
<div align="center">
  <img src="./frontend/images/logo-readme.png" width="500px">
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
Interface desenvolvida em HTML5, CSS3 e JavaScript puro (Vanilla), integrada às APIs via protocolo HTTP/JSON. O sistema implementa:
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
*   **Linguagem:** Python 3.12+
*   **Framework Backend:** FastAPI
*   **ORM:** SQLAlchemy 2.0
*   **Comunicação:** HTTPX (Async)
*   **Segurança:** JWT (JSON Web Token) e Passlib (Bcrypt)
*   **Interface:** JavaScript Vanilla, CSS Grid e Flexbox
*   **Qualidade:** Pytest, Coverage, Pytest-Mock e RESPX

## Garantia de Qualidade (Testes)
O projeto atingiu o índice de **100% de cobertura de código** (Code Coverage) em ambas as aplicações backend, validando fluxos de sucesso e exceção.
*   **Aplicação 1:** Testada via Mocks de serviço e simulação de rede com RESPX.
*   **Aplicação 2:** Testada utilizando banco de dados em memória (SQLite :memory:) para isolamento total.

## Instruções de Execução

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

### Inicialização dos Serviços
Ambos os servidores devem ser iniciados simultaneamente em terminais distintos:

#### Aplicação de Dados
```bash
cd '.\Banco Javer\backend\app_data\'
python -m uvicorn app.main:app --port 8001
```

#### Aplicação Gateway
```bash
cd '.\Banco Javer\backend\app_customer\'
python -m uvicorn app.main:app --port 8000
```

### Execução de Testes
```bash
cd '.\Banco Javer\backend\'
python -m pytest --cov=app_customer --cov=app_data
```

## Desenvolvedor
Thiago Jardim de Oliveira
