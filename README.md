# PM3 — Tratamento de Dados: Cargos Vagos e Vacâncias (SEGRT/Executivo Federal)

**Projeto Mensal 3 — Disciplina de Big Data Analytics / BI / Data Mining**

**Equipe:** Heron Felipe Juvenil Divino, Jihad Riad Ghozayel, Nicolas Gabriel Correa Martão, Thiago Andre Simonetti

---

## 1. Sobre o projeto

Este projeto realiza o **tratamento completo de uma base de dados real** do Governo Federal Brasileiro, partindo do dado bruto e chegando a um dataset final preparado para uso em Business Intelligence e Data Mining.

O foco está nas etapas de **preparação de dados** (qualidade, limpeza, transformação, normalização, feature engineering e documentação) — não na construção de dashboards ou modelos preditivos.

## 2. Sobre a base

- **Nome:** Cargos Vagos e Vacâncias do Poder Executivo Federal Civil
- **Período:** Março/2026 (competência 202603)
- **Fonte:** Portal Brasileiro de Dados Abertos — [dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---cargos-vagos-e-vacancias)
- **Órgão responsável:** Secretaria de Gestão e Inovação (SEGES) / Ministério da Gestão e da Inovação em Serviços Públicos
- **Arquivo original:** `CargosVagosVacancias_202603.ods`
- **Aba utilizada:** `por_Órgao_e_Cargo` (12.769 linhas × 20 colunas)
- **Dicionário oficial:** [Dicionario_CargosVagosVacancias.pdf](https://repositorio.dados.gov.br/segrt/cargos%20vagos%20e%20vacancia/2026/Dicionario_CargosVagosVacancias.pdf)

## 3. Estrutura do projeto

```
PM3_CargosVagosVacancias/
│
├── dados_brutos/
│   ├── CargosVagosVacancias_202603.ods   (arquivo original preservado)
│   └── CargosVagosVacancias_202603.csv   (versão CSV para o Orange)
│
├── dados_tratados/
│   ├── dataset_pos_limpeza.csv           (gerado no Notebook 02)
│   ├── dataset_com_features.csv          (gerado no Notebook 03)
│   ├── agregacoes/                       (geradas no Notebook 03)
│   │   ├── agg_por_orgao.csv
│   │   ├── agg_por_nivel.csv
│   │   └── agg_por_tipo_vacancia.csv
│   └── dataset_final_tratado.csv         (gerado no Notebook 04)
│
├── notebooks/
│   ├── 00_planejamento_e_contexto.ipynb  (etapas 6.1 e 6.2 — contexto analítico)
│   ├── 01_diagnostico_qualidade.ipynb
│   ├── 02_limpeza_e_transformacao.ipynb
│   ├── 02b_analise_exploratoria.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_dataset_final.ipynb
│
├── orange/
│   ├── GUIA_ORANGE.md                    (instruções para AED visual)
│   └── fluxo_aed.ows                     (a ser gerado pelo aluno no Orange)
│
├── documentacao/
│   ├── problemas_qualidade.xlsx          (gerado no Notebook 01)
│   ├── catalogo_dados.xlsx               (gerado no Notebook 04)
│   ├── relatorio_final.docx              (relatório final completo)
│   ├── relatorio_final.md                (versão markdown do relatório)
│   ├── respostas_etapas_enunciado.md     (respostas às etapas 6.1-6.17)
│   ├── resultado_esperado.md             (auto-avaliação contra item 10)
│   ├── guia_de_execucao.md               (como rodar o projeto)
│   └── guia_orange_visualizacao.md       (visualização no Orange)
│
├── evidencias_aed/
│   └── *.png                             (gráficos gerados pelos notebooks)
│
└── README.md                             (este arquivo)
```

## 4. Ordem de execução

Execute os notebooks na seguinte sequência:

| Ordem | Notebook | Etapas do enunciado |
|------|----------|---------------------|
| 1 | `00_planejamento_e_contexto.ipynb` | **6.1, 6.2** (planejamento e relação com BI/BDA/DM) |
| 2 | `01_diagnostico_qualidade.ipynb` | 6.3, 6.4 |
| 3 | `02_limpeza_e_transformacao.ipynb` | 6.6, 6.7, 6.8, 6.9, 6.10 |
| 4 | `02b_analise_exploratoria.ipynb` | 6.5 (Análise Exploratória de Dados) |
| 5 | `03_feature_engineering.ipynb` | 6.11, 6.12, 6.13, 6.14 |
| 6 | `04_dataset_final.ipynb` | 6.15, 6.16 |

Cada notebook contém células de **markdown explicativo** que podem ser copiadas diretamente para o relatório final.

## 4.1 Para avaliação rápida

Se você está revisando o projeto e quer ir direto ao essencial, leia nesta ordem:

| # | Arquivo | O que tem |
|---|---|---|
| 1 | `README.md` | Visão geral e estrutura |
| 2 | `documentacao/respostas_etapas_enunciado.md` | Respostas diretas às 17 etapas do enunciado |
| 3 | `documentacao/resultado_esperado.md` | Auto-avaliação contra o item 10 |
| 4 | `documentacao/relatorio_final.docx` | Relatório formal completo (23 seções) |
| 5 | `documentacao/catalogo_dados.xlsx` | Documentação das 37 colunas do dataset final |
| 6 | `documentacao/problemas_qualidade.xlsx` | 10 problemas de qualidade identificados |
| 7 | `documentacao/guia_de_execucao.md` | Como reproduzir o pipeline |
| 8 | Notebooks 00 → 01 → 02 → 02b → 03 → 04 | Código com markdown inline |
| 9 | `dados_tratados/dataset_final_tratado.csv` | Produto final |
| 10 | `documentacao/guia_orange_visualizacao.md` | Visualização visual complementar (opcional) |

## 5. Reprodutibilidade

Para reproduzir os resultados:

```bash
# 1. Instalar dependências (apenas as estritamente necessárias)
pip install pandas numpy matplotlib seaborn openpyxl jupyter scikit-learn

# 2. Abrir os notebooks
cd notebooks/
jupyter notebook
```

> **Nota:** os notebooks leem a base a partir do arquivo `.csv` em `dados_brutos/` (conversão fiel do `.ods` original). Isso elimina a necessidade da biblioteca `odfpy` e garante que o código rode em qualquer ambiente Python padrão, incluindo Anaconda. O arquivo `.ods` original permanece preservado como referência da fonte oficial.

Os notebooks usam **caminhos relativos** (`../dados_brutos/`, etc.), então funcionam de qualquer máquina desde que a estrutura de pastas seja preservada.

## 6. Bibliotecas utilizadas

| Biblioteca | Função |
|---|---|
| `pandas` | Manipulação de DataFrames |
| `numpy` | Operações numéricas, `linspace` para discretização |
| `matplotlib` | Gráficos estáticos |
| `seaborn` | Gráficos estatísticos (boxplot, heatmap) |
| `openpyxl` | Leitura/escrita de XLSX |
| `odfpy` | Leitura do arquivo ODS original |
| `scikit-learn` | Normalização/padronização (RobustScaler, MinMax, StandardScaler) |

Ferramenta de apoio visual: **Orange Data Mining** v3.36+

## 7. Referências bibliográficas (para o relatório)

- BRASIL. **Secretaria de Gestão e Inovação (SEGES).** Conjunto de dados: Cargos Vagos e Vacâncias do Poder Executivo Federal Civil. Disponível em: https://dados.gov.br. Acesso em: 2026.
- BRASIL. **Lei nº 8.112/90**, art. 33 — Vacância no Regime Jurídico dos Servidores Públicos Civis da União.
- CASTRO, L. N.; FERRARI, D. G. *Introdução à mineração de dados: conceitos básicos, algoritmos e aplicações.* São Paulo: Saraiva, 2016.
- GOLDSCHMIDT, R.; BEZERRA, E.; PASSOS, E. *Data mining: conceitos, técnicas, algoritmos, orientações e aplicações.* Rio de Janeiro: Elsevier, 2015.
- CERCHIARI DE ANDRADE, A. L. *Preparação e análise exploratória de dados.* SAGAH, [s.d.].
