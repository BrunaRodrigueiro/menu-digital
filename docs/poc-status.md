# POC – Cardápio Digital com Gestão de Pedidos

## Objetivo atual

Nesta etapa da POC, o objetivo foi estruturar o backend básico do sistema, estabelecer a comunicação com o PostgreSQL e validar o fluxo principal de criação e consulta de pedidos.

A implementação atual está focada em:

- configuração do PostgreSQL;
- conexão com SQLAlchemy;
- criação dos models;
- criação dos schemas;
- criação de pedidos;
- adição de itens aos pedidos;
- listagem de pedidos;
- consulta de pedido por ID;
- relacionamento entre `Order`, `OrderItem` e `Product`;
- documentação automática via Swagger/OpenAPI.

Funcionalidades de exclusão, mesas, status do pedido e autenticação ficaram para etapas posteriores.

---

# Models criados

Atualmente foram criados os seguintes models:

```text
Category
ProductCategory
Product
Order
OrderItem
```

Nesta etapa, o fluxo efetivamente implementado e testado está concentrado principalmente em:

```text
Order
OrderItem
Product
```

O `Product` é necessário porque cada `OrderItem` possui uma chave estrangeira apontando para um produto existente.

---

# Schemas criados

Os schemas principais do projeto já foram preparados para permitir a continuidade da implementação.

Foram criados schemas relacionados a:

```text
Category
Product
Order
OrderItem
```

O projeto utiliza **Pydantic v2**.

Por isso, para leitura de objetos vindos do SQLAlchemy, é utilizada a configuração:

```python
model_config = ConfigDict(from_attributes=True)
```

em substituição ao antigo:

```python
class Config:
    orm_mode = True
```

utilizado no Pydantic v1.

---

# ORDERS

## Funcionalidades implementadas

### Criar pedido

```text
POST /orders/
```

Cria uma nova comanda/pedido.

Atualmente o model `Order` possui apenas o campo `id`, que é gerado automaticamente pelo banco.

Por esse motivo, essa rota não necessita de body.

Exemplo de resposta:

```json
{
  "id": 1
}
```

---

### Adicionar item ao pedido

Endpoint responsável pela criação de um `OrderItem` vinculado a um pedido existente.

Exemplo de body:

```json
{
  "id": 1,
  "order_id": 1,
  "product_id": 1,
  "quantity": 2,
  "unit_price": 25.90,
  "notes": "Sem cebola"
}
```

Para que o item seja criado corretamente:

```text
order_id
→ precisa corresponder a um Order existente

product_id
→ precisa corresponder a um Product existente
```

Cada chamada cria um novo `OrderItem`.

Assim, um mesmo pedido pode possuir vários itens.

---

### Listar todos os pedidos

```text
GET /orders/
```

Retorna os pedidos cadastrados no banco.

A consulta utiliza:

```python
orders = session.query(Order).all()
```

---

### Buscar pedido por ID

```text
GET /orders/{order_id}
```

Busca um único `Order` através do seu ID.

Exemplo:

```text
GET /orders/2
```

Além do ID do pedido, o endpoint retorna todos os `OrderItem` associados a ele.

Exemplo:

```json
{
  "id": 2,
  "items": [
    {
      "id": 7,
      "order_id": 2,
      "product_id": 1,
      "quantity": 2,
      "unit_price": 25.9,
      "notes": "Sem cebola"
    }
  ]
}
```

Caso o pedido solicitado não exista, é retornado:

```text
404 Not Found
```

com:

```json
{
  "detail": "Pedido não encontrado"
}
```

---

# Relacionamento Order e OrderItem

`Order` representa a comanda/pedido.

Atualmente:

```text
Order
└── id
```

`OrderItem` representa cada item adicionado àquela comanda.

Exemplo:

```text
Order 2
├── OrderItem 6
├── OrderItem 7
└── OrderItem 8
```

O relacionamento existente no model `Order` permite acessar:

```python
order.items
```

e obter todos os itens vinculados ao pedido.

Conceitualmente:

```text
Order
   │
   └── vários OrderItems
              │
              └── cada OrderItem referencia um Product
```

---

# Banco de dados

O backend utiliza:

```text
PostgreSQL
SQLAlchemy
psycopg
python-dotenv
```

As informações de conexão são carregadas através do arquivo `.env`.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=digital_menu_db
DB_USER=menu_app
DB_PASSWORD=...
```

A criação da engine é realizada pelo SQLAlchemy e as sessões são criadas através do `SessionLocal`.

Durante a POC, também está sendo utilizado:

```python
Base.metadata.create_all(bind=engine)
```

para criar automaticamente as tabelas que ainda não existem.

Em uma etapa posterior, poderá ser utilizado **Alembic** para gerenciamento das migrations.

---

# Fluxo implementado da POC

O fluxo atualmente validado é:

```text
Criar Order
     ↓
POST /orders/
     ↓
Banco gera o order_id
     ↓
Adicionar OrderItem
     ↓
