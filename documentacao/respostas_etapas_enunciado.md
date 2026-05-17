# Respostas às Perguntas do Enunciado

> Este documento responde **diretamente** às perguntas explícitas do enunciado do PM3, etapa por etapa. Serve como mapa de evidência: para cada pergunta da disciplina, você encontra a resposta concisa aqui, e a referência ao notebook que aprofunda o assunto.

---

## Etapa 6.1 — Planejamento do tratamento dos dados

> *Notebook de referência: `00_planejamento_e_contexto.ipynb` (seção 1)*

### Qual é o tema da base?

Gestão quantitativa de pessoas no **Poder Executivo Federal Civil brasileiro**. A base apresenta, mês a mês, a fotografia do quadro de pessoal de cada órgão da administração federal direta, autárquica e fundacional — detalhando quantos cargos foram aprovados em lei, distribuídos, ocupados, vagos, e o fluxo de saída por sete causas distintas (aposentadoria, exoneração, demissão, promoção, readaptação, posse em outro cargo inacumulável e falecimento). A unidade de análise é a combinação **(órgão × cargo)** na competência 03/2026.

### De onde os dados foram retirados?

- **Fonte:** Portal Brasileiro de Dados Abertos — `dados.gov.br`
- **Conjunto:** "Cargos Vagos e Vacâncias do Poder Executivo Federal Civil"
- **Órgão produtor:** Secretaria de Gestão e Inovação (SEGES) — Ministério da Gestão e da Inovação em Serviços Públicos (MGI)
- **Arquivo:** `CargosVagosVacancias_202603.ods`, aba `por_Órgao_e_Cargo`
- **Licença:** CC BY 4.0
- **Data de acesso:** 2026

### Qual problema essa base ajuda a compreender?

Cinco fenômenos centrais da gestão pública federal:

1. **Déficit estrutural de servidores** — quando o teto legal (aprovada) está muito acima do ocupado.
2. **Pressão de reposição via aposentadoria** — aposentadoria representa 76,7% das vacâncias em 03/2026.
3. **Estoque de cargos em extinção** — cerca de 28% dos cargos da base estão formalmente em extinção.
4. **Concentração desigual de pessoal** — alguns poucos cargos concentram milhares de servidores enquanto centenas têm 1 ou 2.
5. **Reorganização ministerial recorrente** — a base captura as mudanças de denominação dos órgãos ao longo do tempo.

### Quem poderia usar esses dados para tomar decisão?

| Ator | Decisão que toma |
|---|---|
| MGI / SEGES | Calendário de concursos; redistribuição de vagas; políticas de carreira |
| Ministério do Planejamento e Orçamento | Previsão da folha; impacto orçamentário de reposições |
| TCU | Fiscalização do cumprimento dos tetos legais por órgão |
| CGU | Auditorias sobre cessões e movimentações de pessoal |
| Comissões do Congresso | Pareceres sobre projetos de reestruturação de carreiras |
| Dirigentes dos próprios órgãos | Solicitação de concursos; planejamento de sucessão |
| Sindicatos de servidores | Acompanhamento da força de trabalho da categoria |
| Pesquisadores e jornalismo de dados | Estudos e reportagens sobre gestão pública |

### Como essa base poderia ser usada em Business Intelligence?

- **Dashboards executivos** em Power BI / Looker Studio / Tableau / Metabase
- **KPIs derivados**: taxa de ocupação, déficit nominal, taxa de vacância mensal
- **Drill-down hierárquico**: Executivo Federal → Ministério → Órgão → Carreira → Cargo
- **Alertas operacionais**: órgãos com taxa de vacância > X%
- **Comparativo entre carreiras** e entre níveis de escolaridade

### Como essa base poderia ser usada em Data Mining?

- **Clustering** dos 211 órgãos em perfis típicos (fiscalizadores, prestadores de grande escala, universitários, etc.)
- **Detecção de anomalias** — cargos com taxa de vacância atípica para o tamanho do quadro
- **Regras de associação** — cargos que tendem a coexistir nos mesmos órgãos
- **Classificação supervisionada** — prever se um cargo "tende a estar em extinção"
- **Análise preditiva** (com série histórica) — projetar vacâncias futuras por aposentadoria

### Quais perguntas poderiam ser respondidas com esses dados?

**Descritivas (BI):**
1. Quais órgãos têm mais vagas em aberto em 03/2026?
2. Qual a taxa de ocupação média do governo federal?
3. Quais os 10 cargos com maior quantitativo total?
4. Quanto pesa a aposentadoria comparada às outras causas de vacância?
5. Quantos cargos estão em extinção e em quais órgãos?

