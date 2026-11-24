# PoC – Cardápio Digital com Gestão de Pedidos

## Estado atual da PoC

A Prova de Conceito (PoC) do **Cardápio Digital com Gestão de Pedidos** possui atualmente o fluxo principal da aplicação implementado e funcional.

A solução integra:

```text
Frontend
   ↓
API REST com FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

O cliente pode visualizar os produtos cadastrados, navegar pelas categorias, selecionar itens, definir quantidades e observações, montar o pedido e enviá-lo para o backend.

Os dados são processados pela API e persistidos no PostgreSQL, permitindo posteriormente a consulta dos pedidos e de seus respectivos itens.

---

# Tecnologias utilizadas

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic v2
- Uvicorn

## Banco de dados

- PostgreSQL
- psycopg
- python-dotenv

## Frontend

- HTML
- CSS
- JavaScript

## Versionamento

- Git
- GitHub

---

# Arquitetura da PoC

A aplicação foi organizada em camadas, separando a interface, a API, o acesso aos dados e o banco de dados.

```text
Cliente
   ↓
Frontend
HTML + CSS + JavaScript
   ↓
HTTP / JSON
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

O frontend consome os endpoints disponibilizados pela API.

O FastAPI recebe e valida os dados utilizando schemas Pydantic e utiliza o SQLAlchemy para realizar a comunicação com o PostgreSQL.

---

# Models implementados

Atualmente, a PoC utiliza os seguintes models principais:

```text
Category
ProductCategory
Product
Order
OrderItem
```

## Category

Representa uma categoria do cardápio, como:

```text
Lanches
Bebidas
Porções
Sobremesas
```

## Product

Representa um produto disponível no cardápio.

Entre suas informações estão:

```text
id
name
description
price
image_url
```

## ProductCategory

Realiza a associação entre produtos e categorias.

```text
Product
   ↓
ProductCategory
   ↓
Category
```

## Order

Representa um pedido realizado pelo cliente.

Atualmente armazena informações como:

```text
id
customer_name
general_notes
items
```

O nome do cliente e a observação geral são opcionais.

## OrderItem

Representa cada item pertencente a um pedido.

Contém informações como:

```text
id
order_id
product_id
quantity
unit_price
notes
```

A observação do item é opcional e pode ser utilizada para solicitações específicas, como:

```text
Sem maionese
Sem cebola
```

---

# Relacionamentos principais

## Product e Category

Produtos são associados às categorias através de `ProductCategory`.

Conceitualmente:

```text
Product
   │
   ↓
ProductCategory
   │
   ↓
Category
```

## Order e OrderItem

Um pedido pode possuir vários itens:

```text
Order
   │
   ├── OrderItem
   ├── OrderItem
   └── OrderItem
```

Cada `OrderItem` pertence a um `Order`.

## Product e OrderItem

Cada item do pedido referencia um produto existente:

```text
Order
   ↓
OrderItem
   ↓
Product
```

Dessa forma, o sistema consegue identificar o produto solicitado, sua quantidade, preço unitário e possíveis observações.

---

# Categories

As rotas de categorias estão implementadas e permitem o gerenciamento básico das categorias utilizadas pelo cardápio.

Principais operações:

```text
POST   /categories/
GET    /categories/
GET    /categories/{category_id}
DELETE /categories/{category_id}
```

Ao excluir uma categoria, as associações correspondentes em `ProductCategory` são tratadas antes da exclusão.

---

# Products

As rotas de produtos estão implementadas e integradas ao frontend.

Principais operações:

```text
POST   /products/
GET    /products/
GET    /products/{product_id}
DELETE /products/{product_id}
```

Ao cadastrar um produto, ele é associado à categoria informada.

A listagem de produtos também fornece a categoria correspondente, permitindo que o frontend organize dinamicamente o cardápio.

Existe ainda uma validação para impedir a exclusão de produtos que já estejam vinculados a itens de pedidos.

