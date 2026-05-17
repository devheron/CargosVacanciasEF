# Guia de Execução do Projeto

> Este guia mostra **passo a passo** como rodar todo o pipeline do projeto, do zero, em qualquer máquina com Python instalado. Para uma visão de alto nível, veja o `README.md` na raiz.

---

## 1. Pré-requisitos

### Software necessário

| Software | Versão mínima | Para que serve |
|---|---|---|
| Python | 3.9+ | Linguagem dos notebooks |
| Jupyter | 6+ ou Jupyter Lab 3+ | Executar os notebooks `.ipynb` |
| Editor de texto (opcional) | qualquer | Inspecionar README, markdowns, CSVs |
| Excel ou LibreOffice (opcional) | qualquer | Abrir os arquivos `.xlsx` e `.ods` |
| Orange Data Mining (opcional) | 3.36+ | Visualização visual complementar |

### Distribuição Python recomendada

A forma mais simples de ter tudo isso de uma vez é instalar o **Anaconda** (https://www.anaconda.com/download). Inclui Python, Jupyter, pandas, numpy, matplotlib, seaborn, scikit-learn e openpyxl — tudo o que o projeto precisa, exceto eventualmente uma reinstalação fina das versões.

Se preferir Python "puro" (sem Anaconda), basta instalar do site oficial https://www.python.org e depois rodar `pip install` das bibliotecas (próximo passo).

---

## 2. Instalação das dependências

Abra um terminal (Anaconda Prompt no Windows, ou Terminal no Mac/Linux) na pasta-raiz do projeto e execute:

```bash
pip install pandas numpy matplotlib seaborn openpyxl scikit-learn jupyter
```

Se estiver no Anaconda e quiser garantir versões consistentes:

```bash
conda install pandas numpy matplotlib seaborn openpyxl scikit-learn jupyter -c conda-forge
```

### Verificação rápida

Cole no terminal Python:

```python
import pandas, numpy, matplotlib, seaborn, openpyxl, sklearn
print("Tudo certo!")
```

Se imprimir "Tudo certo!", está pronto. Se faltar algum, o erro vai dizer qual e você instala individualmente com `pip install nome-da-biblioteca`.

---

## 3. Estrutura de pastas e o que cada uma significa

```
PM3_CargosVagosVacancias/
│
├── dados_brutos/                          ← ENTRADA: base original (não mexer!)
│   ├── CargosVagosVacancias_202603.ods    ← arquivo oficial preservado
│   └── CargosVagosVacancias_202603.csv    ← versão CSV (gerada a partir do ODS)
│
├── dados_tratados/                        ← SAÍDA: artefatos do pipeline
│   ├── dataset_pos_limpeza.csv            ← checkpoint após Notebook 02
│   ├── dataset_com_features.csv           ← checkpoint após Notebook 03
│   ├── dataset_final_tratado.csv          ← ENTREGÁVEL final (NB 04)
│   ├── dataset_final_tratado.xlsx         ← ENTREGÁVEL final em Excel
│   └── agregacoes/                        ← tabelas agregadas (NB 03)
│       ├── agg_por_orgao.csv
│       ├── agg_por_nivel.csv
│       └── agg_por_tipo_vacancia.csv
│
├── notebooks/                             ← CÓDIGO: 6 notebooks Jupyter
│   ├── 00_planejamento_e_contexto.ipynb   ← contexto analítico
│   ├── 01_diagnostico_qualidade.ipynb     ← diagnóstico
│   ├── 02_limpeza_e_transformacao.ipynb   ← limpeza
│   ├── 02b_analise_exploratoria.ipynb     ← AED (gera os PNGs)
│   ├── 03_feature_engineering.ipynb       ← FE + agregação + norm + discr
│   └── 04_dataset_final.ipynb             ← consolidação + catálogo
│
├── documentacao/                          ← DOCUMENTAÇÃO
│   ├── problemas_qualidade.xlsx           ← 10 problemas (gerado NB 01)
│   ├── catalogo_dados.xlsx                ← catálogo (gerado NB 04)
│   ├── relatorio_final.docx               ← relatório final em Word
│   ├── relatorio_final.md                 ← versão markdown do relatório
│   ├── respostas_etapas_enunciado.md      ← respostas às etapas 6.1-6.17
│   ├── resultado_esperado.md              ← auto-avaliação (item 10)
│   └── guia_de_execucao.md                ← este arquivo
│
├── evidencias_aed/                        ← 7 gráficos PNG (gerado NB 02b)
│   ├── 03_histogramas_variaveis_principais.png
│   ├── 04_boxplots_variaveis_principais.png
│   ├── 05_top15_orgaos_vagas.png
│   ├── 06_distribuicao_nivel.png
│   ├── 07_vacancias_por_tipo.png
│   ├── 08_mapa_calor_correlacao.png
│   └── 09_boxplot_aprovada_por_nivel.png
│
├── orange/                                ← OPCIONAL: visualização visual
│   ├── GUIA_ORANGE.md                     ← como configurar Orange
│   └── fluxo_aed.ows                      ← (a gerar pelo aluno)
│
└── README.md                              ← visão geral do projeto
```

### Princípios da organização

- **`dados_brutos/`** nunca é modificado. Hot path imutável.
- **`dados_tratados/`** é totalmente regenerável — apague o conteúdo e rode os notebooks que ele reaparece.
- **`notebooks/`** usa caminhos relativos (`../dados_brutos/`, `../dados_tratados/`), então funciona em qualquer máquina.
- **`documentacao/`** consolida tudo que um avaliador precisa ler.

---

## 4. Ordem de execução dos notebooks

### Visão geral

| Ordem | Notebook | Tempo | Lê | Produz |
|---|---|---|---|---|
| 1 | `00_planejamento_e_contexto.ipynb` | <30s | CSV bruto | Apenas markdown (contexto) |
| 2 | `01_diagnostico_qualidade.ipynb` | ~30s | CSV bruto | `problemas_qualidade.xlsx` |
| 3 | `02_limpeza_e_transformacao.ipynb` | ~1 min | CSV bruto | `dataset_pos_limpeza.csv` |
| 4 | `02b_analise_exploratoria.ipynb` | ~1 min | `dataset_pos_limpeza.csv` | 7 PNGs em `evidencias_aed/` |
| 5 | `03_feature_engineering.ipynb` | ~30s | `dataset_pos_limpeza.csv` | `dataset_com_features.csv` + agregações |
| 6 | `04_dataset_final.ipynb` | ~10s | `dataset_com_features.csv` | `dataset_final_tratado.csv` + `catalogo_dados.xlsx` |

**Tempo total estimado:** 3-5 minutos em uma máquina padrão.

### Como iniciar o Jupyter

No terminal, na pasta-raiz do projeto:

```bash
cd notebooks/
jupyter notebook
```

Vai abrir o navegador no endereço `http://localhost:8888`. Clique no notebook que quer executar.

Alternativa: **Jupyter Lab**

```bash
cd notebooks/
jupyter lab
```

Interface mais moderna, com abas. Use o que preferir.

### Como executar um notebook

Em cada notebook aberto:

- **Menu:** `Run → Run All Cells` executa tudo do início ao fim
- **Atalho:** `Shift + Enter` executa a célula atual e passa para a próxima

As células com saída de texto vão mostrar tabelas, números e validações. Não pule células — algumas dependem das anteriores.

### O que esperar de output em cada notebook

**Notebook 00 — Planejamento e Contexto**

- Carrega a base bruta apenas para evidência factual
- Imprime números-chave (servidores ativos, taxa de ocupação geral, etc.)
- Não gera arquivos — é só leitura e markdown explicativo

**Notebook 01 — Diagnóstico de Qualidade**

- Análise dos 10 problemas
- No final, gera `documentacao/problemas_qualidade.xlsx`
- Verifique que o arquivo foi criado antes de seguir

**Notebook 02 — Limpeza e Transformação**

- Renomeia colunas, converte tipos, trata nulos
- Cria flag `is_outlier` (1.879 marcados)
- Gera `dados_tratados/dataset_pos_limpeza.csv` (12.769 × 21 colunas)

**Notebook 02b — Análise Exploratória**

- Carrega o CSV pós-limpeza
- Gera 7 gráficos PNG em `evidencias_aed/`
- Confira que os 7 arquivos foram criados:

```bash
ls evidencias_aed/
# Deve listar: 03_*.png, 04_*.png, 05_*.png, 06_*.png, 07_*.png, 08_*.png, 09_*.png
```

**Notebook 03 — Feature Engineering**

- Cria 9 features derivadas
- Aplica RobustScaler em 5 colunas
- Cria 2 discretizações
- Gera 3 agregações em `dados_tratados/agregacoes/`
- Gera `dados_tratados/dataset_com_features.csv` (12.769 × 37 colunas)

**Notebook 04 — Dataset Final e Catálogo**

- Valida 6 critérios de qualidade automatizados com `assert`
- Reorganiza 37 colunas em 9 blocos semânticos
- Gera os dois entregáveis principais:
  - `dados_tratados/dataset_final_tratado.csv`
  - `documentacao/catalogo_dados.xlsx`

Se algum `assert` falhar no Notebook 04, o pipeline **para** com mensagem clara — isso é um recurso de segurança, não um bug.

---

## 5. Reprodutibilidade

### Como verificar que tudo funcionou

Após executar os 6 notebooks na ordem, confira a lista de arquivos esperados:

```bash
# Datasets
ls dados_tratados/
# dataset_pos_limpeza.csv
# dataset_com_features.csv
# dataset_final_tratado.csv
# dataset_final_tratado.xlsx
# agregacoes/

# Documentação
ls documentacao/
# problemas_qualidade.xlsx
# catalogo_dados.xlsx
# ... (markdowns e relatório)

# Gráficos AED
ls evidencias_aed/
# 7 arquivos PNG
```

### Como saber que o dataset final tem os números certos

Abra um terminal Python na pasta `notebooks/` e rode:

```python
import pandas as pd
df = pd.read_csv('../dados_tratados/dataset_final_tratado.csv')
print(f"Shape: {df.shape}")
# Esperado: (12769, 37)

print(f"Total de servidores ativos: {df['qtd_ocupada'].sum():,}")
# Esperado próximo de: 474.000

print(f"Vacâncias totais: {df['total_vacancias'].sum():,}")
# Esperado: 280.125
```

Se os números baterem com os esperados, o pipeline rodou corretamente.

### Limpando para começar do zero

Se precisar regenerar tudo:

```bash
# Apaga apenas os arquivos gerados (preserva os brutos)
rm -rf dados_tratados/*
rm -rf evidencias_aed/*
rm -f documentacao/problemas_qualidade.xlsx
rm -f documentacao/catalogo_dados.xlsx
```

Depois rode os notebooks na ordem novamente.

---

## 6. Solução de problemas comuns

### "ModuleNotFoundError: No module named 'pandas'"

Falta instalar a biblioteca. Volte ao passo 2 e instale as dependências.

### "FileNotFoundError: dados_brutos/CargosVagosVacancias_202603.csv"

O notebook está sendo rodado de uma pasta errada. Confirme que está dentro de `notebooks/` quando inicia o Jupyter, ou ajuste o `BASE_DIR` na primeira célula.

### "AssertionError" no Notebook 04

O Notebook 04 tem validações automatizadas que param o pipeline se algo estiver inconsistente. A mensagem do `assert` indica exatamente qual critério falhou. Causas comuns:

- O dataset pós-limpeza ou com features não foi gerado (rode os notebooks 02 e 03 antes do 04)
- Alguma manipulação manual alterou os arquivos intermediários

### Saídas de gráficos não aparecem no Jupyter

Verifique se está com `%matplotlib inline` no início do notebook (já está em todos do projeto). Se ainda não aparecer, reinicie o kernel: `Kernel → Restart`.

### Erro ao salvar XLSX no Notebook 04

Pode ser permissão de arquivo. Feche o `dataset_final_tratado.xlsx` e o `catalogo_dados.xlsx` no Excel antes de rodar — o Windows trava o arquivo enquanto aberto.

### "Differences in pandas dtype output"

O Notebook 04 já é tolerante a pandas 2.x e 3.x. Se mesmo assim aparecer aviso de tipos, abra um issue.

---

## 7. Tempo total esperado para a primeira execução

| Etapa | Tempo |
|---|---|
| Instalar Anaconda (se for o caso) | 10-15 min |
| Instalar dependências adicionais | 1-2 min |
| Abrir o Jupyter | 30 segundos |
| Executar os 6 notebooks | 3-5 min |
| Verificar artefatos gerados | 2 min |
| **TOTAL** | **15-25 min** |

Execuções subsequentes (sem reinstalar): **5-10 minutos** do clique em "Run All" do Notebook 00 até o último arquivo do Notebook 04.

---

## 8. Para revisar/avaliar o projeto

Se você está avaliando o projeto (e não rodando), a ordem de leitura recomendada é:

1. **`README.md`** — visão geral
2. **`documentacao/respostas_etapas_enunciado.md`** — mapeamento direto às etapas 6.1-6.17
3. **`documentacao/resultado_esperado.md`** — auto-avaliação contra o item 10
4. **`documentacao/relatorio_final.docx`** — relatório formal completo
5. **`documentacao/catalogo_dados.xlsx`** — documentação de cada coluna
6. **`documentacao/problemas_qualidade.xlsx`** — diagnóstico inicial
7. **Notebooks na ordem 00 → 01 → 02 → 02b → 03 → 04** — código com markdown explicativo
8. **`dados_tratados/dataset_final_tratado.csv`** — produto final
9. **`evidencias_aed/`** — gráficos
10. **`orange/GUIA_ORANGE.md`** — visualização visual complementar (opcional)
