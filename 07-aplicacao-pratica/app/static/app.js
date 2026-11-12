// Front-end da rede social: chama a API Flask e mostra o Cypher que rodou no Neo4j.
const $ = (sel) => document.querySelector(sel);
const estado = { usuarios: [], atual: null, aba: "posts" };

// ------------------------------------------------------------------ utilitários
async function api(metodo, url, corpo) {
  const resp = await fetch(url, {
    method: metodo,
    headers: corpo ? { "Content-Type": "application/json" } : {},
    body: corpo ? JSON.stringify(corpo) : undefined,
  });
  const json = await resp.json().catch(() => ({ erro: `HTTP ${resp.status}` }));
  if (json.cypher && json.cypher.length) mostrarCypher(json.cypher);
  if (!resp.ok) { toast(json.erro || `Erro ${resp.status}`, true); throw new Error(json.erro); }
  return json.dados;
}

function mostrarCypher(lista) {
  $("#cypher").textContent = lista
    .map((c) => `${c.query}\n// parâmetros: ${JSON.stringify(c.params)}`)
    .join("\n\n");
}

function toast(msg, erro = false) {
  const t = $("#toast");
  t.textContent = msg; t.className = erro ? "erro" : ""; t.hidden = false;
  clearTimeout(t._timer); t._timer = setTimeout(() => (t.hidden = true), 3500);
}

function el(tag, attrs = {}, ...filhos) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => (k.startsWith("on") ? e.addEventListener(k.slice(2), v) : e.setAttribute(k, v)));
  filhos.flat().forEach((f) => e.append(f instanceof Node ? f : document.createTextNode(f ?? "")));
  return e;
}

const dadosForm = (form) => Object.fromEntries(new FormData(form).entries());
const dataBr = (iso) => (iso ? new Date(iso).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "");

// ------------------------------------------------------------------ usuários
async function carregarUsuarios() {
  estado.usuarios = await api("GET", "/api/usuarios");
  const ul = $("#lista-usuarios");
  ul.replaceChildren(...estado.usuarios.map((u) =>
    el("li", { class: u.username === estado.atual ? "sel" : "", onclick: () => abrirPerfil(u.username) },
      el("span", {}, u.nome), el("small", { class: "muted" }, `${u.seguidores} seg.`))));
  document.querySelectorAll(".sel-usuarios").forEach((sel) => {
    const valor = sel.value;
    sel.replaceChildren(...estado.usuarios.map((u) => el("option", { value: u.username }, u.nome)));
    if (valor) sel.value = valor;
  });
}

async function abrirPerfil(username) {
  estado.atual = username;
  const p = await api("GET", `/api/usuarios/${username}`);
  $("#perfil-vazio").hidden = true; $("#perfil").hidden = false;
  $("#p-nome").textContent = p.nome;
  $("#p-username").textContent = p.username;
  $("#p-cidade").textContent = p.cidade || "—";
  $("#p-bio").textContent = p.bio || "";
  $("#p-seguidores").textContent = p.seguidores.length;
  $("#p-seguindo").textContent = p.seguindo.length;
  $("#p-interesses").replaceChildren(...p.interesses.map((i) => el("span", { class: "chip" }, i)));

  const f = $("#form-editar");
  f.nome.value = p.nome; f.cidade.value = p.cidade || ""; f.bio.value = p.bio || "";
  f.interesses.value = p.interesses.join(", ");

  $("#p-lista-seguindo").replaceChildren(...p.seguindo.map((s) =>
    el("span", { class: "chip" }, s.nome,
      el("button", { title: "Deixar de seguir (DELETE da aresta)", onclick: () => deixarDeSeguir(s.username) }, "×"))));

  estado.perfil = p;
  document.querySelectorAll("#lista-usuarios li").forEach((li, i) =>
    li.classList.toggle("sel", estado.usuarios[i]?.username === username));
  await Promise.all([carregarSugestoes(), renderizarAba()]);
}

async function carregarSugestoes() {
  const sugs = await api("GET", `/api/usuarios/${estado.atual}/sugestoes`);
  $("#sugestoes").replaceChildren(...(sugs.length ? sugs.map((s) => {
    const motivo = [
      s.amigosEmComum.length ? `segue: ${s.amigosEmComum.join(", ")}` : "",
      s.interessesEmComum.length ? `curte: ${s.interessesEmComum.join(", ")}` : "",
    ].filter(Boolean).join(" · ");
    return el("li", {},
      el("div", {}, el("b", {}, s.nome), el("div", { class: "muted" }, motivo)),
      el("button", { class: "leve", onclick: () => seguir(s.username) }, "Seguir"));
  }) : [el("li", { class: "muted" }, "Sem sugestões — siga alguém primeiro.")]));
}

async function renderizarAba() {
  const ul = $("#posts");
  let itens;
  if (estado.aba === "feed") {
    itens = await api("GET", `/api/usuarios/${estado.atual}/feed`);
  } else {
    itens = estado.perfil.posts.map((p) => ({ ...p, autor: estado.atual, autorNome: estado.perfil.nome }));
  }
  ul.replaceChildren(...(itens.length ? itens.map(itemPost) : [el("li", { class: "muted" }, "Nada por aqui ainda.")]));
}