---

# Orders

## Criar pedido

```text
POST /orders/
```

O endpoint recebe o pedido completo, incluindo os itens selecionados.

Exemplo de requisição:

```json
{
  "customer_name": "Bruna",
  "general_notes": "Trazer copos e guardanapos",
  "items": [
    {
      "product_id": 2,
      "quantity": 1,
      "notes": "Sem maionese"
    },
    {
      "product_id": 3,
      "quantity": 2,
      "notes": null
    }
  ]
}
```

O nome do cliente e a observação geral são opcionais.

Para cada item, o backend consulta o produto correspondente e utiliza o preço cadastrado no banco como `unit_price`.

Após a validação, o pedido e seus itens são persistidos no PostgreSQL.

---

## Listar pedidos

```text
GET /orders/
```

Retorna os pedidos cadastrados juntamente com seus respectivos itens.

Exemplo simplificado:

```json
[
  {
    "id": 1,
    "customer_name": "Bruna",
    "general_notes": "Trazer copos e guardanapos",
    "items": [
      {
        "product_id": 2,
        "quantity": 1,
        "unit_price": 28.9,
        "notes": "Sem maionese"
      }
    ]
  }
]
```

---

## Buscar pedido por ID

```text
GET /orders/{order_id}
```

Permite consultar individualmente um pedido e seus itens.

Caso o pedido solicitado não exista, a API retorna:

```text
404 Not Found
```

---

## Excluir pedido

A PoC também possui operação para exclusão de pedidos.

Antes da exclusão do `Order`, seus respectivos `OrderItem` são removidos para respeitar os relacionamentos existentes no banco de dados.

---

# Frontend

O frontend está implementado utilizando:

```text
HTML
CSS
JavaScript
```

Ele está integrado diretamente à API FastAPI.

As funcionalidades disponíveis incluem:

- visualização dos produtos cadastrados;
- organização dos produtos por categoria;
- filtro por categoria;
- seleção de produtos;
- aumento e redução da quantidade;
- observação específica por item;
- carrinho de pedidos;
- cálculo do valor total;
- nome opcional do cliente;
- observação geral do pedido;
- envio do pedido para a API;
- retorno visual após o envio.

Os produtos exibidos no cardápio são obtidos através do backend, não sendo necessário cadastrá-los diretamente no código do frontend.

---

# Fluxo funcional da PoC

O fluxo principal atualmente implementado é:

```text
Cliente acessa o cardápio
        ↓
Frontend consulta GET /products/
        ↓
Produtos e categorias são exibidos
        ↓
Cliente seleciona os produtos
        ↓
Define quantidades e observações
        ↓
Informa nome opcional
        ↓
Informa observação geral opcional
        ↓
Carrinho calcula o valor total
        ↓
Cliente envia o pedido
        ↓
POST /orders/
        ↓
FastAPI valida os dados
        ↓
SQLAlchemy persiste os dados
        ↓
PostgreSQL armazena Order e OrderItems
        ↓
GET /orders/
        ↓
Pedido pode ser consultado com seus itens
```

Esse fluxo foi validado durante o desenvolvimento utilizando o frontend e a documentação interativa do FastAPI.

---

# Banco de dados

O backend utiliza:

```text
PostgreSQL
SQLAlchemy
psycopg
python-dotenv
```

As informações de conexão são carregadas através de variáveis de ambiente.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=digital_menu_db
DB_USER=menu_app
DB_PASSWORD=...
```

As sessões do SQLAlchemy são criadas através do `SessionLocal`.

Durante a PoC também é utilizado:

```python
Base.metadata.create_all(bind=engine)
```

para criação das tabelas que ainda não existem.

Alterações estruturais realizadas em tabelas existentes foram aplicadas diretamente no banco durante o desenvolvimento.

Para uma evolução futura do projeto, poderá ser utilizado **Alembic** para gerenciamento de migrations.

---

# Documentação da API

O FastAPI disponibiliza automaticamente a documentação OpenAPI/Swagger.

Com o backend em execução, ela pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

Por meio do Swagger é possível visualizar e testar os endpoints disponíveis.

---

# Funcionalidades implementadas

```text
PostgreSQL configurado                         ✅
Conexão com SQLAlchemy                        ✅
Models principais                             ✅
Schemas Pydantic                              ✅