**Comparativas:**
6. Cargos de Nível Superior têm taxa de ocupação maior que os Intermediários?
7. Órgãos pequenos têm comportamento de vacância diferente dos grandes?
8. A exoneração se concentra em algum tipo específico de carreira?

**Estruturais (DM):**
9. É possível agrupar os 211 órgãos em perfis típicos?
10. Existem cargos que tendem a coexistir nos mesmos órgãos?
11. Há outliers que mereçam tratamento separado?

---

## Etapa 6.2 — Relação com Big Data Analytics, Data Mining e BI

> *Notebook de referência: `00_planejamento_e_contexto.ipynb` (seção 2)*

### Como os dados poderiam apoiar decisões?

Cada KPI derivado responde a uma decisão concreta:

- **`taxa_ocupacao`** baixa em um órgão → solicitar concurso público
- **`pct_aposentadoria`** alto → priorizar concurso emergencial para reposição
- **`deficit_nominal`** alto em valor absoluto → impacto orçamentário a planejar
- **`is_outlier`** marca cargos institucionais para análise segmentada

### Quais padrões poderiam ser descobertos?

Padrões que **só emergem com tratamento adequado** dos dados:

- **Paradoxo de Simpson na taxa de ocupação** — 76% dos cargos individuais estão "completos" (≥90%), mas a taxa agregada do governo é apenas 67%. Cargos pequenos puxam a média individual para cima; cargos gigantes puxam o agregado para baixo.
- **Concentração extrema de aposentadorias** — 76,7% das vacâncias do mês foram por aposentadoria. Política pública precisa ser pautada por demografia, não por turnover convencional.
- **Inconsistência sistemática** entre `ocupada + vaga` e `distribuida` em 14% dos cargos — efeito de cessões, comissionamentos e duplo vínculo.

### Que tipo de análise poderia ser feita?

- **Descritiva** (o que aconteceu): rankings, médias, totais
- **Diagnóstica** (por que aconteceu): comparação entre grupos
- **Preditiva** (o que vai acontecer): projeção de vacâncias futuras
- **Prescritiva** (o que fazer): priorização de concursos

### A base poderia ser usada em dashboards?

**Sim.** O dataset final tratado (`dataset_final_tratado.csv`, 37 colunas) está organizado em 9 blocos semânticos exatamente pensados para BI:
- Dimensões (temporal, órgão, cargo) para filtros e drill-down
- Medidas brutas (quantitativos) para KPIs aditivos
- Features derivadas (taxas, percentuais) para indicadores acionáveis
- Discretizações (porte, faixa de ocupação) para segmentações visuais

### A base poderia ser usada para classificação, agrupamento, previsão ou descoberta de padrões?

**Sim, para todas as quatro tarefas.** A normalização aplicada (`*_robust`) prepara as features para algoritmos sensíveis a escala. Detalhes:

- **Agrupamento (clustering)**: K-Means / DBSCAN sobre as features `*_robust` para identificar perfis de órgão
- **Classificação**: Random Forest / Logistic Regression para prever `em_extincao`
- **Previsão**: combinando com série histórica, ARIMA / Prophet / gradient boosting para projetar vacâncias futuras
- **Descoberta de padrões**: Apriori / FP-Growth sobre `cod_cargo` × `cod_orgao` para regras de associação

---

## Etapa 6.3 — Modelagem inicial dos dados

> *Notebook de referência: `01_diagnostico_qualidade.ipynb`*

### Quantidade de linhas e colunas?

**Base bruta:** 12.769 linhas × 20 colunas  
**Dataset final tratado:** 12.769 linhas × 37 colunas

### Nome das principais colunas?

- **Temporais:** `ANO_MES` (depois `ano_mes`, `ano`, `mes`, `trimestre`)
- **Órgão:** `ORGAO`, `NOME_ORGAO`, `SIGLA_ORGAO`
- **Cargo:** `CARGO`, `NOME_CARGO`, `NIVEL`, `PLANO_CARREIRA`, `CARGO_EM_EXTINCAO`
- **Quantitativos:** `APROVADA`, `DISTRIBUIDA`, `OCUPADA`, `VAGA`
- **Vacâncias (7 tipos):** `VACANCIA_POR_*`

### Quais colunas são numéricas?

11 colunas: `APROVADA`, `DISTRIBUIDA`, `OCUPADA`, `VAGA`, e as 7 `VACANCIA_POR_*`. Todas são **contagens inteiras**.

### Quais colunas são categóricas?