function itemPost(p) {
  const meu = p.autor === estado.atual;
  const acoes = meu
    ? [el("button", { class: "leve", onclick: () => editarPost(p) }, "Editar"),
       el("button", { class: "leve perigo", onclick: () => excluirPost(p.id) }, "Excluir")]
    : [el("button", { class: "leve", onclick: () => curtir(p.id) }, "♥ Curtir")];
  return el("li", {},
    el("div", {}, p.conteudo),
    el("div", { class: "meta" },
      el("span", {}, `${p.autorNome} · ${dataBr(p.criadoEm)} · ♥ ${p.curtidas}`),
      el("span", {}, ...acoes)));
}

// ------------------------------------------------------------------ ações
async function recarregar() {
  await carregarUsuarios();
  if (estado.atual) await abrirPerfil(estado.atual);
  carregarGrafo();
}

async function seguir(alvo) {
  await api("POST", `/api/usuarios/${estado.atual}/seguir/${alvo}`);
  toast("Agora seguindo!"); recarregar();
}

async function deixarDeSeguir(alvo) {
  await api("DELETE", `/api/usuarios/${estado.atual}/seguir/${alvo}`);
  toast("Relacionamento SEGUE removido."); recarregar();
}

async function editarPost(p) {
  const novo = prompt("Novo conteúdo do post:", p.conteudo);
  if (!novo || novo === p.conteudo) return;
  await api("PUT", `/api/posts/${p.id}`, { conteudo: novo });
  toast("Post atualizado."); recarregar();
}

async function excluirPost(id) {
  if (!confirm("Excluir este post?")) return;
  await api("DELETE", `/api/posts/${id}`);
  toast("Post excluído."); recarregar();
}

async function curtir(id) {
  await api("POST", `/api/posts/${id}/curtir/${estado.atual}`);
  toast("Curtido!"); renderizarAba(); carregarGrafo();
}

$("#form-criar").addEventListener("submit", async (e) => {
  e.preventDefault();
  const u = await api("POST", "/api/usuarios", dadosForm(e.target));
  e.target.reset(); toast(`Usuário ${u.nome} criado.`);
  estado.atual = u.username; recarregar();
});

$("#form-editar").addEventListener("submit", async (e) => {
  e.preventDefault();
  await api("PUT", `/api/usuarios/${estado.atual}`, dadosForm(e.target));
  toast("Usuário atualizado."); recarregar();
});

$("#btn-excluir").addEventListener("click", async () => {
  if (!confirm(`Excluir @${estado.atual}, seus posts e todos os relacionamentos?`)) return;
  await api("DELETE", `/api/usuarios/${estado.atual}`);
  toast("Usuário excluído (DETACH DELETE).");
  estado.atual = null; $("#perfil").hidden = true; $("#perfil-vazio").hidden = false;
  recarregar();
});

$("#form-seguir").addEventListener("submit", (e) => { e.preventDefault(); seguir(e.target.alvo.value); });

$("#form-post").addEventListener("submit", async (e) => {
  e.preventDefault();
  await api("POST", `/api/usuarios/${estado.atual}/posts`, dadosForm(e.target));
  e.target.reset(); toast("Post publicado."); recarregar();
});

$("#form-caminho").addEventListener("submit", async (e) => {
  e.preventDefault();
  const { de, para } = dadosForm(e.target);
  const alvo = $("#caminho-resultado");
  try {
    const r = await api("GET", `/api/caminho?de=${encodeURIComponent(de)}&para=${encodeURIComponent(para)}`);
    alvo.replaceChildren(el("b", {}, `${r.graus} grau(s): `), r.pessoas.join(" → "));
  } catch { alvo.textContent = ""; }
});

document.querySelectorAll(".abas button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".abas button").forEach((x) => x.classList.toggle("ativa", x === b));
  estado.aba = b.dataset.aba; renderizarAba();
}));

// ------------------------------------------------------------------ visualização do grafo
const CORES = { Usuario: "#2f5bd3", Post: "#e08a1e", Interesse: "#2a9d6f" };
let rede;

async function carregarGrafo() {
  if (!window.vis) { $("#grafo").textContent = "Biblioteca de visualização indisponível (sem internet?)."; return; }
  const resp = await fetch("/api/grafo").then((r) => r.json());
  if (!resp.dados) return;
  const { nos, arestas } = resp.dados;
  const dados = {
    nodes: new vis.DataSet(nos.map((n) => ({
      id: n.id, label: n.rotulo, group: n.tipo, color: CORES[n.tipo],
      shape: n.tipo === "Usuario" ? "dot" : n.tipo === "Post" ? "box" : "diamond",
      size: n.tipo === "Usuario" ? 16 : 10,
      font: { color: n.tipo === "Post" ? "#fff" : "#1b2430", size: 12 },
    }))),
    edges: new vis.DataSet(arestas.map((a) => ({
      from: a.de, to: a.para, label: a.tipo, arrows: "to",
      font: { size: 9, color: "#8a93a3", strokeWidth: 0 }, color: { color: "#c3cbd9" },
      dashes: a.tipo === "INTERESSADO_EM",
    }))),
  };
  const opcoes = { physics: { stabilization: { iterations: 150 }, barnesHut: { springLength: 120 } }, interaction: { hover: true } };
  if (rede) rede.setData(dados); else rede = new vis.Network($("#grafo"), dados, opcoes);
}

$("#btn-grafo").addEventListener("click", carregarGrafo);

// ------------------------------------------------------------------ início
carregarUsuarios().then(carregarGrafo).catch(() => {});
