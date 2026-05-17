# Resultado Esperado — Auto-avaliação do projeto

> Este documento responde diretamente ao **item 10 do enunciado**: *"Ao final do PM3, espera-se que você consiga demonstrar domínio sobre o processo de preparação de dados para Business Intelligence."*

---

## O que o enunciado espera

O enunciado lista, em ordem, os seis pontos que o aluno precisa demonstrar:

1. Sair de uma **base bruta**
2. **Identificar problemas**
3. **Corrigir inconsistências**
4. **Transformar variáveis**
5. **Normalizar dados**
6. **Criar novas informações úteis**
7. **Documentar o dataset final**

E encerra com a frase-tese:

> *"Em outras palavras, você deverá provar que sabe preparar dados antes de analisá-los. No mundo real, essa etapa é decisiva. Um dashboard bonito com dados ruins continua sendo ruim — só que mais colorido."*

---

## Demonstração ponto a ponto

### 1. Sair de uma base bruta

**Sim, e o ponto de partida está preservado.**

A base original — `CargosVagosVacancias_202603.ods` — é o arquivo oficial publicado pela SEGES/MGI no Portal Brasileiro de Dados Abertos. Tem 12.769 linhas e 20 colunas, com 1.618 valores ausentes, tipos heterogêneos (datas como int, códigos com perda de zeros à esquerda), nomes de colunas em MAIÚSCULAS sem padrão, e inconsistências aritméticas em 14% dos registros.

O arquivo original **continua intacto** em `dados_brutos/` ao final do projeto. Nenhuma das operações do pipeline o modifica. Essa imutabilidade é um princípio de DataOps respeitado em todos os notebooks.

> **Evidência:** `dados_brutos/CargosVagosVacancias_202603.ods` (preservado) + `notebooks/01_diagnostico_qualidade.ipynb` (mostra a base como veio)

---

### 2. Identificar problemas

**Sim, 10 problemas catalogados de forma documentada.**

O Notebook 01 fez análise sistemática de qualidade, gerando `documentacao/problemas_qualidade.xlsx`. Os problemas identificados não foram pequenos — incluem:

- Nulos em 9,8% das linhas para `NIVEL`
- Datas armazenadas como inteiros
- Códigos identificadores que perderiam zeros se mantidos como inteiros
- Outliers extremos em variáveis-chave (max = 34.209 vs. mediana = 3)
- Inconsistências aritméticas entre `OCUPADA + VAGA` e `DISTRIBUIDA` em 1.787 linhas

Cada problema foi catalogado com **severidade**, **linhas afetadas** e **decisão de tratamento**. Nada foi escondido.

> **Evidência:** `documentacao/problemas_qualidade.xlsx` (10 problemas) + Notebook 01

---

### 3. Corrigir inconsistências

**Sim, e com decisões justificadas — não automáticas.**

O ponto crítico aqui é que **nem toda inconsistência foi "corrigida"**. Algumas foram preservadas como informação, porque o tratamento adequado depende do contexto:

| Inconsistência | Decisão técnica | Por quê |
|---|---|---|
| Nulos em `NIVEL` (1.255 linhas) | Preencher com "NAO_INFORMADO" | Remover linhas custaria 9,8% da base; imputar com moda distorceria |
| Tipos errados (datas como int) | Converter para datetime | Permite operações temporais |
| Códigos como int | Converter para str + zfill | Preserva zeros à esquerda, garante chaves consistentes |
| Outliers extremos em `qtd_aprovada` | **Preservar com flag** `is_outlier` | São cargos institucionais reais, não erros |
| `OCUPADA + VAGA ≠ DISTRIBUIDA` (14%) | **Materializar como feature** `diferenca_distribuicao` | A diferença é informação real (cessões, comissionamentos) |

A última coluna da tabela mostra o que torna esse projeto diferente de uma "limpeza ingênua": **decisões baseadas em entendimento do domínio**, não em receitas mecânicas.

> **Evidência:** Notebook 02, seções 3 (nulos) e 4 (outliers); Notebook 03, seção 1.8 (`diferenca_distribuicao`)

---

### 4. Transformar variáveis

**Sim, e ao longo de todo o pipeline.**

Transformações aplicadas:

- **Conversão de tipos:** int → datetime, int → string com zfill, object → category
- **Padronização de nomes:** 20 colunas em UPPERCASE → snake_case
- **Renomeação semântica:** `VACANCIA_POR_APOSENTADORIA` → `vac_aposentadoria`
- **Decomposição temporal:** `ano_mes` → `ano`, `mes`, `trimestre`
- **Discretização:** numéricas contínuas → categorias semânticas (`porte_cargo`, `faixa_taxa_ocupacao`)

Cada transformação **preserva informação** — qualquer registro pode ser rastreado de volta à base bruta.

> **Evidência:** Notebook 02 (transformações básicas); Notebook 03, seções 1 e 4 (decomposição e discretização)

---

### 5. Normalizar dados

**Sim, com discussão técnica do trade-off entre métodos.**

A etapa 6.12 do enunciado pede a aplicação de normalização em pelo menos uma variável. O projeto fez **mais do que isso**: aplicou RobustScaler em 5 variáveis-chave, mas também comparou explicitamente com MinMax e StandardScaler para mostrar **por que** RobustScaler é a escolha técnica adequada para esta base.

A comparação está documentada em uma tabela de percentis no Notebook 03, seção 3.4 — que evidencia que MinMax esmaga 75% dos cargos abaixo de 0,0005, e StandardScaler distorce a média pelos outliers.