7 colunas: `ORGAO`, `NOME_ORGAO`, `SIGLA_ORGAO`, `CARGO`, `NOME_CARGO`, `NIVEL`, `PLANO_CARREIRA`, `CARGO_EM_EXTINCAO`. (Os códigos numéricos `ORGAO` e `CARGO` são, semanticamente, identificadores categóricos — o tratamento converteu para string.)

### Quais colunas representam datas ou períodos?

Apenas uma: `ANO_MES` (formato int AAAAMM, ex.: 202603 → convertida para datetime no notebook 02).

### Quais colunas poderiam ser usadas como dimensões em BI?

Todas as colunas de identificação:
- **Temporal**: `ano_mes`, `ano`, `mes`, `trimestre`
- **Órgão**: `sigla_orgao`, `nome_orgao`, `cod_orgao`
- **Cargo**: `cod_cargo`, `nome_cargo`, `plano_carreira`, `nivel`, `em_extincao`
- **Discretizações**: `porte_cargo`, `faixa_taxa_ocupacao`

### Quais colunas poderiam ser usadas como medidas?

Todas as quantitativas + features derivadas:
- **Estoque (brutas)**: `qtd_aprovada`, `qtd_distribuida`, `qtd_ocupada`, `qtd_vaga`
- **Fluxo (vacâncias)**: 7 `vac_*`
- **KPIs (derivadas)**: `total_vacancias`, `deficit_nominal`, `taxa_ocupacao`, `taxa_vacancia_mensal`, `pct_aposentadoria`, `diferenca_distribuicao`
- **Versões para ML**: 5 `*_robust`

---

## Etapa 6.4 — Diagnóstico da qualidade dos dados

> *Notebook de referência: `01_diagnostico_qualidade.ipynb`. Artefato: `documentacao/problemas_qualidade.xlsx`*

### Existem valores ausentes?

**Sim. 1.618 nulos no total**, distribuídos em duas colunas:
- `NIVEL`: 1.255 nulos (9,8% das linhas)
- `PLANO_CARREIRA`: 363 nulos (2,8% das linhas)

### Existem linhas duplicadas?

**Não.** A chave funcional `(ORGAO, CARGO)` foi verificada — cada combinação aparece exatamente uma vez.

### Existem colunas com nomes inadequados?

**Sim.** Todas as 20 colunas vinham em MAIÚSCULAS sem padrão (`ANO_MES`, `VACANCIA_POR_APOSENTADORIA`, etc.). Foram padronizadas para `snake_case` minúsculo no notebook 02.

### Existem tipos de dados incorretos?

**Sim:**
- `ANO_MES` armazenado como inteiro (202603) — convertido para datetime
- `ORGAO` e `CARGO` como int — convertidos para str com `zfill` para preservar zeros à esquerda
- Variáveis categóricas como object — convertidas para `category`

### Datas em formato errado?

**Sim, mas controlado.** `ANO_MES` veio como integer AAAAMM. No tratamento foi convertido para `datetime` (primeiro dia do mês da competência).

### Textos com espaços extras?

**Não foram encontrados.** A base original já vem limpa nesse aspecto.

### Categorias escritas de formas diferentes?

**Não foram encontradas inconsistências graves.** Os valores categóricos (`NIVEL`, `em_extincao`) são padronizados pela SEGES na fonte.

### Valores numéricos fora do padrão?

**Sim, mas legítimos.** Os outliers em `APROVADA` (1.879 cargos com valores acima de Q3 + 1,5×IQR, chegando a 34.209) são valores reais — cargos institucionais grandes — não erros.

### Outliers?

**Sim, 1.879 cargos sinalizados pelo método IQR.** Decisão: **preservar com flag** `is_outlier` em vez de remover (detalhamento na etapa 6.9).

### Colunas sem utilidade?

**Nenhuma.** Todas as 20 colunas têm utilidade analítica e foram preservadas no dataset final.

### Dados inconsistentes?

**Sim, um caso importante:** em 14% das linhas, `OCUPADA + VAGA ≠ DISTRIBUIDA`. Investigando, descobriu-se que essa diferença reflete fenômenos reais (servidores cedidos, comissionamentos). Decisão: materializar como feature `diferenca_distribuicao` em vez de "corrigir".

### Tabela completa dos problemas encontrados

10 problemas catalogados em `documentacao/problemas_qualidade.xlsx`:

