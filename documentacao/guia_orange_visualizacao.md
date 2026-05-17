# Guia de Visualização no Orange Data Mining

> Este guia complementa o `orange/GUIA_ORANGE.md` (que descreve como **construir** o fluxo Orange). Aqui o foco é **visualizar os resultados** do projeto — útil para revisores, professores, ou para você mesmo explorar o que o pipeline produziu.

---

## O que é o Orange Data Mining?

**Orange** é uma ferramenta visual de mineração de dados de código aberto, desenvolvida pela Universidade de Ljubljana. Diferente do Python (onde você escreve código), no Orange você **arrasta widgets** em um canvas e os conecta para criar um fluxo de análise.

É indicado para:

- **Exploração rápida** de dados sem precisar codificar
- **Apresentações** — gráficos limpos e interativos
- **Ensino** — ótimo para mostrar conceitos de DM sem o atrito de programação

**Não substitui** o pipeline Python deste projeto — o tratamento de dados precisa ser reprodutível e versionado em código. O Orange entra como **camada visual complementar**.

---

## Por que usar Orange além dos notebooks Python?

| Necessidade | Python (notebooks) | Orange |
|---|---|---|
| Reprodutibilidade | ✅ Excelente | ⚠️ Limitada (arquivo `.ows`) |
| Tratamento de dados | ✅ Pleno controle | ⚠️ Limitado |
| Visualizações interativas | ⚠️ Estáticas (PNG) | ✅ Excelente |
| Curva de aprendizado | Alta | Baixa |
| Modelos de ML prontos | Via sklearn | ✅ Widgets nativos |

**Resumo:** o projeto faz o tratamento sério em Python. O Orange entra para você **brincar com os dados** depois e gerar visualizações extras para apresentação.

---

## Instalação

1. Baixe em **https://orangedatamining.com/download/**
2. Instalador para Windows, Mac e Linux disponível
3. Versão recomendada: **3.36 ou superior**
4. Tamanho do download: ~500 MB (vem com Python e dependências embutidas)

Não precisa configurar nada além disso. Não conflita com Anaconda.

---

## Passo a passo: visualizando a base BRUTA

### Passo 1 — Carregar o CSV

1. Abra o Orange
2. Na **paleta de widgets** à esquerda, encontre **`File`** (categoria *Data*)
3. **Arraste** o widget `File` para o canvas
4. **Duplo clique** no widget para abrir as configurações
5. Em "Source", clique no botão de pasta e selecione:
   ```
   dados_brutos/CargosVagosVacancias_202603.csv
   ```
6. O Orange vai mostrar uma prévia da base na parte inferior

### Passo 2 — Ajustar tipos de coluna

Esta é a parte mais importante — Orange tenta inferir o tipo, mas precisa de ajuda. Na tabela de variáveis (parte inferior do widget File):

| Coluna | Marcar como |
|---|---|
| `ANO_MES` | **Categorical** (é código, não número) |
| `ORGAO`, `CARGO` | **Categorical** (identificadores) |
| `NOME_ORGAO`, `SIGLA_ORGAO`, `NOME_CARGO` | **Text** ou **Categorical** |
| `NIVEL`, `PLANO_CARREIRA`, `CARGO_EM_EXTINCAO` | **Categorical** |
| `APROVADA`, `DISTRIBUIDA`, `OCUPADA`, `VAGA` | **Numeric** |
| Todas as 7 `VACANCIA_POR_*` | **Numeric** |

Clique em **Apply** quando terminar.

> **Por que isso importa?** Se `ORGAO` (código numérico) ficar como Numeric, o Orange vai tentar calcular "média de código de órgão" — sem sentido. Como Categorical, ele trata como identificador.

---

## Passo 3 — Visualizações recomendadas

Para cada visão, **arraste o widget** correspondente e **conecte ao `File`** (puxe a linha pontilhada da saída do File para o widget).

### A. Visão geral da base — Data Table

- **Widget:** `Data Table` (categoria *Data*)
- **O que mostra:** a base inteira em formato tabular
- **Para que serve:** entender estrutura, scroll pelas linhas, ver tipos
- **Print recomendado:** screenshot mostrando as primeiras 20 linhas

### B. Distribuição de uma variável — Distributions

- **Widget:** `Distributions` (categoria *Visualize*)
- **O que mostra:** histograma ou gráfico de barras da variável escolhida
- **Configurações sugeridas:**
  - `APROVADA` (numérica) → histograma com escala log no eixo Y para visualizar a cauda longa
  - `NIVEL` (categórica) → barras com contagem por nível
  - `CARGO_EM_EXTINCAO` (binária) → S vs N