A justificativa para a escolha está amarrada à característica específica desta base (outliers reais, não erros) — não é uma receita aplicada sem reflexão.

> **Evidência:** Notebook 03, seção 3; 5 colunas `*_robust` no dataset final

---

### 6. Criar novas informações úteis

**Sim, 17 colunas novas adicionadas ao dataset final.**

A base original tinha 20 colunas. O dataset final tem 37 — sendo 17 novas. Não foram criadas para "engordar":

| Tipo de feature criada | Quantidade | Justificativa analítica |
|---|---|---|
| Features quantitativas derivadas | 6 | KPIs ligados às 11 perguntas analíticas |
| Features temporais | 3 | Compatibilidade com séries históricas futuras |
| Versões normalizadas para ML | 5 | Insumos para clustering/classificação |
| Discretizações categóricas | 2 | Segmentação executiva interpretável |
| Flag de outlier | 1 | Permite análises segmentadas |

Cada uma está documentada no catálogo de dados com fórmula, origem e uso esperado.

> **Evidência:** Notebook 03, seções 1 (FE), 3 (normalização) e 4 (discretização); `documentacao/catalogo_dados.xlsx`

---

### 7. Documentar o dataset final

**Sim, com múltiplos artefatos de documentação interligados.**

Esse é o ponto onde o projeto vai além do mínimo:

| Artefato de documentação | Conteúdo |
|---|---|
| `catalogo_dados.xlsx` | 37 colunas × 8 atributos, com formatação profissional + planilha de metadados |
| `relatorio_final.docx` (e `.md`) | 23 seções cobrindo todo o pipeline |
| `problemas_qualidade.xlsx` | Tabela dos 10 problemas com severidade e decisão |
| Markdown explicativo nos 6 notebooks | Cada decisão técnica justificada inline |
| `README.md` | Visão geral, estrutura, ordem de execução |
| `respostas_etapas_enunciado.md` | Mapeamento direto das perguntas do enunciado |
| `guia_de_execucao.md` | Passo a passo para reprodução |

A construção do catálogo inclui uma validação automatizada com `assert`: o conjunto de nomes do catálogo precisa coincidir exatamente com o conjunto de colunas do dataset. Isso impede que o catálogo divirja do dataset em futuras iterações.

> **Evidência:** todos os arquivos em `documentacao/` + Notebook 04, seção 4

---

## Sobre a frase-tese do enunciado

> *"Um dashboard bonito com dados ruins continua sendo ruim — só que mais colorido."*

Três achados deste projeto comprovam essa tese empiricamente:

### Achado 1 — Removendo outliers, esconde-se a maior parte do governo

O método IQR clássico identifica 1.879 cargos como outliers. Um analista descuidado removeria essas linhas e ficaria com uma base "limpa" — perdendo justamente os cargos institucionais mais relevantes: Técnico Administrativo em Educação, cargos do INSS, da Polícia Federal, da Receita.

Um dashboard construído sobre essa base "filtrada" mostraria um Executivo Federal **fictício** — sem suas principais carreiras. Bonito, mas completamente errado.

### Achado 2 — A média das taxas individuais ≠ taxa agregada

76% dos cargos individuais estão "completos" (≥90% de ocupação). Mas a taxa agregada do governo é apenas 67%. O paradoxo de Simpson aplicado a proporções.

Um dashboard que usasse `mean(taxa_ocupacao)` reportaria que o Executivo Federal está em "saúde excelente" (≈95% de média). Errado. A métrica correta para reportar saúde institucional é `sum(ocupada) / sum(aprovada)` — que dá 67%.

**Sem tratamento e documentação cuidadosa**, esse erro de métrica seria invisível para o consumidor final do dashboard.

### Achado 3 — Aposentadoria não é turnover

76,7% das vacâncias do Executivo Federal em 03/2026 foram por aposentadoria. Um dashboard de RH típico, usando modelos de turnover convencionais (que tratam saída como decisão voluntária do servidor), interpretaria essa estatística como "rotatividade alta".

A interpretação correta — visível apenas com a feature `pct_aposentadoria` criada nesta engenharia — é que se trata de **transição demográfica**, não rotatividade. A política pública apropriada (reposição via concurso, baseada em projeções etárias) é radicalmente diferente da política de retenção que um dashboard mal calibrado sugeriria.

---

## Síntese da auto-avaliação

| Critério do item 10 | Cumprido? | Evidência principal |
|---|---|---|
| Sair de uma base bruta | ✅ | Base original preservada em `dados_brutos/` |
| Identificar problemas | ✅ | 10 problemas catalogados (`problemas_qualidade.xlsx`) |
| Corrigir inconsistências | ✅ | Decisões justificadas, não automáticas |
| Transformar variáveis | ✅ | Tipos, nomes, decomposição temporal, discretização |
| Normalizar dados | ✅ | RobustScaler em 5 colunas + comparação com MinMax/StandardScaler |
| Criar novas informações úteis | ✅ | 17 features novas, todas com utilidade documentada |
| Documentar o dataset final | ✅ | 7 artefatos de documentação interligados |
| Demonstrar que isso evita "dashboard bonito com dados ruins" | ✅ | 3 achados empíricos no próprio projeto |

**Conclusão:** o projeto cumpre integralmente o resultado esperado pelo item 10 do enunciado, demonstrando domínio do processo completo de preparação de dados — da identificação dos problemas à documentação final, com decisões técnicas justificadas em cada passo.