| # | Problema | Decisão |
|---|---|---|
| P01 | `NIVEL` com 1.255 nulos | Preencher com "NAO_INFORMADO" |
| P02 | `PLANO_CARREIRA` com 363 nulos | Preencher com "NAO_INFORMADO" |
| P03 | `ANO_MES` como int | Converter para datetime |
| P04 | `ORGAO`/`CARGO` como int (perdem zeros) | Converter para str + zfill |
| P05 | Colunas em MAIÚSCULAS | Padronizar para snake_case |
| P06 | Categóricas como object | Converter para category |
| P07 | Alta assimetria em `APROVADA` | Manter — outliers legítimos |
| P08 | `OCUPADA + VAGA ≠ DISTRIBUIDA` em 14% | Materializar como feature |
| P09 | Outliers em `APROVADA` | Flag (não remover) |
| P10 | Ausência de variáveis derivadas | Criar 9 features |

---

## Etapa 6.5 — Análise Exploratória de Dados

> *Notebook de referência: `02b_analise_exploratoria.ipynb`. Artefatos: 7 PNGs em `evidencias_aed/`*

### Estatísticas descritivas das variáveis numéricas

| Variável | Mediana | Média | Máx | Min | Desvio |
|---|---|---|---|---|---|
| qtd_aprovada | 3 | 54,85 | 34.209 | 1 | 518,08 |
| qtd_ocupada | 1 | 37,15 | — | 0 | — |
| qtd_vaga | 1 | 17,69 | — | 0 | — |
| total_vacancias | 0 | 21,94 | 22.787 | 0 | 352,62 |

Todas com forte assimetria à direita (média >> mediana).

### Frequência das variáveis categóricas

- **Nível:** NS (5.792 cargos, 45%) ≈ NI (5.712, 45%); NM apenas 10; NAO_INFORMADO 1.255
- **Em extinção:** ~28% S, ~72% N
- **Plano de carreira:** 84 planos distintos, com forte concentração nos top 10

### Gráficos de distribuição

3 histogramas + 2 boxplots (gráficos 03, 04, 09). Confirmam a assimetria extrema das contagens — necessário usar escala log para visualizar.

### Gráficos de comparação

- Top 15 órgãos por vagas aprovadas (gráfico 05)
- Distribuição por nível de escolaridade (gráfico 06)
- Vacâncias por tipo (gráfico 07)

### Padrões identificados

1. **Aposentadoria domina** (76,7% das vacâncias)
2. **MS, MF e INSS concentram** o maior volume de vagas
3. **Outliers são institucionais reais**, não erros
4. **Cargos pequenos predominam** em número (43,5% Micro)

### Possíveis relações entre variáveis

Mapa de calor de correlação (gráfico 08) mostra correlação >0,9 entre `aprovada`, `distribuida`, `ocupada` e `vaga` — esperado, são medidas correlacionadas. Vacâncias específicas têm correlação moderada com `ocupada`.

### Análise de valores extremos

Boxplots mostram que praticamente todos os pontos "fora da caixa" são valores reais (cargos institucionais grandes). Isso fundamentou a decisão de **preservar com flag**, não remover.

### Análise temporal

**Não aplicável neste snapshot** — temos apenas competência 03/2026. As colunas `ano`, `mes`, `trimestre` foram criadas como preparação para futuras análises temporais quando concatenar com outros meses.

---

## Etapa 6.6 — Seleção dos dados

> *Notebook de referência: `02_limpeza_e_transformacao.ipynb` (seção 1)*

### Quais colunas foram mantidas?

**Todas as 20 originais.** Justificativa em três blocos:

1. **Identificação (8 cols):** essenciais como dimensões para qualquer análise em BI.
2. **Quantitativos brutos (4 cols):** medidas básicas, nucleares para todos os KPIs.
3. **Vacâncias por tipo (7 cols):** cada tipo tem semântica jurídica distinta (Lei 8.112/90). Mesmo as raras são informação legítima.
4. **`CARGO_EM_EXTINCAO` (1 col):** dimensão de filtro relevante.

### Quais colunas foram removidas?

**Nenhuma.** Não havia colunas inúteis ou redundantes na base bruta.

### Quais registros foram filtrados?

**Nenhum.** Todos os 12.769 registros foram preservados — incluindo os 1.879 sinalizados como outliers (com flag, não removidos).

### Por que determinadas informações foram descartadas?

**Nada foi descartado.** O critério orientador foi: em base governamental oficial, a hipótese padrão é que cada registro reflete uma realidade jurídica e analítica relevante.

### Quais variáveis são importantes para a análise?

Em ordem de importância para os KPIs principais:

1. **Quantitativos:** `qtd_aprovada`, `qtd_ocupada`, `qtd_vaga` (formam todos os indicadores de saúde do quadro)
2. **Vacâncias:** principalmente `vac_aposentadoria` (76,7% das saídas)
3. **Dimensões:** `sigla_orgao`, `nivel`, `em_extincao` (segmentações analíticas mais usadas)

