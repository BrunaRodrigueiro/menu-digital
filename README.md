# 🍔 Cardápio Digital

Prova de conceito (PoC) de um sistema de **cardápio digital com gestão de pedidos para pequenos estabelecimentos gastronômicos**, desenvolvida como Projeto Integrador do curso de **Análise e Desenvolvimento de Sistemas (SENAC)**.

## Sobre o projeto

Muitos pequenos estabelecimentos ainda utilizam PDFs, imagens ou links de armazenamento em nuvem como cardápio, o que pode dificultar a atualização das informações e tornar o processo de realização dos pedidos menos organizado.

O projeto propõe uma solução web em que o cliente pode visualizar o cardápio pelo celular, consultar os produtos disponíveis, selecionar itens, informar quantidades e observações e enviar o pedido de forma organizada.

A aplicação integra frontend, API e banco de dados, permitindo que os produtos cadastrados no sistema sejam exibidos dinamicamente no cardápio e que os pedidos realizados sejam armazenados para consulta.

## Escopo da PoC

A versão atual da PoC contempla o fluxo principal do sistema:

- Cadastro e consulta de categorias;
- Cadastro e consulta de produtos;
- Associação de produtos às suas respectivas categorias;
- Exibição dinâmica do cardápio no frontend;
- Organização dos produtos por categoria;
- Adição e remoção de itens no carrinho;
- Definição da quantidade de cada produto;
- Inclusão de observações nos itens do pedido;
- Cálculo do valor total do pedido;
- Envio do pedido pelo frontend para a API;
- Armazenamento dos pedidos e seus itens no PostgreSQL;
- Consulta de pedidos realizados;
- Exclusão de categorias, produtos e pedidos, respeitando as validações implementadas.

A PoC tem como objetivo demonstrar o funcionamento do fluxo principal e a integração entre as diferentes camadas da aplicação.

Funcionalidades como **gestão de mesas, acompanhamento do status dos pedidos, usuários, login e autenticação** não fazem parte do escopo atual e poderão ser desenvolvidas em etapas futuras.

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Banco de dados

- PostgreSQL

### Frontend

- HTML
- CSS
- JavaScript

### Versionamento

- Git
- GitHub

## Estrutura do projeto

```text
menu-digital/
│
├── backend/
│   └── app/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Funcionamento

O fluxo principal da aplicação ocorre da seguinte forma:

```text
Cliente
   ↓
Frontend (HTML, CSS e JavaScript)
   ↓
API REST (FastAPI)
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

O frontend consulta os produtos disponibilizados pela API e monta o cardápio dinamicamente. Após selecionar os produtos desejados, o cliente pode montar seu pedido e enviá-lo para o backend.

A API recebe os dados, realiza as operações necessárias e persiste o pedido e seus respectivos itens no banco de dados PostgreSQL.

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/BrunaRodrigueiro/menu-digital.git
cd menu-digital
```

### 2. Crie e ative o ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um arquivo `.env` dentro de `backend/app` utilizando as configurações necessárias para conexão com o PostgreSQL.

Utilize o arquivo `.env.example` como referência para as variáveis de ambiente necessárias.

### 5. Execute o backend

A partir do diretório `backend/app`:

```bash
uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa do FastAPI poderá ser acessada em:

```text
http://127.0.0.1:8000/docs
```

### 6. Execute o frontend

Abra a pasta `frontend` utilizando um servidor local, como o **Live Server** do Visual Studio Code.

Com o backend em execução, o frontend poderá consumir os dados disponibilizados pela API.

## Principais endpoints

A API possui endpoints para gerenciamento dos principais recursos da PoC:

```text
/categories/          Categorias
/products/            Produtos
/orders/              Pedidos
```

A documentação completa e os métodos disponíveis podem ser consultados pelo Swagger em `/docs` durante a execução da API.

## Próximas evoluções

Como continuidade do projeto, poderão ser implementadas funcionalidades como:

- Gestão de mesas;
- Status e acompanhamento dos pedidos;
- Área administrativa;
- Cadastro e gerenciamento de usuários;
- Autenticação e autorização;
- Melhorias na interface e experiência do usuário;
- Evolução da aplicação para uso em ambiente de produção.

## Integrantes

- Bruna Rodrigueiro Dias (BrunaRodrigueiro)
- Thais Helena Bezerra Da Silva (thaishbs)
- Marco Antonio Neves Souza (marconevesz)
- Priscila Alexsandra De Oliveira Ferreira (PRISCILA2025)
- Camila Sayaka Hiura (camilasayaka)