- **O que observar:** a forte assimetria de `APROVADA` é o achado-chave que motiva todo o tratamento de outliers

### C. Outliers visuais — Box Plot

- **Widget:** `Box Plot` (categoria *Visualize*)
- **O que mostra:** mediana, quartis, e outliers visualmente
- **Configurações sugeridas:**
  - **Variable:** `APROVADA`
  - **Subgroups:** `NIVEL` (mostra como APROVADA varia por escolaridade)
- **O que observar:** os pontos fora dos "bigodes" — quase todos são valores reais (cargos institucionais)

### D. Correlações — Correlations

- **Widget:** `Correlations` (categoria *Data*)
- **O que mostra:** as duas variáveis mais correlacionadas, ranqueadas
- **O que observar:** alta correlação entre APROVADA, DISTRIBUIDA, OCUPADA e VAGA (>0.9). Vacâncias entre si têm correlação mais fraca

### E. Scatter Plot — relação entre duas variáveis

- **Widget:** `Scatter Plot` (categoria *Visualize*)
- **Configurações úteis:**
  - X = `APROVADA`, Y = `OCUPADA` → relação quase linear (esperada)
  - X = `OCUPADA`, Y = `VAGA` → relação inversa
  - **Color:** `CARGO_EM_EXTINCAO` → cargos em extinção formam padrão diferente
- **O que observar:** os outliers visíveis no canto superior direito; o "cluster" de cargos em extinção

### F. Mapa de calor — Heat Map

- **Widget:** `Heat Map` (categoria *Visualize*)
- **Conectar a:** todas as colunas numéricas (excluir `ANO_MES`, `ORGAO`, `CARGO`)
- **O que mostra:** padrão visual de todas as variáveis numéricas juntas
- **O que observar:** linhas dos cargos institucionais "estouram" cromaticamente — outra forma de ver os outliers

---

## Passo 4 — Visualizando o dataset FINAL TRATADO

Para comparar antes vs. depois, **adicione um segundo widget `File`** no canvas e aponte para:

```
dados_tratados/dataset_final_tratado.csv
```

Agora você tem duas fontes no mesmo canvas. Conecte widgets de visualização ao dataset tratado:

### Visões interessantes no dataset final

#### `taxa_ocupacao` por `nivel` — Box Plot

Compara a saúde do quadro entre níveis de escolaridade. Use:
- **Variable:** `taxa_ocupacao`
- **Subgroups:** `nivel`

Você verá: a mediana das taxas individuais é altíssima (~100%) em todos os níveis — efeito do paradoxo de Simpson explicado no relatório.

#### `porte_cargo` x `faixa_taxa_ocupacao` — Sieve Diagram

- **Widget:** `Sieve Diagram` (categoria *Visualize*)
- **Eixos:** X = `porte_cargo`, Y = `faixa_taxa_ocupacao`
- **O que mostra:** se cargos de portes diferentes têm padrões de ocupação distintos

Você verá: cargos Micro estão majoritariamente "Completos" (ocupados a 100%). Cargos Mega tendem a estar nas faixas "Adequada" e "Baixa". Visualmente confirma o paradoxo.

#### Distribuição das features normalizadas — Distributions

- Selecione qualquer coluna `*_robust`
- Veja como a distribuição fica centrada em 0 (mediana) com cauda dos outliers preservada
- Compare com a versão original (`qtd_aprovada` vs `qtd_aprovada_robust`) — fica claro por que RobustScaler é melhor que MinMax

---

## Passo 5 — Tarefas de Data Mining (opcional)

Se quiser ir além da visualização e explorar mineração de dados sobre a base tratada:

### Clustering — K-Means sobre as features normalizadas

1. Adicione widget **`Select Columns`** (categoria *Data*) conectado ao File
2. Selecione apenas as 5 colunas `*_robust` como features
3. Conecte ao widget **`k-Means`** (categoria *Unsupervised*)
4. Configure k = 4 ou 5
5. Conecte a saída a um **`Scatter Plot`** com **Color = Cluster**
6. **O que observar:** os 209 órgãos se separam em perfis distintos

### Detecção de anomalias — Outliers

1. Widget **`Outliers`** (categoria *Data*) conectado ao File
2. Use método `Isolation Forest` ou `Local Outlier Factor`
3. Compare os outliers encontrados pelo Orange com a flag `is_outlier` do dataset

---

## Passo 6 — Salvando o fluxo