---

## Etapa 6.7 — Limpeza e pré-processamento

> *Notebook de referência: `02_limpeza_e_transformacao.ipynb` (seções 2-4)*

Ações executadas:

| Ação | Detalhe |
|---|---|
| Renomear colunas | 20 colunas em UPPERCASE → snake_case |
| Padronizar nomes | Prefixos uniformes: `vac_*`, `qtd_*` |
| Corrigir tipos | int→datetime, int→str, object→category |
| Converter datas | `ANO_MES` (202603) → `2026-03-01` |
| Remover duplicidades | Nenhuma encontrada |
| Corrigir categorias | Nenhuma inconsistência encontrada |
| Padronizar textos | Verificado, sem ajustes necessários |
| Corrigir valores inválidos | Nenhum encontrado |
| Tratar valores ausentes | 1.618 nulos preenchidos com "NAO_INFORMADO" |
| Preparar para análise | Categóricas convertidas para `category` (memória) |

**Antes:** `Data Venda, VALOR R$, nome_cliente, Estado` (não aplicável — base já vinha sem caracteres especiais)  
**Depois:** `data_venda, valor, nome_cliente, estado` (no nosso caso: `ANO_MES → ano_mes`, `VACANCIA_POR_APOSENTADORIA → vac_aposentadoria`)

---

## Etapa 6.8 — Tratamento de valores faltantes

> *Notebook de referência: `02_limpeza_e_transformacao.ipynb` (seção 3)*

### Quantidade de valores ausentes antes do tratamento

| Coluna | Nulos | % |
|---|---|---|
| `NIVEL` | 1.255 | 9,8% |
| `PLANO_CARREIRA` | 363 | 2,8% |
| **Total** | **1.618** | **— ** |

### Estratégia adotada

**Preenchimento com a categoria explícita `"NAO_INFORMADO"`.**

### Por que não foi usado `dropna()`?

Remover linhas com nulos eliminaria 9,8% da base — empobrecimento gratuito. A ausência de `NIVEL` em alguns cargos antigos é informação legítima (carreiras descontinuadas em situação administrativa especial).

### Por que não foi usada a moda?

Imputar com a moda ("NS") atribuiria nível superior a cargos que podem ser de qualquer nível, distorcendo análises por escolaridade.

### Quantidade de valores ausentes após o tratamento

**Zero** nulos no dataset pós-limpeza. Os NaN que aparecem no dataset final (em `taxa_vacancia_mensal` e `pct_aposentadoria`) são gerados pelas features derivadas onde o denominador é zero — situação semanticamente correta e justificada na etapa 6.14.

---

## Etapa 6.9 — Tratamento de outliers

> *Notebook de referência: `02_limpeza_e_transformacao.ipynb` (seção 4)*

### Como os outliers foram identificados?

Pelo método **IQR (Intervalo Interquartil)** sobre `qtd_aprovada`:
- Q1 = 1, Q3 = 12, IQR = 11
- Limite superior = Q3 + 1,5×IQR = 28,5
- **1.879 cargos** com valores acima desse limite

Boxplot e histograma (gráficos 04 e 03 da AED) confirmam visualmente a presença dos outliers.

### Decisão tomada

**Preservar todos os 1.879 outliers, mas marcar com flag `is_outlier`.**

### Justificativa

Investigação caso a caso mostrou que os outliers correspondem aos **cargos institucionais grandes**:
- Técnico Administrativo em Educação (34.209 vagas)
- Cargos do INSS, da Polícia Federal, da Receita Federal
- Cargos das forças civis e dos grandes ministérios prestadores

São **valores legítimos**, não erros. Removê-los empobreceria gravemente a análise — o enunciado adverte explicitamente: "outlier não é automaticamente erro. Às vezes ele é justamente o dado mais importante da análise".

### Vantagens da abordagem com flag

- Permite análises segmentadas (`df[df['is_outlier']==1]` vs `df[df['is_outlier']==0]`)
- Não perde 14,7% da base
- Documenta a decisão de forma transparente
- Reflete corretamente a realidade institucional do Executivo Federal

---

## Etapa 6.10 — Transformação dos dados

> *Notebook de referência: `02_limpeza_e_transformacao.ipynb` (seção 5)*