informar order_id + product_id
     ↓
OrderItem é salvo no PostgreSQL
     ↓
GET /orders/
     ↓
listar os pedidos cadastrados
     ↓
GET /orders/{order_id}
     ↓
consultar um pedido específico
     ↓
retornar o Order e seus OrderItems
```

Esse fluxo foi testado com sucesso através do Swagger.

---

# O que já está implementado

```text
Configuração do PostgreSQL                 ✅
Conexão com SQLAlchemy                     ✅
Models principais                          ✅
Schemas principais                         ✅
Model Category                              ✅
Model Product                               ✅
Model ProductCategory                       ✅
Model Order                                 ✅
Model OrderItem                             ✅
Relacionamento Order ↔ OrderItem            ✅
Relacionamento Product ↔ OrderItem          ✅
POST para criação de Order                  ✅
POST para criação de OrderItem              ✅
GET para listagem de Orders                 ✅
GET de Order por ID                         ✅
Retorno dos itens de um Order               ✅
Tratamento de Order inexistente com 404     ✅
Swagger / OpenAPI                           ✅
Persistência no PostgreSQL                  ✅
```

---

# Funcionalidades ainda não implementadas

## Exclusão

Nenhuma funcionalidade `DELETE` foi implementada nesta etapa.

Futuramente poderão ser adicionados endpoints como:

```text
DELETE /products/{id}
DELETE /categories/{id}
DELETE /orders/{id}
```

A implementação deverá considerar os relacionamentos existentes e as restrições de chave estrangeira.

---

## Atualização

Operações de atualização também ficarão para uma próxima etapa.

Exemplos futuros:

```text
PUT   /products/{id}
PUT   /categories/{id}
PATCH /orders/{id}/status
```

---

## Tables

A entidade e o fluxo relacionados às mesas foram retirados temporariamente do escopo da POC atual.

Planejamento futuro:

```text
GET  /tables
GET  /tables/{id}
POST /tables
GET  /tables/{id}/orders
```

A ideia é posteriormente relacionar o pedido à mesa responsável por aquela comanda.

---

## Status do pedido

O campo de status também ficou para uma próxima etapa.

Futuramente poderá existir:

```text
PATCH /orders/{id}/status
```

com estados como:

```text
novo
em preparo
pronto
entregue
```

---

## Usuários e autenticação

Ainda não foi implementada autenticação de usuários.

Essa etapa deverá incluir futuramente:

```text
User
Login
Autenticação
JWT
Controle de acesso
```

Possíveis perfis poderão ser definidos posteriormente de acordo com a necessidade do sistema, por exemplo:

```text
Administrador
Atendente
Cozinha
```

---

# Products e Categories

Os **models e schemas** dessas entidades já foram preparados.

As rotas completas ainda serão desenvolvidas.

Estrutura planejada:

```text
PRODUCTS

GET  /products
GET  /products/{id}
POST /products
```

e:

```text
CATEGORIES

GET  /categories
GET  /categories/{id}
POST /categories
```

Funcionalidades de atualização e exclusão poderão ser adicionadas posteriormente.

---

# Estado atual da POC

Nesta etapa, a POC já consegue demonstrar o fluxo principal:

```text
Produto existente
        ↓
Criar pedido
        ↓
Adicionar item ao pedido
        ↓
Persistir no PostgreSQL
        ↓
Listar pedidos
        ↓
Consultar um pedido específico
        ↓
Visualizar seus itens
```

O objetivo atual não é implementar todas as funcionalidades de um sistema final, mas comprovar que a arquitetura básica, a API, os relacionamentos e a persistência dos pedidos estão funcionando corretamente.

As funcionalidades de **DELETE, UPDATE, TABLE, STATUS e USER/LOGIN** serão evoluções posteriores do projeto.


---


## Frontend

O frontend ainda será desenvolvido.

A definição visual e a implementação da interface serão trabalhadas posteriormente pela equipe.

Nesta etapa, o foco ficou concentrado no backend e na validação do fluxo principal da POC através da API e do Swagger.

O frontend deverá contemplar, futuramente, funcionalidades como:

```text
Visualização do cardápio
Seleção de produtos
Definição de quantidade
Observações do pedido
Carrinho
Envio do pedido
Consulta/visualização dos pedidos
Integração com os endpoints do backend
```

A equipe responsável pelo frontend irá avaliar e definir a implementação visual e técnica nesta semana.

Até o momento, o backend já fornece a base necessária para iniciar essa integração, principalmente através das rotas de criação e consulta de pedidos.

---

# Próximas etapas do projeto

As próximas evoluções previstas incluem:

```text
Desenvolvimento do frontend
Integração frontend ↔ backend
Rotas de Product
Rotas de Category
Operações de atualização
Operações de exclusão
Table
Status do pedido
User / Login
Autenticação com JWT
```

O escopo poderá ser ajustado conforme a evolução da POC e a divisão das responsabilidades entre os integrantes da equipe.