Categorias                                    ✅
Cadastro de categoria                         ✅
Listagem de categorias                        ✅
Consulta de categoria                         ✅
Exclusão de categoria                         ✅

Produtos                                      ✅
Cadastro de produto                           ✅
Associação produto ↔ categoria                ✅
Listagem de produtos                          ✅
Consulta de produto                           ✅
Exclusão de produto                           ✅
Validação de produto associado a pedido       ✅

Pedidos                                       ✅
Criação de pedido com múltiplos itens         ✅
Nome opcional do cliente                      ✅
Observação geral                              ✅
Observação individual dos itens               ✅
Listagem dos pedidos com seus itens            ✅
Consulta de pedido por ID                     ✅
Exclusão de pedido                            ✅
Persistência dos pedidos no PostgreSQL        ✅

Frontend                                      ✅
Exibição dinâmica dos produtos                ✅
Filtros por categoria                         ✅
Carrinho                                      ✅
Controle de quantidade                        ✅
Cálculo do total                              ✅
Integração frontend ↔ backend                 ✅

Swagger / OpenAPI                             ✅
Versionamento com Git e GitHub                ✅
```

---

# Funcionalidades fora do escopo atual

## Mesas

A gestão de mesas foi retirada do escopo atual da PoC.

Em uma evolução futura poderão existir funcionalidades como:

```text
GET  /tables/
GET  /tables/{id}
POST /tables/
GET  /tables/{id}/orders
```

---

## Status do pedido

O acompanhamento do status do pedido não faz parte da versão atual.

Futuramente poderão ser utilizados estados como:

```text
novo
em preparo
pronto
entregue
```

e endpoints específicos para atualização do status.

---

## Usuários e autenticação

A PoC atual não possui sistema de usuários ou autenticação.

Uma evolução futura poderá incluir:

```text
User
Login
JWT
Autenticação
Autorização
Controle de acesso
```

---

## Atualização de registros

Operações de atualização através de `PUT` ou `PATCH` não fazem parte do fluxo principal implementado nesta versão da PoC.

Poderão ser adicionadas conforme a evolução do projeto.

---

# Resultado atual

A PoC demonstra atualmente um fluxo funcional de ponta a ponta:

```text
PostgreSQL
    ↑
SQLAlchemy
    ↑
FastAPI
    ↑
JavaScript
    ↑
Interface Web
    ↑
Cliente
```

O sistema permite consultar dados reais armazenados no PostgreSQL, apresentar esses dados no frontend, montar um pedido e enviá-lo através da API.

O pedido é persistido no banco juntamente com seus itens, quantidades, preços e observações, podendo posteriormente ser consultado através dos endpoints disponíveis.

Dessa forma, a PoC comprova o funcionamento da arquitetura proposta e a integração entre **frontend, backend e banco de dados**.

---

# Próximas etapas

Possíveis evoluções futuras incluem:

- criação de uma área de gerenciamento de pedidos, permitindo visualizar os pedidos recebidos e seus respectivos itens;
- acompanhamento e atualização do status dos pedidos, como `novo`, `em preparo`, `pronto` e `entregue`;
- gestão de mesas e associação dos pedidos às respectivas mesas;
- área administrativa para gerenciamento do cardápio;
- atualização de produtos e categorias;
- usuários e perfis de acesso;
- autenticação e autorização;
- migrations com Alembic;
- melhorias de interface e experiência do usuário;
- preparação da aplicação para ambiente de produção.