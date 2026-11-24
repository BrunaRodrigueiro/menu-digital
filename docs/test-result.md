## Teste: Envio de pedido

- Cenário:
Cliente seleciona produtos no cardápio, informa quantidade,
observações e nome e envia o pedido.

- Resultado esperado:
O pedido deve ser enviado para a API e armazenado no PostgreSQL.

- Resultado obtido:
Pedido criado com sucesso. Os dados do cliente, observação geral,
itens, quantidades, preços e observações dos itens foram persistidos
e retornados pelo endpoint GET /orders/.

Status: Aprovado.