| Tipo de transformação | Aplicação no projeto |
|---|---|
| Converter texto em número | Não aplicável (a base já tem numéricos como int) |
| Converter texto em data | `ANO_MES` (int 202603) → datetime |
| Criar coluna de ano, mês e trimestre | `ano`, `mes`, `trimestre` extraídos de `ano_mes` |
| Criar faixas de valores | `porte_cargo`, `faixa_taxa_ocupacao` (etapa 6.13) |
| Agrupar categorias | Não foi necessário — categorias já estão padronizadas |
| Padronizar nomes | Todas as 20 colunas em snake_case |
| Converter valores monetários | Não aplicável (não há colunas monetárias) |
| Transformar variáveis categóricas | object → category para `nivel`, `plano_carreira`, `em_extincao` |
| Criar indicadores | `is_outlier` (binário), `em_extincao` (já vinha S/N) |

---

## Etapa 6.11 — Agregação de dados

> *Notebook de referência: `03_feature_engineering.ipynb` (seção 2). Artefatos em `dados_tratados/agregacoes/`*

### Foi realizada agregação? Quais?

**Sim, três agregações complementares:**

1. **Por órgão** (`agg_por_orgao.csv`) — 209 órgãos resumidos com totais e taxa de ocupação
2. **Por nível de escolaridade** (`agg_por_nivel.csv`) — 4 níveis com médias, totais e taxa agregada
3. **Por tipo de vacância** (`agg_por_tipo_vacancia.csv`) — 7 tipos com totais e percentuais

### O que cada agregação mostra?

**Por órgão:**
- MS, MF e INSS dominam o volume aprovado
- DPRF e DPF têm as taxas de ocupação mais altas (>80%)
- MEC tem taxa anormalmente baixa (4,7%) — efeito da reforma que distribuiu cargos para autarquias

**Por nível:**
- NS e NI têm volumes próximos (5.792 e 5.712 cargos)
- Taxa de ocupação agregada: NS = 68,6%, NI = 62,4%
- Cargos com nível NAO_INFORMADO estão quase totalmente ocupados (94,6%) — sinal de carreiras descontinuadas

**Por tipo de vacância:**
- Aposentadoria: 76,7% (214.829 movimentações)
- Posse em cargo inacumulável: 8,2%
- Exoneração: 7,4%
- Demais (demissão, promoção, readaptação): <2% combinados

---

## Etapa 6.12 — Normalização e padronização

> *Notebook de referência: `03_feature_engineering.ipynb` (seção 3)*

### Quais colunas foram normalizadas?

Cinco colunas-chave:
- `qtd_aprovada_robust`
- `qtd_ocupada_robust`
- `qtd_vaga_robust`
- `total_vacancias_robust`
- `deficit_nominal_robust`

### Qual técnica foi usada?

**RobustScaler** do scikit-learn (mediana=0, IQR=1).

### Por que essa técnica foi escolhida?

Comparação técnica explícita no notebook 03:

| Técnica | Problema com esta base |
|---|---|
| MinMax | 75% dos cargos ficam abaixo de 0,0005 — perde discriminação |
| StandardScaler | Outliers puxam média; p99 chega a +8,7σ |
| **RobustScaler** | Mediana e IQR resistem aos outliers — escolha técnica |

A base tem **outliers reais** (1.879 cargos institucionais). MinMax e StandardScaler tratam-nos como anomalias a serem "achatadas" — destruindo informação. RobustScaler preserva.

### Qual a diferença antes e depois?

| Percentil | Original (qtd_aprovada) | MinMax | StandardScaler | **RobustScaler** |
|---|---|---|---|---|
| p25 | 1 | 0,000000 | -0,104 | **-0,182** |
| p50 | 3 | 0,000058 | -0,100 | **0,000** |
| p75 | 12 | 0,000322 | -0,083 | **0,818** |
| p99 | 1.099 | 0,032 | 2,017 | 99,72 |

A mediana fica exatamente em zero (por construção). Valores positivos = acima da mediana; negativos = abaixo. Os outliers continuam visíveis (p99 alto), mas o miolo da distribuição mantém poder de discriminação.

---

## Etapa 6.13 — Discretização dos dados

> *Notebook de referência: `03_feature_engineering.ipynb` (seção 4)*

### Quais variáveis foram discretizadas?

Duas:

1. **`porte_cargo`** ← discretização de `qtd_aprovada`
2. **`faixa_taxa_ocupacao`** ← discretização de `taxa_ocupacao`

### Qual método foi usado?

**`pd.cut()`** com **cortes de negócio** (não com quartis). Justificativa: quartis dividem em grupos de mesmo tamanho, sem significado gerencial. Cortes semânticos produzem categorias **interpretáveis e estáveis** ao longo do tempo.

### Variável original vs variável discretizada

**`porte_cargo`:**