1. **File → Save As**
2. Salve como **`fluxo_aed.ows`** dentro da pasta `orange/` do projeto
3. Esse arquivo `.ows` pode ser entregue junto com o projeto — qualquer pessoa com Orange instalado consegue abrir e ver todo o canvas

---

## Layout sugerido do canvas

Para deixar o canvas legível, organize os widgets em camadas:

```
                        ┌─ [Data Table]
                        ├─ [Distributions]
                        ├─ [Box Plot]
[File: base bruta] ─────┼─ [Correlations]
                        ├─ [Scatter Plot]
                        └─ [Heat Map]

                        ┌─ [Box Plot taxa_ocupacao]
                        ├─ [Sieve porte vs faixa]
[File: dataset final] ──┤─ [Distributions robust]
                        ├─ [k-Means]
                        └─ [Outliers]
```

---

## O que tirar como evidência para o relatório

Para incluir no relatório final, capture screenshots de **3-5 widgets** que demonstrem visualmente os achados-chave:

1. **`Box Plot` de `APROVADA`** → mostra a presença dos outliers (justifica decisão da etapa 6.9)
2. **`Distributions` de `nivel`** → mostra distribuição categórica (etapa 6.5)
3. **`Scatter Plot` `OCUPADA` × `VAGA`** → mostra a relação inversa (etapa 6.5)
4. **`Correlations`** → tabela ordenada (etapa 6.5)
5. **`Box Plot` de `taxa_ocupacao` por `nivel`** no dataset final → mostra o paradoxo de Simpson (etapas 6.13 e 6.16)

Cada screenshot pode entrar na seção de AED (item 8 do relatório) com legenda do tipo:

> *Figura X — Boxplot de APROVADA por NIVEL, gerado no Orange Data Mining a partir da base bruta. Outliers (pontos fora dos bigodes) representam cargos institucionais grandes, preservados no dataset final com a flag `is_outlier`.*

---

## Comparação rápida: Orange vs notebooks Python deste projeto

| Visão | Onde está no projeto | Equivalente no Orange |
|---|---|---|
| Histogramas das variáveis | `evidencias_aed/03_histogramas_variaveis_principais.png` | Widget `Distributions` |
| Boxplots | `evidencias_aed/04_boxplots_variaveis_principais.png` | Widget `Box Plot` |
| Top 15 órgãos | `evidencias_aed/05_top15_orgaos_vagas.png` | Filtrar + `Bar Plot` |
| Distribuição por nível | `evidencias_aed/06_distribuicao_nivel.png` | Widget `Distributions` em variável categórica |
| Vacâncias por tipo | `evidencias_aed/07_vacancias_por_tipo.png` | Widget `Bar Plot` |
| Mapa de calor | `evidencias_aed/08_mapa_calor_correlacao.png` | Widget `Correlations` + `Heat Map` |
| Boxplot APROVADA × NIVEL | `evidencias_aed/09_boxplot_aprovada_por_nivel.png` | Widget `Box Plot` com subgroup |

Os PNGs em `evidencias_aed/` são versões "para o relatório" — estáticas e prontas. O Orange é para **interação ao vivo** com os dados.

---

## Limitações do Orange neste projeto

- O Orange **não é reprodutível** da mesma forma que código Python. O arquivo `.ows` salva o fluxo, mas pequenas mudanças no dataset podem quebrar o canvas.
- Para o **tratamento sério** (limpeza, criação de features, normalização), use os notebooks. O Orange tem widgets para isso, mas são limitados e difíceis de auditar.
- Algumas visualizações ficam **pesadas** com 12.769 linhas. Se o Orange ficar lento, use o widget **`Data Sampler`** para amostrar 1.000-2.000 linhas para visualização.

---

## Resumo

Para visualizar o projeto no Orange:

1. **Instalar** o Orange 3.36+ (~500 MB)
2. **Arrastar widget `File`** e apontar para a base (bruta ou final tratada)
3. **Ajustar tipos** (códigos como Categorical)
4. **Conectar widgets de visualização**: Data Table, Distributions, Box Plot, Correlations, Scatter Plot, Heat Map
5. **(Opcional)** Adicionar widgets de mineração: k-Means, Outliers
6. **Salvar** o fluxo como `orange/fluxo_aed.ows`
7. **Capturar screenshots** dos achados-chave para o relatório

Tempo total estimado para reproduzir o fluxo completo: **30-45 minutos** na primeira vez, **5-10 minutos** depois que estiver familiarizado com a interface.
