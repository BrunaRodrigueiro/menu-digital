const CONFIG = {
  API_URL: "http://localhost:8000",   // URL do backend FastAPI
  ROTA_PRODUTOS: "/produtos",         // GET  -> lista de produtos
  ROTA_PEDIDOS: "/pedidos",           // POST -> cria pedido
  USAR_MOCK_SE_FALHAR: true,          // se a API estiver fora, usa dados de exemplo
};

/* Dados de exemplo (usados só se a API não responder) */
const PRODUTOS_MOCK = [
  { id: 1, nome: "X-Burger", descricao: "Pão, hambúrguer 150g, queijo, alface e tomate.", preco: 24.9, categoria: "Lanches" },
  { id: 2, nome: "X-Bacon", descricao: "Hambúrguer 150g, queijo, bacon crocante e molho da casa.", preco: 28.9, categoria: "Lanches" },
  { id: 3, nome: "Batata Frita", descricao: "Porção individual com sal e orégano.", preco: 16.0, categoria: "Porções" },
  { id: 4, nome: "Onion Rings", descricao: "Anéis de cebola empanados.", preco: 18.5, categoria: "Porções" },
  { id: 5, nome: "Refrigerante Lata", descricao: "Coca-Cola, Guaraná ou Sprite 350ml.", preco: 6.5, categoria: "Bebidas" },
  { id: 6, nome: "Suco Natural", descricao: "Laranja, limão ou maracujá 400ml.", preco: 9.0, categoria: "Bebidas" },
  { id: 7, nome: "Brownie", descricao: "Brownie de chocolate com sorvete.", preco: 14.0, categoria: "Sobremesas" },
];

/* ---------- Estado ---------- */
let produtos = [];
let categoriaAtiva = "Todos";
let carrinho = carregarCarrinho(); // { [produtoId]: { quantidade, observacao } }

/* ---------- Atalhos DOM ---------- */
const $ = (id) => document.getElementById(id);
const el = {
  lista: $("lista"),
  categorias: $("categorias"),
  aviso: $("aviso"),
  btnCarrinho: $("btn-carrinho"),
  qtdTotal: $("qtd-total"),
  valorTotal: $("valor-total"),
  painel: $("painel"),
  itensCarrinho: $("itens-carrinho"),
  valorTotalPainel: $("valor-total-painel"),
  cliente: $("cliente"),
  obsGeral: $("obs-geral"),
  btnEnviar: $("btn-enviar"),
  btnLimpar: $("btn-limpar"),
  toast: $("toast"),
};

/* ---------- Utilidades ---------- */
const moeda = (v) =>
  Number(v || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

function escapar(texto) {
  const d = document.createElement("div");
  d.textContent = texto ?? "";
  return d.innerHTML;
}

function carregarCarrinho() {
  try {
    return JSON.parse(localStorage.getItem("carrinho")) || {};
  } catch {
    return {};
  }
}
function salvarCarrinho() {
  try {
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
  } catch { /* ignora */ }
}

let toastTimer;
function mostrarToast(msg, tipo = "") {
  el.toast.textContent = msg;
  el.toast.className = "toast " + tipo;
  el.toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.toast.hidden = true), 3000);
}

/* Normaliza os campos vindos da API (aceita variações comuns de nomes) */
function normalizarProduto(p) {
  return {
    id: p.id ?? p.id_produto,
    nome: p.nome ?? p.name ?? "Produto",
    descricao: p.descricao ?? p.description ?? "",
    preco: Number(p.preco ?? p.price ?? 0),
    categoria: p.categoria?.nome ?? p.categoria ?? p.category ?? "Outros",
    imagem: p.imagem_url ?? p.imagem ?? p.image_url ?? "",
  };
}