| Faixa | Cortes | Cargos | % |
|---|---|---|---|
| Micro | 1-2 | 5.558 | 43,5% |
| Pequeno | 3-10 | 3.715 | 29,1% |
| Médio | 11-50 | 2.266 | 17,7% |
| Grande | 51-500 | 966 | 7,6% |
| Mega | >500 | 264 | 2,1% |

**`faixa_taxa_ocupacao`:**

| Faixa | Cortes | Cargos | % |
|---|---|---|---|
| Crítica | <40% | 1.539 | 12,1% |
| Baixa | 40-70% | 610 | 4,8% |
| Adequada | 70-90% | 870 | 6,8% |
| Completa | 90-100% | 9.750 | 76,4% |
| Excedente | >100% | 0 | 0% |

**Achado interessante:** 76% dos cargos em "Completa", mas taxa agregada do governo é só 67% (paradoxo de Simpson — detalhado no notebook 03).

---

## Etapa 6.14 — Feature Engineering

> *Notebook de referência: `03_feature_engineering.ipynb` (seção 1)*

### Quais variáveis novas foram criadas?

**Nove features:**

| Feature | Fórmula | Justificativa |
|---|---|---|
| `total_vacancias` | soma das 7 `vac_*` | KPI consolidado de fluxo |
| `pct_aposentadoria` | `vac_aposentadoria / total_vacancias` | Proxy de envelhecimento |
| `taxa_ocupacao` | `qtd_ocupada / qtd_aprovada` | KPI principal de saúde do quadro |
| `taxa_vacancia_mensal` | `total_vacancias / qtd_ocupada` | Rotatividade |
| `deficit_nominal` | `qtd_aprovada - qtd_ocupada` | Quantifica déficit absoluto |
| `diferenca_distribuicao` | `(ocupada + vaga) - distribuida` | Materializa problema P08 |
| `ano` | extraído de `ano_mes` | Compatibilidade temporal |
| `mes` | extraído de `ano_mes` | Sazonalidade futura |
| `trimestre` | extraído de `ano_mes` | Agregação trimestral |

### As novas variáveis têm utilidade analítica?

**Sim — cada uma está amarrada a pelo menos uma das 11 perguntas analíticas** definidas no notebook 00. Nenhuma feature foi criada apenas para "engordar" a base.

### Tratamento de divisão por zero

Três features podem produzir NaN (divisões). Tratamento diferenciado por significado semântico:

- `pct_aposentadoria` → NaN quando não há vacância (não há "porcentagem" a calcular)
- `taxa_ocupacao` → NaN quando não há vaga aprovada (situação anômala)
- `taxa_vacancia_mensal` → NaN quando não há ocupantes (não há "rotatividade")

Não substituídos por zero — isso seria semanticamente incorreto.

---

## Etapa 6.15 — Consolidação do dataset final

> *Notebook de referência: `04_dataset_final.ipynb`*

### O dataset final está limpo?

**Sim.** Zero espaços extras, zero duplicatas pela chave funcional, zero nulos não justificados.

### Está padronizado?

**Sim.** Todas as 37 colunas em `snake_case` minúsculo. Tipos coerentes (datetime, string, category, int64, float64).

### Tem valores ausentes tratados ou justificados?

**Sim.** Os únicos nulos remanescentes estão em duas features derivadas (`pct_aposentadoria`, `taxa_vacancia_mensal`) onde o NaN reflete divisão indefinida — semanticamente correto.

### Tem outliers analisados?

**Sim.** Os 1.879 outliers identificados foram preservados com a flag `is_outlier`.

### Tem colunas relevantes?

**Sim.** Todas as 37 colunas têm utilidade analítica documentada no catálogo.

### Tem novas variáveis criadas?

**Sim, 17 colunas novas:** 9 features derivadas, 5 versões normalizadas, 2 discretizações, 1 flag (`is_outlier`).

### Tem nomes de colunas claros?

**Sim.** Padrão `snake_case`, prefixos consistentes (`qtd_*`, `vac_*`, `*_robust`).

### Tem tipos de dados corretos?

**Sim.** Validado com `assert` no notebook 04 (tolerante a pandas 2.x e 3.x).

### Está pronto para BI, DM ou análise exploratória?

**Sim.** Organizado em 9 blocos semânticos (temporal, identificação do órgão, identificação do cargo, quantitativos brutos, vacâncias, features quantitativas, features categóricas, versões normalizadas, flags).

### Em qual formato foi entregue?

