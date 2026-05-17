# Guia do Orange Data Mining — Diagnóstico Visual e AED

Este guia mostra como usar o **Orange Data Mining** em paralelo aos notebooks Python para gerar visualizações que vão direto pro relatório. O Orange é especialmente bom para:

- Boxplots e histogramas interativos
- Mapas de calor de correlação
- Matriz de dispersão
- Inspeção visual de distribuições

> **Estratégia:** o tratamento de dados (limpeza, transformação, criação de variáveis) será feito **em Python** porque o enunciado exige reprodutibilidade. O Orange entra como **ferramenta complementar de visualização**, gerando screenshots para o relatório.

---

## Passo 1 — Instalar e abrir o Orange

1. Baixe em https://orangedatamining.com/download/ (versão 3.36 ou superior).
2. Abra o Orange. A interface tem uma **paleta de widgets** à esquerda e um **canvas** no centro onde você arrasta os widgets.

---

## Passo 2 — Carregar a base no Orange

1. Na paleta **Data**, arraste o widget **`File`** para o canvas.
2. Dê duplo clique no widget `File`.
3. Em "Source", aponte para `dados_brutos/CargosVagosVacancias_202603.csv`.
4. Confira se o Orange identificou corretamente os tipos:
   - `ANO_MES`, `ORGAO`, `CARGO` → marque como **Categorical** (são códigos, não números)
   - `NIVEL`, `PLANO_CARREIRA`, `NOME_CARGO`, `NOME_ORGAO`, `SIGLA_ORGAO`, `CARGO_EM_EXTINCAO` → **Categorical**
   - `APROVADA`, `DISTRIBUIDA`, `OCUPADA`, `VAGA` e as 7 `VACANCIA_*` → **Numeric**
5. Clique em "Apply".

> Se o Orange marcar algum código como Numeric, clique na flechinha ao lado do nome da coluna na tabela do widget File e troque para Categorical. Isso evita que ele calcule médias absurdas com identificadores.

---

## Passo 3 — Visualizações para o relatório

Conecte os widgets abaixo ao `File` (arraste a linha pontilhada da saída do `File` até cada widget):

### 3.1 Data Table — visão geral
- **Widget:** `Data Table` (paleta Data)
- **Para que serve:** mostra a base em tabela. Útil para o leitor entender a estrutura.
- **Print para o relatório:** uma screenshot da tabela com algumas linhas visíveis.

### 3.2 Distributions — histogramas por variável
- **Widget:** `Distributions` (paleta Visualize)
- **Para que serve:** gera histograma para qualquer variável selecionada.
- **Variáveis sugeridas:**
  - `APROVADA` com `Bin width` automático
  - `OCUPADA`
  - `VAGA`
  - `NIVEL` (mostra distribuição categórica)
  - `CARGO_EM_EXTINCAO` (binária)
- **Print para o relatório:** uma screenshot por histograma. Mostra visualmente a assimetria das distribuições.

### 3.3 Box Plot — outliers
- **Widget:** `Box Plot` (paleta Visualize)
- **Para que serve:** identificação visual de outliers e quartis.
- **Configuração:**
  - Variable: `APROVADA`
  - Subgroup: `NIVEL` (mostra como APROVADA se distribui por nível de escolaridade)
- **Print para o relatório:** screenshot do boxplot agrupado.

### 3.4 Scatter Plot — relações entre variáveis
- **Widget:** `Scatter Plot` (paleta Visualize)
- **Para que serve:** ver correlação visual entre duas variáveis.
- **Configurações úteis:**
  - X = `APROVADA`, Y = `OCUPADA` (deve mostrar forte correlação positiva)
  - X = `OCUPADA`, Y = `VAGA` (mostra relação inversa)
  - Color = `CARGO_EM_EXTINCAO` (separa por status)
- **Print para o relatório:** dois ou três scatter plots interessantes.

### 3.5 Correlations — mapa de calor
- **Widget:** `Correlations` (paleta Data)
- **Para que serve:** lista as correlações mais fortes entre variáveis numéricas.
- **Print para o relatório:** a tabela ordenada por força de correlação.

### 3.6 Heat Map (opcional)
- **Widget:** `Heat Map` (paleta Visualize)
- **Para que serve:** visualizar padrões em todas as variáveis numéricas simultaneamente.
- Configurar para usar **apenas as colunas numéricas** (excluir códigos e categóricos).

---

## Passo 4 — Salvar o fluxo

1. **File > Save As** → salve como `fluxo_aed.ows` dentro da pasta `orange/` do projeto.
2. Esse arquivo `.ows` é o que vai junto com a entrega. O professor consegue abrir e ver o fluxo completo.

---

## Layout sugerido do canvas Orange

```
[File] ──┬─→ [Data Table]
         ├─→ [Distributions]
         ├─→ [Box Plot]
         ├─→ [Scatter Plot]
         ├─→ [Correlations]
         └─→ [Heat Map]
```

Todos os widgets conectados ao mesmo `File`. Simples e legível.

---

## Capturando screenshots para o relatório

Para cada widget visual:

1. Configure a visualização como quer.
2. Use **Print Screen** ou ferramenta de captura do sistema (Win+Shift+S no Windows, Cmd+Shift+4 no Mac).
3. Salve em `evidencias_aed/orange_XX_descricao.png`.
4. Insira no relatório com legenda.

> O Orange também tem um botão "Save Image" em alguns widgets (canto inferior dos gráficos) — gera PNG/SVG direto. Use sempre que disponível.

---

## Como mencionar isso no relatório

Sugestão de texto para a seção 6.5 (AED) do relatório:

> A análise exploratória de dados foi conduzida em duas frentes complementares: (i) em Python, com as bibliotecas Pandas, Matplotlib e Seaborn, garantindo a reprodutibilidade através dos notebooks Jupyter; e (ii) no Orange Data Mining, ferramenta visual de mineração de dados, utilizada para gerar visualizações interativas que enriquecem este relatório. O fluxo Orange completo está disponível em `orange/fluxo_aed.ows` no repositório do projeto.