/* ---------- API ---------- */
async function carregarProdutos() {
  try {
    const resp = await fetch(CONFIG.API_URL + CONFIG.ROTA_PRODUTOS);
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const dados = await resp.json();
    produtos = dados.map(normalizarProduto);
  } catch (e) {
    console.warn("Falha ao buscar produtos:", e);
    if (CONFIG.USAR_MOCK_SE_FALHAR) {
      produtos = PRODUTOS_MOCK.map(normalizarProduto);
      el.aviso.textContent =
        "Não foi possível conectar à API. Exibindo dados de exemplo.";
      el.aviso.hidden = false;
    } else {
      el.lista.innerHTML = '<p class="vazio">Não foi possível carregar o cardápio.</p>';
      return;
    }
  }
  // remove do carrinho itens que não existem mais
  Object.keys(carrinho).forEach((id) => {
    if (!produtos.some((p) => String(p.id) === id)) delete carrinho[id];
  });
  renderizarCategorias();
  renderizarLista();
  atualizarCarrinho();
}

async function enviarPedido() {
  const itens = Object.entries(carrinho).map(([id, i]) => ({
    produto_id: Number(id),
    quantidade: i.quantidade,
    observacao: i.observacao || "",
  }));
  if (!itens.length) return;

  // Ajuste este payload ao schema (Pydantic) do seu backend
  const payload = {
    cliente: el.cliente.value.trim() || null,
    observacao: el.obsGeral.value.trim() || null,
    itens,
  };

  el.btnEnviar.disabled = true;
  el.btnEnviar.textContent = "Enviando...";
  try {
    const resp = await fetch(CONFIG.API_URL + CONFIG.ROTA_PEDIDOS, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    carrinho = {};
    salvarCarrinho();
    el.obsGeral.value = "";
    fecharPainel();
    renderizarLista();
    atualizarCarrinho();
    mostrarToast("Pedido enviado com sucesso! ✅", "sucesso");
  } catch (e) {
    console.error(e);
    mostrarToast("Não foi possível enviar o pedido. Tente novamente.", "erro");
  } finally {
    el.btnEnviar.disabled = false;
    el.btnEnviar.textContent = "Enviar pedido";
  }
}

/* ---------- Renderização ---------- */
function renderizarCategorias() {
  const cats = ["Todos", ...new Set(produtos.map((p) => p.categoria))];
  el.categorias.innerHTML = cats
    .map(
      (c) =>
        `<button class="chip ${c === categoriaAtiva ? "ativo" : ""}" data-cat="${escapar(c)}">${escapar(c)}</button>`
    )
    .join("");
}

function htmlProduto(p) {
  const qtd = carrinho[p.id]?.quantidade || 0;
  const foto = p.imagem
    ? `<img src="${escapar(p.imagem)}" alt="${escapar(p.nome)}" loading="lazy">`
    : `<div class="sem-foto" aria-hidden="true">🍽️</div>`;
  const acao = qtd
    ? `<div class="qtd">
         <button data-menos="${p.id}" aria-label="Diminuir">−</button>
         <span>${qtd}</span>
         <button data-mais="${p.id}" aria-label="Aumentar">+</button>
       </div>`
    : `<button class="btn-add" data-mais="${p.id}">Adicionar</button>`;
  return `
    <article class="produto">
      ${foto}
      <div class="produto-info">
        <h3>${escapar(p.nome)}</h3>
        <p>${escapar(p.descricao)}</p>
        <div class="produto-rodape">
          <span class="preco">${moeda(p.preco)}</span>
          ${acao}
        </div>
      </div>
    </article>`;
}

function renderizarLista() {
  const visiveis =
    categoriaAtiva === "Todos"
      ? produtos
      : produtos.filter((p) => p.categoria === categoriaAtiva);

  if (!visiveis.length) {
    el.lista.innerHTML = '<p class="vazio">Nenhum item disponível.</p>';
    return;
  }

  // agrupa por categoria
  const grupos = {};
  visiveis.forEach((p) => (grupos[p.categoria] ||= []).push(p));

  el.lista.innerHTML = Object.entries(grupos)
    .map(
      ([cat, itens]) =>
        `<h2 class="categoria-titulo">${escapar(cat)}</h2>${itens.map(htmlProduto).join("")}`
    )
    .join("");
}

function totais() {
  let qtd = 0, valor = 0;
  for (const [id, item] of Object.entries(carrinho)) {
    const p = produtos.find((x) => String(x.id) === id);
    if (!p) continue;
    qtd += item.quantidade;
    valor += item.quantidade * p.preco;
  }
  return { qtd, valor };
}

function atualizarCarrinho() {
  const { qtd, valor } = totais();
  el.btnCarrinho.hidden = qtd === 0;
  el.qtdTotal.textContent = qtd;
  el.valorTotal.textContent = moeda(valor);
  el.valorTotalPainel.textContent = moeda(valor);
  salvarCarrinho();
  if (!el.painel.hidden) renderizarPainel();
}

function renderizarPainel() {
  const linhas = Object.entries(carrinho)
    .map(([id, item]) => {
      const p = produtos.find((x) => String(x.id) === id);
      if (!p) return "";
      return `
        <li class="item-carrinho">
          <div class="item-linha">
            <div>
              <div class="item-nome">${escapar(p.nome)}</div>
              <div class="item-sub">${moeda(p.preco)} × ${item.quantidade} = ${moeda(p.preco * item.quantidade)}</div>
            </div>
            <div class="qtd">
              <button data-menos="${p.id}" aria-label="Diminuir">−</button>
              <span>${item.quantidade}</span>
              <button data-mais="${p.id}" aria-label="Aumentar">+</button>
            </div>
          </div>
          <input class="item-obs" data-obs="${p.id}" type="text" maxlength="120"
                 placeholder="Observação (ex.: sem cebola)" value="${escapar(item.observacao || "")}">
        </li>`;
    })
    .join("");
  el.itensCarrinho.innerHTML = linhas || '<li class="vazio">Seu pedido está vazio.</li>';
}

/* ---------- Ações do carrinho ---------- */
function alterarQuantidade(id, delta) {
  const atual = carrinho[id]?.quantidade || 0;
  const nova = atual + delta;
  if (nova <= 0) {
    delete carrinho[id];
  } else {
    carrinho[id] = { quantidade: Math.min(nova, 99), observacao: carrinho[id]?.observacao || "" };
  }
  renderizarLista();
  atualizarCarrinho();
  if (!Object.keys(carrinho).length) fecharPainel();
}

function abrirPainel() {
  renderizarPainel();
  el.painel.hidden = false;
  document.body.style.overflow = "hidden";
}
function fecharPainel() {
  el.painel.hidden = true;
  document.body.style.overflow = "";
}

/* ---------- Eventos ---------- */
document.addEventListener("click", (e) => {
  const mais = e.target.closest("[data-mais]");
  const menos = e.target.closest("[data-menos]");
  const chip = e.target.closest("[data-cat]");

  if (mais) return alterarQuantidade(mais.dataset.mais, +1);
  if (menos) return alterarQuantidade(menos.dataset.menos, -1);
  if (chip) {
    categoriaAtiva = chip.dataset.cat;
    renderizarCategorias();
    renderizarLista();
    window.scrollTo({ top: 0, behavior: "smooth" });
    return;
  }
  if (e.target.closest("[data-fechar]")) fecharPainel();
});

el.itensCarrinho.addEventListener("input", (e) => {
  const campo = e.target.closest("[data-obs]");
  if (!campo || !carrinho[campo.dataset.obs]) return;
  carrinho[campo.dataset.obs].observacao = campo.value;
  salvarCarrinho();
});

el.btnCarrinho.addEventListener("click", abrirPainel);
el.btnEnviar.addEventListener("click", enviarPedido);
el.btnLimpar.addEventListener("click", () => {
  carrinho = {};
  renderizarLista();
  atualizarCarrinho();
  fecharPainel();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !el.painel.hidden) fecharPainel();
});

/* ---------- Início ---------- */
carregarProdutos();