**Dois formatos:**
- `dataset_final_tratado.csv` (3,5 MB) — universal, recomendado para reprodutibilidade
- `dataset_final_tratado.xlsx` (1,9 MB) — conveniência para Excel

---

## Etapa 6.16 — Catálogo de dados

> *Notebook de referência: `04_dataset_final.ipynb` (seção 4). Artefato: `documentacao/catalogo_dados.xlsx`*

### O catálogo contém os 8 atributos exigidos?

**Sim, para cada uma das 37 colunas:**

| Atributo exigido | Coluna no catálogo |
|---|---|
| Nome da coluna | `nome_coluna` |
| Descrição | `descricao` |
| Tipo de dado | `tipo_dado` |
| Exemplo de valor | `exemplo` (coletado dinamicamente do dataset) |
| Origem | `origem` |
| Tratamento aplicado | `tratamento_aplicado` |
| Original ou criada | `origem_tipo` |
| Uso esperado | `uso_esperado` |

### Distribuição da origem das colunas

| Origem | Quantidade |
|---|---|
| Criada | 17 |
| Original | 14 |
| Original (transformada) | 4 |
| Original (tratada) | 2 |
| **Total** | **37** |

### Formato do catálogo

Excel formatado profissionalmente com **duas planilhas**:

1. **`Catalogo`** — tabela principal com cabeçalho destacado, zebra rows, bordas finas, larguras calibradas, freeze panes
2. **`Metadados`** — 15 atributos sobre o projeto (versão, fonte, licença, totais, data de geração)

---

## Etapa 6.17 — DataOps e organização do projeto

> *Notebook de referência: estrutura completa do projeto + `README.md`*

### A base original foi preservada?

**Sim.** O arquivo `CargosVagosVacancias_202603.ods` está intacto em `dados_brutos/`. Nenhuma operação do pipeline modifica ele.

### O dataset final é diferente da base original?

**Sim, substancialmente:**
- Base original: 12.769 × 20, com 1.618 nulos, em formato ODS
- Dataset final: 12.769 × 37 (17 colunas novas), com nulos justificados, em CSV e XLSX padronizados

### O código está organizado e executável?

**Sim.** Seis notebooks Jupyter sequenciais, cada um com uma responsabilidade clara, todos com caminhos relativos, dependências mínimas (pandas, numpy, matplotlib, seaborn, openpyxl, scikit-learn).

### Outras pessoas conseguem reproduzir?

**Sim.** Estrutura segue a sugestão do enunciado:

```
PM3_CargosVagosVacancias/
├── dados_brutos/         (original preservado)
├── dados_tratados/       (artefatos de pipeline)
├── notebooks/            (6 notebooks executáveis)
├── documentacao/         (catálogo, relatório, problemas)
├── evidencias_aed/       (gráficos PNG)
├── orange/               (fluxo Orange complementar)
└── README.md
```

O `README.md` documenta a ordem de execução, dependências e estrutura. Os notebooks usam caminhos relativos (`../dados_brutos/`), o que garante que qualquer pessoa consiga rodar de qualquer máquina.

---

## Cobertura dos Entregáveis Obrigatórios (item 7 do enunciado)

| Entregável obrigatório | Status | Localização |
|---|---|---|
| Base de dados original | ✅ | `dados_brutos/CargosVagosVacancias_202603.ods` |
| Dataset final tratado | ✅ | `dados_tratados/dataset_final_tratado.csv` (+ .xlsx) |
| Notebook ou script Python | ✅ | `notebooks/` (6 notebooks) |
| Relatório final | ✅ | `documentacao/relatorio_final.docx` (+ .md) |
| Catálogo de dados | ✅ | `documentacao/catalogo_dados.xlsx` |
| Evidências da AED | ✅ | `evidencias_aed/` (7 PNGs) |
| Tabela com problemas de qualidade | ✅ | `documentacao/problemas_qualidade.xlsx` |
| Descrição das etapas de limpeza | ✅ | Notebooks 02 + este documento |
| Demonstração de valores faltantes | ✅ | Notebook 02, seção 3 |
| Demonstração de outliers | ✅ | Notebook 02, seção 4 |
| Demonstração de transformação | ✅ | Notebook 02, seção 5 |
| Demonstração de agregação | ✅ | Notebook 03, seção 2 |
| Demonstração de normalização | ✅ | Notebook 03, seção 3 |
| Demonstração de discretização | ✅ | Notebook 03, seção 4 |
| Demonstração de Feature Engineering | ✅ | Notebook 03, seção 1 |
| Explicação sobre uso em BI e DM | ✅ | Notebook 00, seção 2 + este documento |

**Total: 16 de 16 entregáveis cumpridos.**
