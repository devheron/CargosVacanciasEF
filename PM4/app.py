"""
============================================================================
 Dashboard PM4 — Cargos Vagos e Vacancias do Executivo Federal Civil
 Fonte: SEGES/MGI — Portal Brasileiro de Dados Abertos (dados.gov.br), 03/2026
 Equipe: Heron Felipe Juvenil Divino, Jihad Riad Ghozayel, Nicolas Gabriel Correa Martao
 Repositorio: https://github.com/devheron/CargosVacanciasEF
============================================================================

 COMO RODAR (passo a passo)
 --------------------------------------------------------------------------
 1. Tenha o Python 3.10+ instalado.

 2. Instale as dependencias (uma unica vez):
        pip install streamlit pandas plotly

 3. Garanta que a pasta de dados esteja ao lado deste arquivo:
        PM4/
        ├── app.py            <- este arquivo
        └── dados_tratados/
            └── dataset_final_tratado.csv

    O caminho lido e "dados_tratados/dataset_final_tratado.csv" (relativo).
    Se rodar de outra pasta, ajuste a variavel CAMINHO_CSV abaixo.

 4. Rode o app:
        streamlit run app.py

    Se aparecer "streamlit nao e reconhecido" (problema de PATH no Windows),
    use sempre:
        python -m streamlit run app.py

 5. O navegador abre sozinho em http://localhost:8501
    Para parar o servidor: Ctrl + C no terminal.

 PUBLICAR ONLINE (opcional, gratis)
 --------------------------------------------------------------------------
 - Suba a pasta no GitHub (ja feito neste repositorio).
 - Acesse share.streamlit.io, conecte o repo e aponte para PM4/app.py.
 - O Streamlit Community Cloud instala o requirements.txt e publica o link.

 ESTRUTURA DO DASHBOARD
 --------------------------------------------------------------------------
 - 5 indicadores (KPIs): cargos, taxa de ocupacao, deficit, % aposentadoria, extincao.
 - 5 graficos: Top 10 orgaos, vacancias por causa, Pareto, faixa de ocupacao,
   porte x extincao. (Sem grafico de pizza, por opcao de leitura.)
 - 4 filtros interativos na barra lateral: nivel, porte, situacao, faixa.
============================================================================
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CAMINHO_CSV = "dados_tratados/dataset_final_tratado.csv"

st.set_page_config(page_title="Cargos Vagos e Vacancias — Executivo Federal", layout="wide")

TEAL = "#0d9488"
ORANGE = "#f59e0b"

CAUSAS = {
    "vac_aposentadoria": "Aposentadoria",
    "vac_posse_cargo_inac": "Posse Cargo Inac.",
    "vac_exoneracao": "Exoneracao",
    "vac_falecimento": "Falecimento",
    "vac_demissao": "Demissao",
    "vac_promocao": "Promocao",
    "vac_readaptacao": "Readaptacao",
}

@st.cache_data
def carregar():
    df = pd.read_csv(CAMINHO_CSV)
    df["nivel"] = df["nivel"].fillna("NAO_INFORMADO")
    return df

df = carregar()

st.markdown(
    "<div style='height:6px;border-radius:4px;margin-bottom:10px;"
    "background:linear-gradient(90deg,#009b3a 0 33%,#ffdf00 33% 66%,#002776 66% 100%);'></div>",
    unsafe_allow_html=True,
)
st.title("Cargos Vagos e Vacancias do Executivo Federal Civil")
st.caption("SEGES / Ministerio da Gestao e Inovacao — competencia marco/2026 · Fonte: dados.gov.br")

with st.expander("A historia do projeto: do dado bruto ao dashboard (PM3 → PM4)", expanded=True):
    st.markdown(
        "Partimos de uma base oficial da **SEGES/MGI** no **dados.gov.br** — a fotografia mensal de "
        "quantos cargos cada orgao federal tem aprovados, ocupados e vagos, mais o fluxo de saidas por sete causas. "
        "No **PM3** tratamos o dado bruto: ele chegou sujo, com **1.618 valores nulos**, datas como inteiro, "
        "codigos perdendo zeros a esquerda, nomes em maiusculas sem padrao e **1.879 outliers** extremos. "
        "Catalogamos **10 problemas de qualidade**, preenchemos nulos, convertemos tipos, padronizamos e — por decisao "
        "de negocio — **preservamos os outliers com uma flag**, pois sao cargos institucionais reais (INSS, Policia Federal), "
        "nao erros. Depois criamos **17 novas variaveis** (taxa de ocupacao, deficit, porte, faixa de ocupacao, normalizacoes), "
        "saindo de **20 para 37 colunas sem perder um registro**. Este dashboard (PM4) transforma esse dataset em historia visivel."
    )
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.metric("Colunas", "20 → 37")
    n2.metric("Nulos tratados", "1.618")
    n3.metric("Problemas de qualidade", "10")
    n4.metric("Outliers preservados", "1.879")
    n5.metric("Registros perdidos", "0")
    st.info(
        "Tres achados que guiaram tudo: 76,7% das vacancias sao aposentadoria (transicao demografica, nao turnover) · "
        "4 orgaos concentram ~49% das vagas (concentracao) · paradoxo: 85% de ocupacao media individual vs. 66,9% real do governo."
    )

# ---- Filtros (sidebar) ----
st.sidebar.header("Filtros")
niveis = sorted(df["nivel"].unique())
portes = ["Micro (1-2)", "Pequeno (3-10)", "Médio (11-50)", "Grande (51-500)", "Mega (>500)"]
faixas = ["Crítica (<40%)", "Baixa (40-70%)", "Adequada (70-90%)", "Completa (90-100%)"]

f_nivel = st.sidebar.multiselect("Nivel", niveis)
f_porte = st.sidebar.multiselect("Porte do cargo", portes)
f_ext = st.sidebar.radio("Situacao", ["Todas", "Ativo", "Em extincao"], horizontal=True)
f_faixa = st.sidebar.multiselect("Faixa de ocupacao", faixas)

d = df.copy()
if f_nivel:
    d = d[d["nivel"].isin(f_nivel)]
if f_porte:
    d = d[d["porte_cargo"].isin(f_porte)]
if f_ext == "Ativo":
    d = d[d["em_extincao"] == "N"]
elif f_ext == "Em extincao":
    d = d[d["em_extincao"] == "S"]
if f_faixa:
    d = d[d["faixa_taxa_ocupacao"].isin(f_faixa)]

# ---- KPIs ----
aprov = d["qtd_aprovada"].sum()
ocup = d["qtd_ocupada"].sum()
vaga = int(d["qtd_vaga"].sum())
tot_vac = sum(d[c].sum() for c in CAUSAS)
apos = d["vac_aposentadoria"].sum()
taxa = (ocup / aprov * 100) if aprov else 0
pct_apos = (apos / tot_vac * 100) if tot_vac else 0
ext_ocup = int(((d["em_extincao"] == "S") & (d["qtd_ocupada"] > 0)).sum())

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Cargos (registros)", f"{len(d):,}".replace(",", "."))
k2.metric("Taxa de ocupacao", f"{taxa:.1f}%")
k3.metric("Deficit nominal (vagas)", f"{vaga:,}".replace(",", "."))
k4.metric("Vac. por aposentadoria", f"{pct_apos:.1f}%")
k5.metric("Extincao c/ ocupante", f"{ext_ocup:,}".replace(",", "."))

st.divider()

# ---- Linha 1 ----
c1, c2 = st.columns(2)

with c1:
    top = d.groupby("sigla_orgao")["qtd_vaga"].sum().sort_values(ascending=False).head(10).sort_values()
    fig = px.bar(x=top.values, y=top.index, orientation="h",
                 labels={"x": "vagas", "y": ""}, title="Top 10 orgaos por vagas",
                 color_discrete_sequence=[TEAL])
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    pares = sorted([(lbl, d[col].sum()) for col, lbl in CAUSAS.items()], key=lambda x: x[1])
    tot_c = sum(v for _, v in pares) or 1
    fig = px.bar(x=[v for _, v in pares], y=[l for l, _ in pares], orientation="h",
                 title="Vacancias por causa", labels={"x": "vacancias no mes", "y": ""},
                 text=[f"{v/tot_c*100:.1f}%" for _, v in pares],
                 color=[l for l, _ in pares],
                 color_discrete_map={l: (ORANGE if l == "Aposentadoria" else TEAL) for l, _ in pares})
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---- Linha 2: Pareto (largura total) ----
byorg = d.groupby("sigla_orgao")["qtd_vaga"].sum().sort_values(ascending=False).head(20)
acum = (byorg.cumsum() / d["qtd_vaga"].sum() * 100) if d["qtd_vaga"].sum() else byorg * 0
fig = go.Figure()
fig.add_bar(x=byorg.index, y=byorg.values, marker_color=TEAL, name="vagas")
fig.add_scatter(x=byorg.index, y=acum.values, yaxis="y2", mode="lines+markers",
                line=dict(color=ORANGE, width=2), name="% acumulado")
fig.update_layout(height=380, title="Concentracao de vagas por orgao (Pareto)",
                  yaxis=dict(title="vagas"), yaxis2=dict(overlaying="y", side="right", range=[0, 105], title="% acum."),
                  margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=1.12))
st.plotly_chart(fig, use_container_width=True)

# ---- Linha 3 ----
c3, c4 = st.columns(2)

with c3:
    order = ["Crítica (<40%)", "Baixa (40-70%)", "Adequada (70-90%)", "Completa (90-100%)"]
    fc = d["faixa_taxa_ocupacao"].value_counts().reindex(order).fillna(0)
    fig = px.bar(x=order, y=fc.values, title="Cargos por faixa de ocupacao",
                 labels={"x": "", "y": "nº de cargos"},
                 color=order, color_discrete_sequence=["#dc2626", "#f59e0b", "#3b82f6", "#0d9488"])
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    ct = pd.crosstab(d["porte_cargo"], d["em_extincao"]).reindex(portes).fillna(0)
    fig = go.Figure()
    fig.add_bar(x=portes, y=ct.get("N", pd.Series(0, index=portes)).values, name="Ativo", marker_color=TEAL)
    fig.add_bar(x=portes, y=ct.get("S", pd.Series(0, index=portes)).values, name="Em extincao", marker_color=ORANGE)
    fig.update_layout(barmode="stack", height=350, title="Porte x situacao de extincao",
                      margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Equipe e referencias")
st.markdown(
    "**Projeto Mensal 4 — Visualizacao de Dados e Dashboard**  \n"
    "**Grupo:** Heron Felipe Juvenil Divino · Jihad Riad Ghozayel · Nicolas Gabriel Correa Martao  \n"
    "**Repositorio:** https://github.com/devheron/CargosVacanciasEF"
)
st.markdown(
    "**Fontes:**  \n"
    "- BRASIL. SEGES/MGI. Cargos Vagos e Vacancias do Poder Executivo Federal Civil, 03/2026. dados.gov.br. CC BY 4.0.  \n"
    "- BRASIL. Lei 8.112/90, art. 33 — Vacancia no Regime Juridico dos Servidores Publicos Civis da Uniao.  \n"
    "- CASTRO, L. N.; FERRARI, D. G. Introducao a mineracao de dados. Saraiva, 2016.  \n"
    "- GOLDSCHMIDT, R.; BEZERRA, E.; PASSOS, E. Data mining: conceitos, tecnicas, algoritmos. Elsevier, 2015."
)
st.caption("Dashboard PM4 · dados tratados no PM3 (37 colunas, 12.769 registros) · Fonte: dados.gov.br — SEGES/MGI")
