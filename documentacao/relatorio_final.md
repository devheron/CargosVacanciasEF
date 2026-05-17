# Relatório Final — PM3: Tratamento de Dados

**Cargos Vagos e Vacâncias do Poder Executivo Federal Civil — competência 03/2026**

**Disciplina:** Big Data Analytics / BI / Data Mining  
**Projeto Mensal 3:** Tratamento de Dados  
**Base utilizada:** SEGES/MGI — Cargos Vagos e Vacâncias (03/2026)  
**Equipe:*8 Heron Felipe Juvenil Divino, Jihad Riad Ghozayel, Nicolas Gabriel Correa Martão, Thiago Andre Simonetti
**Data:** 17/05/2026


---

## Sumário

1. Introdução
2. Tema escolhido
3. Fonte dos dados
4. Objetivo da análise
5. Descrição da base original
6. Relação da base com BI, Big Data Analytics e Data Mining
7. Diagnóstico da qualidade dos dados
8. Análise Exploratória de Dados (AED)
9. Seleção das variáveis
10. Limpeza e pré-processamento
11. Tratamento de valores faltantes
12. Tratamento de outliers
13. Transformações realizadas
14. Agregações realizadas
15. Normalização e padronização
16. Discretização
17. Feature Engineering
18. Descrição do dataset final
19. Catálogo de dados
20. Organização DataOps
21. Conclusão
22. Limitações
23. Próximos passos
- Referências bibliográficas

---

## 1. Introdução

O presente trabalho corresponde ao **Projeto Mensal 3** da disciplina, cujo foco é o tratamento completo de uma base de dados real — desde sua versão bruta até um dataset final preparado, documentado e pronto para uso em Business Intelligence (BI) e Data Mining (DM). Como destaca o próprio enunciado, "um dashboard bonito com dados ruins continua sendo ruim — só que mais colorido". O projeto reforça essa premissa: antes de qualquer análise sofisticada, é preciso garantir a **qualidade do dado**.

A base escolhida para o projeto foi a de **Cargos Vagos e Vacâncias do Poder Executivo Federal Civil**, publicada mensalmente pela Secretaria de Gestão e Inovação (SEGES) do Ministério da Gestão e da Inovação em Serviços Públicos (MGI), disponibilizada via Portal Brasileiro de Dados Abertos (dados.gov.br). Trata-se de uma base oficial, com licença CC BY 4.0, contendo a fotografia mensal do quadro de pessoal de cada órgão da administração federal — quantos cargos foram aprovados em lei, quantos estão ocupados, quantos estão vagos, e o fluxo de servidores que saíram no mês por sete causas distintas (aposentadoria, exoneração, demissão, promoção, readaptação, posse em outro cargo inacumulável e falecimento).

O tratamento foi conduzido em uma estrutura de **seis notebooks Jupyter sequenciais**, do `00_planejamento_e_contexto.ipynb` ao `04_dataset_final.ipynb`, cada um responsável por uma etapa específica do enunciado. Todas as decisões técnicas estão justificadas no código e replicadas neste relatório. O dataset final entregue tem **12.769 registros e 37 colunas** — partindo de 20 colunas originais e adicionando 17 colunas derivadas (features de engenharia, normalizações e discretizações), todas documentadas no catálogo de dados (`catalogo_dados.xlsx`).

Este relatório consolida os achados de todas as etapas, respondendo à exigência do enunciado de que "não basta mostrar código; é necessário explicar o que foi feito".

---

## 2. Tema escolhido

O tema é a **gestão quantitativa de pessoas no Poder Executivo Federal Civil brasileiro**. A base apresenta, mês a mês, o estoque e o fluxo do quadro de servidores em cada órgão da administração federal direta, autárquica e fundacional. A unidade de análise é a combinação **(órgão × cargo)** — cada linha corresponde a uma carreira específica dentro de um órgão específico, em uma competência específica.

A relevância do tema está em três frentes:

Primeiro, é um tema de **interesse público direto**. As decisões tomadas com base nesta análise impactam a folha de pagamento da União (uma das maiores rubricas do Orçamento Federal), o tempo de espera por serviços públicos (INSS, Receita Federal, universidades) e a qualidade da entrega governamental como um todo.

Segundo, é um caso **rico em problemas de qualidade de dados** — exatamente o objetivo pedagógico do PM3. A base contém valores ausentes em campos categóricos, inconsistências aritméticas entre colunas relacionadas, alta assimetria com outliers legítimos, e categorias que precisam de padronização. Não é uma base "limpa", o que torna o trabalho de tratamento substantivo.

Terceiro, é um tema com **clara aplicação em BI e DM**. As medidas (vagas aprovadas, ocupadas, vacâncias) são aditivas e suportam dashboards executivos. As dimensões (órgão, cargo, nível, plano de carreira) permitem segmentação rica. E o conjunto de variáveis permite aplicar tarefas clássicas de Data Mining como clustering, detecção de anomalias e regras de associação.

---

## 3. Fonte dos dados

| Atributo | Detalhe |
|---|---|
| **Fonte primária** | Portal Brasileiro de Dados Abertos — `dados.gov.br` |
| **Conjunto de dados** | "Cargos Vagos e Vacâncias do Poder Executivo Federal Civil" |
| **URL** | https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---cargos-vagos-e-vacancias |
| **Órgão produtor** | Secretaria de Gestão e Inovação (SEGES) — Ministério da Gestão e da Inovação em Serviços Públicos (MGI) |
| **Arquivo utilizado** | `CargosVagosVacancias_202603.ods`, aba `por_Órgao_e_Cargo` |
| **Competência analisada** | Março/2026 (snapshot mensal) |
| **Periodicidade da publicação** | Mensal, com séries históricas disponíveis |
| **Licença** | Dados abertos sob CC BY 4.0 |
| **Dicionário oficial** | `Dicionario_CargosVagosVacancias.pdf` (anexo ao conjunto de dados) |
| **Data de acesso** | 2026 |

A escolha pela aba `por_Órgao_e_Cargo` (12.769 linhas) em vez da aba agregada `por_Órgao` (211 linhas) se justifica tecnicamente: a base detalhada permite todas as análises da base agregada e mais várias outras, enquanto o inverso não é verdadeiro. Como o objetivo do projeto é demonstrar técnicas de tratamento, é desejável ter a granularidade máxima.

Em conformidade com o requisito do enunciado de preservação da base original, o arquivo `.ods` ficou intacto na pasta `dados_brutos/`, e uma cópia em `.csv` foi gerada para facilitar a leitura pelos notebooks (eliminando a dependência da biblioteca `odfpy`).

---

## 4. Objetivo da análise

O objetivo geral é **partir de uma base bruta governamental e entregar um dataset tratado, documentado e analiticamente útil**, capaz de responder a perguntas concretas sobre a gestão de pessoas do Executivo Federal e de servir de insumo para projetos de BI e DM.

As **onze perguntas analíticas norteadoras**, definidas no início do projeto, são:

**Perguntas descritivas (BI clássico):**

1. Quais órgãos do Executivo Federal têm mais vagas em aberto em 03/2026?
2. Qual a taxa de ocupação média do governo federal? E por nível de escolaridade?
3. Quais são os 10 cargos com maior quantitativo total no Executivo?
4. Quanto pesa a aposentadoria como causa de vacância, comparada às outras seis causas?
5. Quantos cargos estão formalmente em extinção e em quais órgãos eles ainda têm ocupantes?

**Perguntas comparativas e segmentadas:**

6. Cargos de Nível Superior têm taxa de ocupação maior ou menor que cargos de Nível Intermediário?
7. Órgãos pequenos (poucas vagas aprovadas) têm comportamento de vacância diferente dos grandes?
8. A vacância por exoneração se concentra em algum tipo específico de carreira?

**Perguntas estruturais (Data Mining):**

9. É possível agrupar os 211 órgãos em "perfis" distintos com base na composição do seu quadro?
10. Existem cargos que tendem a coexistir nos mesmos órgãos (regras de associação)?
11. Há outliers que mereçam tratamento separado (cargos institucionais gigantes)?

Cada coluna mantida, cada feature criada, cada transformação aplicada teve como justificativa servir a pelo menos uma dessas perguntas — atendendo à orientação do enunciado de que "as novas variáveis precisam ter utilidade analítica".

---

## 5. Descrição da base original

A base bruta tem as seguintes características:

| Característica | Valor |
|---|---|
| **Registros** | 12.769 linhas |
| **Colunas** | 20 |
| **Órgãos distintos** | 211 |
| **Cargos distintos** | 1.043 códigos |
| **Planos de carreira distintos** | 84 |
| **Competência** | uma única (março/2026) |
| **Tamanho do arquivo `.ods`** | ~3 MB |

As 20 colunas originais estão agrupadas semanticamente em quatro blocos:

**Identificação temporal (1 coluna):** `ANO_MES` — competência mensal (formato int AAAAMM, ex.: 202603).

**Identificação do órgão e do cargo (7 colunas):** `ORGAO`, `NOME_ORGAO`, `SIGLA_ORGAO`, `CARGO`, `NOME_CARGO`, `NIVEL` (escolaridade exigida: NS, NI, NM), `PLANO_CARREIRA`, e `CARGO_EM_EXTINCAO` (S/N).

**Quantitativos brutos (4 colunas):** `APROVADA` (teto legal de servidores), `DISTRIBUIDA` (vagas distribuídas ao órgão), `OCUPADA` (vagas ocupadas), `VAGA` (vagas em aberto).

**Vacâncias por tipo (7 colunas):** `VACANCIA_POR_EXONERACAO`, `VACANCIA_POR_DEMISSAO`, `VACANCIA_POR_PROMOCAO`, `VACANCIA_POR_READAPTACAO`, `VACANCIA_POR_APOSENTADORIA`, `VACANCIA_POR_POSSE_CARGO_INAC`, `VACANCIA_POR_FALECIMENTO`.

A base atende todos os critérios mínimos exigidos pelo enunciado (mais de 300 registros, mais de 6 colunas úteis, presença de variáveis numéricas e categóricas, e — crucialmente — presença de problemas de qualidade que justifiquem o tratamento).

Alguns números factuais extraídos diretamente da base bruta, para ancorar o contexto:

- **Total de servidores ativos no Executivo Federal Civil em 03/2026:** ~474 mil
- **Total de vagas aprovadas em lei (teto):** ~708 mil
- **Taxa de ocupação federal geral:** aproximadamente 66,9%
- **Vacâncias no mês:** 280.125 movimentações, sendo **76,7% por aposentadoria** sozinha
- **Cargos formalmente em extinção:** aproximadamente 28% da base

---

## 6. Relação da base com BI, Big Data Analytics e Data Mining

Esta seção responde à exigência da etapa 6.2 do enunciado, aplicando os três conceitos ao tema específico do projeto (e não como definições genéricas).

### 6.1 Aplicação em Business Intelligence

A combinação `(órgão × cargo)` é uma chave dimensional natural para um modelo OLAP. As colunas quantitativas (`aprovada`, `distribuida`, `ocupada`, `vaga`) são medidas aditivas. Isso permite construir dashboards e relatórios diretamente em ferramentas como Power BI, Looker Studio, Tableau ou Metabase.

Algumas aplicações concretas de BI sobre esta base:

- **Painel executivo do MGI:** taxa de ocupação federal, ranking de órgãos deficitários, ranking dos cargos com maior número de aposentadorias previstas, evolução mensal das vacâncias por tipo.
- **Painel por ministério:** o gestor de um ministério específico vê apenas seus órgãos vinculados, drill-down em cargos.
- **Painel por carreira:** distribuição de uma carreira específica (ex.: "Auditor Fiscal") entre os órgãos onde existe.
- **Indicadores derivados:** `taxa de ocupação = ocupada/aprovada`, `déficit nominal = aprovada - ocupada`, `taxa de vacância = total_vacancias/ocupada` — todos criados como features no Notebook 03.
- **Drill-down hierárquico:** `Executivo Federal → Ministério → Órgão → Plano de Carreira → Cargo Específico`.

### 6.2 Aplicação em Big Data Analytics

A análise honesta dos chamados "5 Vs" do Big Data, aplicada à base:

**Volume:** isoladamente, 12.769 linhas não é "big" — cabem em qualquer computador. No entanto, a base é publicada **mensalmente** há mais de uma década, e a série histórica acumulada gera mais de 1,5 milhão de registros — começa a justificar arquitetura analítica robusta.

**Variedade:** sim — a base mistura identificadores hierárquicos (códigos de órgão, cargo), categorias (nível, plano, em_extinção), e quantitativos inteiros. Em projetos reais, seria integrada a outras bases federais (SIAPE para folha, RAIS para mercado de trabalho, IBGE para dados populacionais).

**Velocidade:** moderada — publicação mensal, processamento batch. Suficiente para o caso de uso (planejamento estratégico de pessoal).

**Veracidade:** alta — fonte governamental oficial, com dicionário e regras de extração documentadas. Os problemas de qualidade identificados são marginais e tratáveis.

**Valor:** alto — decisões de concurso público envolvem bilhões de reais por ano em folha; um modelo analítico baseado nesta base impacta diretamente esse gasto.

Em resumo: o snapshot atual não é Big Data em volume, mas é a **unidade básica de um pipeline de BDA** quando combinada com séries históricas e outras bases federais.

### 6.3 Aplicação em Data Mining

Enquanto o BI responde a perguntas pré-formuladas, o DM **descobre** padrões. As tarefas clássicas se aplicam à base assim:

**Clustering (agrupamento).** Os 211 órgãos podem ser agrupados em perfis típicos a partir do quadro: "órgãos prestadores de serviço com alta rotatividade", "órgãos reguladores enxutos e estáveis", "órgãos universitários com grandes quadros docentes". Algoritmos: K-Means, Hierarchical Clustering, DBSCAN — usando as features normalizadas (`*_robust`) criadas no Notebook 03.

**Detecção de anomalias.** Cargos com taxa de vacância anormalmente alta sem justificativa estrutural; órgãos onde a soma das vacâncias está acima do esperado para o tamanho do quadro. Já implementamos uma versão simples disso com a flag `is_outlier` (método IQR).

**Regras de associação.** Quais cargos tendem a coexistir nos mesmos órgãos? Algoritmos como Apriori ou FP-Growth podem identificar padrões como "todo órgão que tem cargo X também tem cargo Y" — estrutura típica de órgão de fiscalização, por exemplo.

**Classificação supervisionada.** Dado o perfil de um cargo, classificar se tende a estar "em extinção" ou "ativo". Variáveis preditoras: nível, plano, tamanho do quadro, perfil de vacância.

**Análise preditiva.** Com a série histórica, projetar quantas vacâncias por aposentadoria cada órgão terá nos próximos 12 meses — insumo direto para planejamento de concursos.

### Tabela-resumo

| Área | Tarefa concreta | Variáveis-chave usadas | Entrega típica |
|---|---|---|---|
| BI | Dashboard executivo de gestão de pessoal | `nome_orgao`, quantitativos | Painel Power BI |
| BI | KPIs (taxa de ocupação, déficit) | features derivadas | KPIs + rankings |
| BDA | Pipeline mensal com versionamento histórico | toda a base + metadado | Data Lake + catálogo |
| DM | Clustering de órgãos por perfil | features normalizadas | Segmentação |
| DM | Detecção de anomalias | `vac_*`, `taxa_*` | Lista priorizada para auditoria |
| DM | Regras de associação | `cod_cargo` × `cod_orgao` | Padrões estruturais |

---

## 7. Diagnóstico da qualidade dos dados

A análise de qualidade foi conduzida no Notebook 01 (`01_diagnostico_qualidade.ipynb`) e gerou a planilha `documentacao/problemas_qualidade.xlsx` com **10 problemas catalogados**.

| # | Problema | Severidade | Linhas afetadas | Decisão de tratamento |
|---|---|---|---|---|
| P01 | Coluna `NIVEL` com 1.255 valores nulos (9,8%) | Média | 1.255 | Preencher com "NAO_INFORMADO" |
| P02 | Coluna `PLANO_CARREIRA` com 363 nulos (2,8%) | Baixa | 363 | Preencher com "NAO_INFORMADO" |
| P03 | `ANO_MES` armazenado como inteiro (ex.: 202603) | Baixa | 12.769 | Converter para datetime |
| P04 | `ORGAO` e `CARGO` como int (perde zeros à esquerda) | Média | 12.769 | Converter para str com zfill |
| P05 | Nomes de colunas em MAIÚSCULAS, sem padrão | Baixa | todas | Padronizar para snake_case |
| P06 | Categóricas como object (desperdício de memória) | Baixa | 4 cols | Converter para category |
| P07 | Alta assimetria em `APROVADA` (max=34.209, mediana=3) | Alta | distribuição | Manter — outliers legítimos |
| P08 | Inconsistência: `OCUPADA + VAGA ≠ DISTRIBUIDA` em ~14% das linhas | Média | 1.787 | Materializar como feature `diferenca_distribuicao` |
| P09 | Outliers em `APROVADA` por IQR (1.879 cargos) | Alta | 1.879 | Marcar com flag, **não remover** |
| P10 | Ausência de variáveis derivadas analíticas | — | — | Criar 9 features no Notebook 03 |

**Sobre os outliers (P09):** o método IQR identifica 1.879 cargos como "atípicos". Uma análise apressada removeria essas linhas. Porém, esses outliers são **justamente** os cargos institucionais mais relevantes do Executivo Federal — Técnico Administrativo em Educação (34.209 aprovadas), cargos do INSS, da Polícia Federal, da Receita. Removê-los empobreceria gravemente a análise. A decisão foi **preservá-los com uma flag** (`is_outlier`), permitindo análises segmentadas posteriores.

**Sobre a inconsistência aritmética (P08):** em 14% dos cargos, a soma `OCUPADA + VAGA` não bate com `DISTRIBUIDA`. Investigando, essa diferença reflete fenômenos reais (servidores cedidos de outros órgãos, comissionamentos, duplo vínculo). Não é erro de dados — é informação. Por isso a diferença foi materializada como uma feature (`diferenca_distribuicao`) em vez de "corrigida".

A planilha `problemas_qualidade.xlsx` contém todas as informações em formato tabular para consulta rápida.

---

## 8. Análise Exploratória de Dados (AED)

A AED foi conduzida no Notebook 02b (`02b_analise_exploratoria.ipynb`) e gerou **7 gráficos em PNG** salvos em `evidencias_aed/`. Os principais achados:

**Gráfico 03 — Histogramas das variáveis principais** (`03_histogramas_variaveis_principais.png`)

As distribuições de `qtd_aprovada`, `qtd_ocupada` e `qtd_vaga` são **fortemente assimétricas à direita**, com mediana próxima de zero e cauda longa. Foi necessário aplicar escala logarítmica para visualizar a estrutura. Esse padrão confirma que a base é dominada por **cargos pequenos** (a maioria dos cargos tem 1-2 vagas aprovadas) e uma pequena fração de **cargos institucionais gigantes**.

**Gráfico 04 — Boxplots das variáveis principais** (`04_boxplots_variaveis_principais.png`)

Os boxplots tornam a presença dos outliers explícita: praticamente todos os pontos plotados fora da caixa são valores legítimos, não erros. Esse gráfico foi a evidência visual usada para sustentar a decisão de preservar os outliers via flag.

**Gráfico 05 — Top 15 órgãos por vagas aprovadas** (`05_top15_orgaos_vagas.png`)

Os 15 maiores órgãos concentram a maior parte da força de trabalho federal. Ministério da Saúde (MS), Ministério da Fazenda (MF), INSS, MEC, Departamento de Polícia Federal (DPF) e UFRJ aparecem entre os primeiros. A distribuição é extremamente concentrada — uma das justificativas para futuras análises de clustering.

**Gráfico 06 — Distribuição por nível de escolaridade** (`06_distribuicao_nivel.png`)

Cargos de Nível Superior (NS) e Nível Intermediário (NI) têm volumes próximos (cerca de 5,7 mil cada). Cargos de Nível Médio (NM) são raros (apenas 10 códigos distintos). Há 1.255 cargos com nível "NAO_INFORMADO" — preenchidos no tratamento.

**Gráfico 07 — Vacâncias por tipo** (`07_vacancias_por_tipo.png`)

**Achado mais marcante da AED:** aposentadoria sozinha responde por **76,7%** de todas as vacâncias do mês. Posse em outro cargo inacumulável (8,2%) e exoneração (7,4%) vêm em seguida. Demissão, promoção e readaptação somam menos de 2%. Este gráfico é a evidência empírica da tese central do projeto: o Executivo Federal está sob **pressão estrutural de reposição por envelhecimento**, não por rotatividade voluntária.

**Gráfico 08 — Mapa de calor de correlação** (`08_mapa_calor_correlacao.png`)

Como esperado, há fortíssima correlação positiva entre `aprovada`, `distribuida`, `ocupada` e `vaga` (>0,9) — quanto maior o cargo, maior todas essas medidas em valor absoluto. As correlações entre vacâncias específicas e ocupada são moderadas, sugerindo que tipos diferentes de vacância têm dinâmicas distintas.

**Gráfico 09 — Boxplot de aprovada por nível** (`09_boxplot_aprovada_por_nivel.png`)

Confirma que cargos de Nível Superior tendem a ter, em média, mais vagas aprovadas que os de Nível Intermediário, mas com sobreposição substancial entre as duas distribuições. Os outliers extremos aparecem nos dois níveis.

> *Nota para o relatório em Word: as imagens dos sete gráficos estão em `evidencias_aed/`. Inserir na ordem citada acima, com legenda mantendo o nome do arquivo entre parênteses para rastreabilidade.*

---

## 9. Seleção das variáveis

Conforme a etapa 6.6 do enunciado, é necessário justificar quais variáveis foram mantidas e quais foram descartadas.

**Decisão:** todas as 20 colunas originais foram mantidas, e nenhum registro foi filtrado.

**Justificativa para manter todas as colunas:**

- **Identificação temporal e do órgão/cargo (8 cols):** essenciais como dimensões para qualquer análise em BI.
- **Quantitativos brutos (4 cols):** medidas básicas, nucleares para todos os KPIs.
- **Vacâncias por tipo (7 cols):** cada tipo representa uma causa distinta com semântica jurídica diferente (Lei 8.112/90). Mesmo as raras (`vac_promocao`, `vac_readaptacao` = <0,2%) são informações de fluxo legítimas.
- **Cargo em extinção (1 col):** dimensão de filtro relevante para análises de modernização.

**Justificativa para preservar todos os registros:**

A base tem 12.769 linhas e não há linhas claramente "lixo". Outliers foram preservados (com flag) porque representam cargos institucionais reais. Linhas com nulos foram tratadas via preenchimento, não removidas.

Esta decisão alinha-se à orientação do enunciado de que "outlier não é automaticamente erro" — em uma base governamental oficial, a hipótese padrão é que cada registro reflete uma realidade jurídica.

---

## 10. Limpeza e pré-processamento

Conduzido no Notebook 02 (`02_limpeza_e_transformacao.ipynb`). As ações realizadas:

**a) Padronização dos nomes de colunas.** Todos os nomes foram convertidos para `snake_case` minúsculo (P05). Exemplos:

- `ANO_MES` → `ano_mes`
- `VACANCIA_POR_APOSENTADORIA` → `vac_aposentadoria`
- `CARGO_EM_EXTINCAO` → `em_extincao`

**b) Conversão de tipos de dados.**

- `ano_mes` (int 202603) → datetime (2026-03-01).
- `cod_orgao` (int) → string com `zfill(5)` para preservar zeros à esquerda — necessário para futuras integrações com outras bases federais.
- `cod_cargo` (int) → string com `zfill(6)`, pelo mesmo motivo.
- Colunas categóricas (`nivel`, `plano_carreira`, `em_extincao`) → tipo `category` do pandas, ganho de memória e semântica.

**c) Remoção de espaços extras.** Foi feita verificação em todos os campos de texto. Nenhuma ocorrência foi encontrada (a base original já vem limpa nesse aspecto).

**d) Validação de duplicatas.** A chave funcional `(cod_orgao, cod_cargo)` foi verificada — nenhuma duplicata. Cada combinação aparece exatamente uma vez no snapshot.

O resultado dessa etapa foi salvo como `dataset_pos_limpeza.csv` (21 colunas, contando a flag `is_outlier` que entra no passo seguinte).

---

## 11. Tratamento de valores faltantes

A base bruta apresentava **1.618 valores nulos no total**, distribuídos em apenas duas colunas:

| Coluna | Nulos | Proporção | Decisão |
|---|---|---|---|
| `NIVEL` | 1.255 | 9,8% | Preencher com `"NAO_INFORMADO"` |
| `PLANO_CARREIRA` | 363 | 2,8% | Preencher com `"NAO_INFORMADO"` |

**Justificativa da decisão:**

A opção de **remover** linhas com nulos foi descartada — perderíamos 9,8% da base, e a ausência de `NIVEL` em alguns cargos antigos é uma característica legítima dos dados (carreiras descontinuadas ou em situação administrativa especial).

A opção de **imputar com a moda** também foi descartada — atribuiria "NS" (a moda) a cargos que podem ser de qualquer nível, distorcendo as análises.

A opção escolhida (categoria explícita `"NAO_INFORMADO"`) preserva a integridade analítica: as 1.255 linhas continuam disponíveis para análise, e qualquer relatório que agregue por nível pode tratar essa categoria como agrupamento próprio ou filtrar conforme necessário.

**Após o tratamento:** zero nulos no `dataset_pos_limpeza.csv`. Os nulos que aparecem no dataset final estão **apenas em features derivadas** criadas posteriormente (taxa_vacancia_mensal, pct_aposentadoria), onde o NaN reflete divisão indefinida — tratamento justificado na seção 17 deste relatório.

---

## 12. Tratamento de outliers

A análise de outliers em `qtd_aprovada` pelo método **IQR (intervalo interquartil)** identificou **1.879 cargos atípicos** — todos com valores acima de Q3 + 1.5×IQR.

Investigando esses 1.879 cargos, verificou-se que são **outliers legítimos, não erros**. Eles correspondem aos cargos institucionais de grande escala: Técnico Administrativo em Educação (34.209 vagas aprovadas), cargos do INSS, da Polícia Federal, da Receita Federal, das forças armadas civis. São justamente os cargos **mais importantes** para a análise.

**Decisão técnica:** criar uma flag binária `is_outlier` (0 ou 1), marcando os 1.879 registros — **mas sem removê-los**. Essa decisão alinha-se com a orientação explícita do enunciado: "outlier não é automaticamente erro. Às vezes ele é justamente o dado mais importante da análise".

**Vantagens da abordagem com flag:**

- Permite análises segmentadas: "ranking dos órgãos excluindo os outliers" vs. "ranking incluindo".
- Não perde 14,7% da base.
- Documenta a decisão de forma transparente — qualquer analista pode reproduzir a divisão.
- Reflete corretamente a realidade: o Executivo Federal **é** institucionalmente desigual; achatar essa desigualdade falsifica a fotografia.

---

## 13. Transformações realizadas

As transformações foram aplicadas progressivamente ao longo dos notebooks 02 e 03. Lista consolidada:

| Transformação | Coluna afetada | Notebook | Justificativa |
|---|---|---|---|
| `int → datetime` | `ano_mes` | 02 | Permite operações temporais e compatibilidade com séries históricas |
| `int → str + zfill(5)` | `cod_orgao` | 02 | Preserva zeros à esquerda, evita perda de chave |
| `int → str + zfill(6)` | `cod_cargo` | 02 | Idem |
| `object → category` | `nivel`, `plano_carreira`, `em_extincao` | 02 | Otimização de memória; semântica correta |
| `UPPERCASE → snake_case` | todas as 20 cols | 02 | Padronização |
| NaN → "NAO_INFORMADO" | `nivel`, `plano_carreira` | 02 | Preservar informação |
| `dt.year`, `dt.month`, `dt.quarter` | criadas a partir de `ano_mes` | 03 | Compatibilidade com análise temporal futura |

Todas as transformações foram aplicadas **sem perda de informação** — qualquer registro do dataset final pode ser rastreado de volta à base bruta.

---

## 14. Agregações realizadas

A etapa 6.11 exige pelo menos uma agregação. Foram realizadas **três agregações complementares**, cada uma respondendo a uma pergunta analítica diferente. Todas estão salvas em `dados_tratados/agregacoes/`.

### 14.1 Agregação por órgão (`agg_por_orgao.csv`)

Responde às perguntas P1 (órgãos com mais vagas em aberto) e P5 (concentração de cargos em extinção).

**Top 10 órgãos por tamanho institucional (vagas aprovadas):**

| Órgão | Cargos distintos | Aprovada | Ocupada | Vaga | Vacâncias | Taxa Ocup. |
|---|---|---|---|---|---|---|
| MS (Ministério da Saúde) | 258 | 65.209 | 31.374 | 33.835 | 80.922 | 48,1% |
| MF (Min. da Fazenda) | 116 | 47.867 | 19.769 | 28.098 | 22.348 | 41,3% |
| INSS | 96 | 43.022 | 18.490 | 24.532 | 29.582 | 43,0% |
| MEC | 212 | 29.497 | 1.385 | 28.112 | 15.871 | 4,7% |
| DPF (Polícia Federal) | 69 | 17.432 | 14.155 | 3.277 | 3.616 | 81,2% |
| MGI | 190 | 16.241 | 8.630 | 7.611 | 1.953 | 53,1% |
| DPRF | 34 | 13.812 | 13.188 | 624 | 734 | 95,5% |
| UFRJ | 192 | 13.037 | 12.119 | 918 | — | 93,0% |

**Leitura:** os ministérios fiscalizadores enxutos (DPRF, DPF) operam próximos do teto legal (>80% de ocupação). Os grandes prestadores de serviço (MS, INSS) sofrem déficit estrutural (~40-50%). O MEC aparece com taxa absurdamente baixa (4,7%) — efeito da reforma administrativa que transferiu cargos para autarquias vinculadas (universidades federais) sem atualizar o teto consolidado.

### 14.2 Agregação por nível de escolaridade (`agg_por_nivel.csv`)

Responde à pergunta P6.

| Nível | Cargos | Aprovada total | Ocupada total | Taxa Ocup. agregada |
|---|---|---|---|---|
| NS (Superior) | 5.792 | 438.218 | 300.629 | 68,6% |
| NI (Intermediário) | 5.712 | 247.780 | 154.491 | 62,4% |
| NM (Médio) | 10 | 839 | 296 | 35,3% |
| NAO_INFORMADO | 1.255 | 13.576 | 12.848 | 94,6% |

**Leitura:** cargos de Nível Superior têm taxa de ocupação ligeiramente superior aos de Nível Intermediário (68,6% vs 62,4%). Cargos com nível "NAO_INFORMADO" estão quase totalmente ocupados (94,6%) — sugere que são cargos antigos com seus últimos ocupantes, já fechados para novos concursos.

### 14.3 Agregação por tipo de vacância (`agg_por_tipo_vacancia.csv`)

Responde à pergunta P4 e ao achado central da AED.

| Tipo | Total (03/2026) | % do total |
|---|---|---|
| Aposentadoria | 214.829 | 76,7% |
| Posse em cargo inacumulável | 22.983 | 8,2% |
| Exoneração | 20.677 | 7,4% |
| Falecimento | 16.943 | 6,0% |
| Demissão | 4.084 | 1,5% |
| Promoção | 530 | 0,2% |
| Readaptação | 79 | 0,03% |

**Implicação para política pública:** o planejamento de concursos deveria ser pautado por **projeções demográficas** (idade dos servidores ativos), não por modelos de turnover convencionais — a vacância no Executivo Federal é majoritariamente uma transição etária, não decisão voluntária.

---

## 15. Normalização e padronização

A etapa 6.12 foi tratada no Notebook 03, seção 3.

### 15.1 Comparação das três técnicas

| Técnica | Faixa de saída | Sensibilidade a outliers |
|---|---|---|
| Min-Max Scaling | [0, 1] | Alta — outliers achatam o resto |
| StandardScaler (Z-score) | aprox. [-3, 3] | Média |
| **RobustScaler** | sem limite fixo | **Baixa** — mediana e IQR resistem |

### 15.2 Justificativa da escolha

A base tem **outliers reais e legítimos** (1.879 cargos sinalizados pela flag `is_outlier`). Aplicar MinMax produziria distribuição praticamente colada em zero — 75% dos cargos ficariam comprimidos abaixo de 0,0005, perdendo capacidade de discriminação para a maioria absoluta da base. Aplicar StandardScaler tampouco é adequado: a média é fortemente puxada pelos outliers, e o percentil 99 acaba em +8.7 desvios padrão (um valor que algoritmos baseados em normalidade interpretariam como anomalia, quando é realidade institucional).

**RobustScaler** foi a escolha técnica: usa mediana e IQR, robusto a outliers, mantém a informação dos cargos institucionais enquanto preserva poder de discriminação no miolo da distribuição.

### 15.3 Variáveis normalizadas

Cinco colunas numéricas-chave receberam versões normalizadas:

- `qtd_aprovada_robust`
- `qtd_ocupada_robust`
- `qtd_vaga_robust`
- `total_vacancias_robust`
- `deficit_nominal_robust`

A mediana dessas colunas é exatamente 0 (por construção do método). Os valores positivos representam cargos acima da mediana; negativos, abaixo. A escala fica comparável entre variáveis — um cargo "10× acima da mediana de aprovada" é diretamente comparável a "10× acima da mediana de ocupada".

Essa propriedade torna o RobustScaler ideal como **insumo para algoritmos de DM sensíveis a escala** (K-Means, KNN, PCA, redes neurais).

---

## 16. Discretização

A etapa 6.13 foi tratada no Notebook 03, seção 4. Duas variáveis foram discretizadas, ambas com cortes de negócio (não com quartis estatísticos), porque cortes semanticamente definidos produzem categorias **interpretáveis e estáveis** ao longo do tempo.

### 16.1 `porte_cargo` — discretização de `qtd_aprovada`

| Faixa | Cortes | Cargos | % |
|---|---|---|---|
| Micro | 1-2 | 5.558 | 43,5% |
| Pequeno | 3-10 | 3.715 | 29,1% |
| Médio | 11-50 | 2.266 | 17,7% |
| Grande | 51-500 | 966 | 7,6% |
| Mega | >500 | 264 | 2,1% |

**Leitura:** quase metade dos cargos é "Micro" (1-2 vagas) — tipicamente chefias, comissionados ou cargos em extinção com poucos ocupantes. Apenas 2,1% são "Mega", mas concentram a maior parte dos servidores ativos do Executivo Federal.

Utilidade analítica: relatórios executivos podem reportar "X% do quadro federal está concentrado em cargos de porte Mega", linguagem mais clara que valores numéricos. Mining de regras pode associar `porte_cargo` com `nivel`, `em_extincao`, etc.

### 16.2 `faixa_taxa_ocupacao` — discretização de `taxa_ocupacao`

| Faixa | Cortes | Cargos | % |
|---|---|---|---|
| Crítica | <40% | 1.539 | 12,1% |
| Baixa | 40-70% | 610 | 4,8% |
| Adequada | 70-90% | 870 | 6,8% |
| Completa | 90-100% | 9.750 | 76,4% |
| Excedente | >100% | 0 | 0% |

**Achado importante — paradoxo de Simpson observado:**

Aqui ocorre uma aparente contradição: 76,4% dos **cargos individuais** estão "Completos" (≥90% de ocupação), mas a taxa de ocupação **agregada** do governo (calculada como soma de ocupada ÷ soma de aprovada) fica em ~67%. Como?

A explicação é o **paradoxo de Simpson**: a maioria dos cargos individuais é Micro/Pequeno, e nesses casos `qtd_ocupada == qtd_aprovada` é trivial (ex.: 1 ocupado / 1 aprovado = 100%). Os cargos Mega (2% da base) concentram a maior parte do quadro e operam tipicamente com 50-70% de ocupação — arrastando a métrica agregada para baixo.

**Implicação:** o indicador correto para reportar saúde do Executivo Federal é a `taxa_ocupacao_agregada` (~67%), não a média das taxas individuais (que seria ~95%). Este achado é relevante para qualquer dashboard de BI sobre a base — escolha errada da métrica falsifica a história.

Nenhum cargo na faixa "Excedente" foi observado neste snapshot, indicando que a regra `OCUPADA ≤ APROVADA` é respeitada em 100% dos casos. A inconsistência reportada como problema P08 (relacionada a `DISTRIBUIDA`, não a `APROVADA`) é capturada por outra feature (`diferenca_distribuicao`).

---

## 17. Feature Engineering

A etapa 6.14 foi tratada no Notebook 03, seção 1. Foram criadas **nove novas variáveis** derivadas, cada uma com utilidade analítica ligada a pelo menos uma das 11 perguntas norteadoras.

| Feature | Fórmula | Tipo | Pergunta(s) que responde |
|---|---|---|---|
| `total_vacancias` | soma das 7 `vac_*` | inteiro | P4 (peso das causas) |
| `pct_aposentadoria` | `vac_aposentadoria / total_vacancias` | float [0,1] | P9 (envelhecimento) |
| `taxa_ocupacao` | `qtd_ocupada / qtd_aprovada` | float | P2, P6 (eficiência) |
| `taxa_vacancia_mensal` | `total_vacancias / qtd_ocupada` | float | P7 (rotatividade) |
| `deficit_nominal` | `qtd_aprovada - qtd_ocupada` | inteiro | P1, P5 (déficit absoluto) |
| `diferenca_distribuicao` | `(ocupada + vaga) - distribuida` | inteiro | captura problema P08 |
| `ano` | extraído de `ano_mes` | inteiro | compatibilidade temporal |
| `mes` | extraído de `ano_mes` | inteiro | sazonalidade futura |
| `trimestre` | extraído de `ano_mes` | inteiro | agregação trimestral |

### Tratamento de divisão por zero

Três features envolvem divisão e podem produzir NaN. A estratégia adotada para cada uma é distinta, porque o significado da divisão por zero é diferente em cada caso:

| Feature | Quando o denominador é zero significa... | Tratamento |
|---|---|---|
| `pct_aposentadoria` | Nenhuma vacância no mês — não há "porcentagem" a calcular | NaN (preserva semântica de ausência) |
| `taxa_ocupacao` | Cargo sem nenhuma vaga aprovada — situação anômala | NaN (caso a investigar) |
| `taxa_vacancia_mensal` | Cargo sem ocupantes — não há "rotatividade" | NaN |

Substituir esses NaN por zero seria **semanticamente incorreto**: não é o mesmo que "0% de aposentadoria" — é "indefinido". Em ferramentas de BI, basta filtrar essas linhas no widget específico que usa a métrica.

---

## 18. Descrição do dataset final

O dataset final entregue (`dataset_final_tratado.csv` e `.xlsx`) tem **12.769 registros e 37 colunas**, organizadas em **nove blocos semânticos** para facilitar leitura humana e consumo por ferramentas de BI.

| Bloco | Função | Colunas | # |
|---|---|---|---|
| **A. Temporal** | Quando | ano_mes, ano, mes, trimestre | 4 |
| **B. Identificação do órgão** | Onde | cod_orgao, sigla_orgao, nome_orgao | 3 |
| **C. Identificação do cargo** | O quê | cod_cargo, nome_cargo, plano_carreira, nivel, em_extincao | 5 |
| **D. Quantitativos brutos** | Stock | qtd_aprovada, qtd_distribuida, qtd_ocupada, qtd_vaga | 4 |
| **E. Vacâncias por tipo** | Fluxo | 7 colunas vac_* (ordem: aposentadoria, posse_inac, exoneração, falecimento, demissão, promoção, readaptação) | 7 |
| **F. Features derivadas (quant.)** | KPIs | total_vacancias, deficit_nominal, taxa_ocupacao, taxa_vacancia_mensal, pct_aposentadoria, diferenca_distribuicao | 6 |
| **G. Features derivadas (cat.)** | Faixas | porte_cargo, faixa_taxa_ocupacao | 2 |
| **H. Versões normalizadas** | Para ML | 5 colunas *_robust | 5 |
| **I. Flags** | Metadados | is_outlier | 1 |
| **TOTAL** | | | **37** |

### Características de qualidade do dataset final

- **12.769 registros** preservados desde a base bruta — **zero perda** de linhas ao longo do tratamento.
- **0 nulos não justificados** — apenas em 2 features derivadas (`pct_aposentadoria`, `taxa_vacancia_mensal`), onde o NaN é semanticamente correto.
- **0 duplicatas** pela chave funcional `(cod_orgao, cod_cargo)`.
- **Tipos de dados corretos** em todas as colunas (datetime, string, category, int64, float64).
- **Padronização total** — todas as colunas em `snake_case`.
- **Reprodutível** — qualquer execução do pipeline (notebooks 02 → 03 → 04) regenera exatamente este dataset.

### Crescimento da base ao longo do tratamento

| Estágio | Linhas | Colunas | Memória | Nulos |
|---|---|---|---|---|
| Base bruta (`.ods`) | 12.769 | 20 | ~3 MB | 1.618 |
| Pós-limpeza (Notebook 02) | 12.769 | 21 | ~3 MB | 0 |
| Com features (Notebook 03) | 12.769 | 37 | ~6 MB | NaN justificado |
| Dataset final (Notebook 04) | 12.769 | 37 | ~6 MB | NaN justificado |

A base não perdeu nenhum registro ao longo do tratamento — todas as decisões privilegiaram **preservação de informação** sobre simplificação.

---

## 19. Catálogo de dados

O catálogo (`documentacao/catalogo_dados.xlsx`) documenta os 8 atributos exigidos pelo enunciado para cada uma das 37 colunas do dataset final, totalizando **37 entradas × 8 atributos**. Foi construído no Notebook 04, seção 4.

### Atributos documentados (8 por coluna)

1. **`nome_coluna`** — identificador da coluna no dataset
2. **`descricao`** — significado em linguagem natural
3. **`tipo_dado`** — datetime64, int64, float64, category, string
4. **`exemplo`** — valor real extraído dinamicamente do dataset
5. **`origem`** — referência ao campo da base SEGES ou à fórmula de derivação
6. **`tratamento_aplicado`** — operação aplicada (conversão de tipo, preenchimento, fórmula)
7. **`origem_tipo`** — Original / Original (transformada) / Original (tratada) / Criada
8. **`uso_esperado`** — finalidade analítica (chave, dimensão, medida, KPI, insumo de ML)

### Distribuição da origem das colunas

| Origem | Quantidade | % |
|---|---|---|
| Criada | 17 | 45,9% |
| Original | 14 | 37,8% |
| Original (transformada) | 4 | 10,8% |
| Original (tratada) | 2 | 5,4% |
| **Total** | **37** | **100%** |

### Estrutura do arquivo XLSX

O catálogo é um arquivo Excel com **duas planilhas**:

**Planilha `Catalogo`:** 37 linhas × 8 atributos, com cabeçalho destacado (azul-escuro com texto branco em negrito), zebra rows para legibilidade, bordas finas, larguras de coluna calibradas (descrição: 60 caracteres, uso esperado: 55, etc.), fonte Arial 10/11, e *freeze panes* na linha 1.

**Planilha `Metadados`:** 15 atributos sobre o projeto — versão, fonte primária, órgão responsável, arquivo original, totais (registros, colunas originais, colunas criadas), dicionário oficial, licença CC BY 4.0, data de geração.

### Como o catálogo se conecta com o dataset

A construção do catálogo inclui uma **validação cruzada automatizada** com `assert`: o conjunto de nomes do catálogo precisa coincidir exatamente com o conjunto de colunas do dataset — sem coluna faltando, sem coluna sobrando, sem duplicatas. Essa validação impede que o catálogo divirja do dataset em futuras iterações. Os exemplos de valor são coletados **dinamicamente** do dataset, não hardcoded, garantindo que sempre reflitam o conteúdo real.

---

## 20. Organização DataOps

A etapa 6.17 trata da organização do projeto, exigindo que outra pessoa consiga entender e reproduzir o trabalho. Estrutura adotada:

```
PM3_CargosVagosVacancias/
│
├── dados_brutos/                          (original preservado)
│   ├── CargosVagosVacancias_202603.ods
│   └── CargosVagosVacancias_202603.csv
│
├── dados_tratados/
│   ├── dataset_pos_limpeza.csv            (checkpoint NB 02)
│   ├── dataset_com_features.csv           (checkpoint NB 03)
│   ├── dataset_final_tratado.csv          (ENTREGÁVEL final)
│   ├── dataset_final_tratado.xlsx         (ENTREGÁVEL final)
│   └── agregacoes/                        (3 tabelas agregadas)
│       ├── agg_por_orgao.csv
│       ├── agg_por_nivel.csv
│       └── agg_por_tipo_vacancia.csv
│
├── notebooks/
│   ├── 00_planejamento_e_contexto.ipynb   (etapas 6.1, 6.2)
│   ├── 01_diagnostico_qualidade.ipynb     (etapas 6.3, 6.4)
│   ├── 02_limpeza_e_transformacao.ipynb   (etapas 6.6-6.10)
│   ├── 02b_analise_exploratoria.ipynb     (etapa 6.5)
│   ├── 03_feature_engineering.ipynb       (etapas 6.11-6.14)
│   └── 04_dataset_final.ipynb             (etapas 6.15, 6.16)
│
├── documentacao/
│   ├── problemas_qualidade.xlsx           (NB 01)
│   ├── catalogo_dados.xlsx                (NB 04)
│   └── relatorio_final.docx               (este documento)
│
├── evidencias_aed/
│   └── 7 gráficos PNG                     (NB 02b)
│
├── orange/
│   └── GUIA_ORANGE.md                     (opcional)
│
└── README.md                              (instruções de execução)
```

### Princípios DataOps aplicados

**Imutabilidade da base original.** O arquivo `.ods` em `dados_brutos/` nunca é modificado. Cada execução do pipeline lê dele e produz arquivos novos.

**Checkpoints intermediários.** O dataset é salvo após cada etapa importante (pós-limpeza, com features, final). Isso permite que o pipeline seja executado parcialmente — útil para debug e iteração.

**Versionamento implícito.** Como cada notebook produz um arquivo específico, é trivial comparar versões: `diff dataset_pos_limpeza.csv dataset_final_tratado.csv` mostra exatamente o que mudou.

**Reprodutibilidade total.** Os notebooks usam **caminhos relativos** (`../dados_brutos/`) e dependências mínimas (pandas, numpy, matplotlib, seaborn, openpyxl, scikit-learn). Qualquer professor ou colega pode clonar a pasta, instalar as dependências e regenerar exatamente o mesmo dataset final.

**Documentação ancorada no código.** Cada notebook tem markdown explicativo abundante, e os comentários no código justificam decisões técnicas. O catálogo de dados serve como documento de referência principal.

**Asserções de qualidade.** O Notebook 04 inclui 6 verificações automatizadas com `assert`: se algum critério falhar em uma futura execução, o pipeline para em vez de produzir um dataset corrompido silenciosamente.

---

## 21. Conclusão

O projeto cumpriu o objetivo central do PM3: demonstrar domínio sobre o processo completo de preparação de dados, partindo de uma base governamental real e entregando um dataset final, limpo, enriquecido e documentado, pronto para uso em BI e Data Mining.

O ponto de partida foi uma base de 12.769 registros e 20 colunas, com 1.618 valores nulos, inconsistências aritméticas em 14% das linhas, outliers extremos legítimos e categorias sem padronização. O ponto de chegada é um dataset de 12.769 registros (zero perda) e 37 colunas — sendo 14 originais, 6 originais transformadas/tratadas e 17 criadas via feature engineering, normalização e discretização. Toda decisão técnica está justificada nos notebooks, replicada neste relatório, e documentada no catálogo de dados.

Três achados analíticos emergiram durante o tratamento, e ilustram o tipo de insight que justifica todo o processo:

1. **Aposentadoria representa 76,7% das vacâncias.** Não é rotatividade voluntária — é transição etária. Política pública de reposição precisa ser pautada por projeções demográficas, não por turnover convencional.

2. **Cargos institucionais "outliers" são justamente os mais importantes.** A decisão metodológica de preservá-los com flag, em vez de removê-los, foi crítica. Removê-los empobreceria a análise da realidade do Executivo Federal.

3. **Há paradoxo de Simpson na taxa de ocupação.** 76% dos cargos individuais estão "completos" (>90%), mas a taxa agregada do governo é de apenas 67%. A escolha errada da métrica em um dashboard falsifica a história — escolha que só fica visível com tratamento cuidadoso dos dados.

Esses achados validam a premissa do enunciado: dados ruins produzem decisões ruins. Tratamento cuidadoso não é etapa burocrática — é a etapa que define se a análise downstream vai ser correta ou simplesmente colorida.

---

## 22. Limitações

O projeto, apesar de cobrir integralmente as 17 etapas do enunciado, tem limitações que devem ser explicitadas:

**Recorte temporal.** A análise utiliza um único snapshot (março/2026). Conclusões sobre tendências, sazonalidade, evolução do quadro federal ou velocidade de aposentadorias **não podem** ser extraídas desta versão. As colunas `ano`, `mes` e `trimestre` foram criadas como preparação para análises temporais futuras, mas o dataset atual contém apenas uma competência.

**Ausência de dados de servidores individuais.** A base agrega ao nível `(órgão × cargo)`. Não temos informação sobre idade, gênero, tempo de serviço, lotação física ou remuneração de cada servidor. Análises demográficas precisas exigem cruzamento com o SIAPE (Sistema Integrado de Administração de Pessoal), o que está fora do escopo deste projeto.

**Cobertura: apenas Executivo Federal Civil.** Não estão incluídos servidores militares, do Poder Legislativo, do Poder Judiciário, do Ministério Público nem das três esferas estaduais e municipais. Para análise consolidada do setor público brasileiro, seria preciso integrar bases adicionais (RAIS-Setor Público, dados dos tribunais de contas, etc.).

**Outliers preservados sem segmentação ainda aplicada.** A flag `is_outlier` foi criada, mas o dataset final inclui todos os registros juntos. Análises posteriores podem precisar segmentar em "cargos típicos" (`is_outlier=0`) e "institucionais" (`is_outlier=1`) — preparativo feito, decisão postergada.

**Métricas derivadas com NaN nas pontas.** Cerca de 58% dos registros têm `pct_aposentadoria=NaN` (cargos sem vacância no mês) e ~9% têm `taxa_vacancia_mensal=NaN` (cargos sem ocupantes). Esses NaN são justificados, mas exigem atenção em qualquer agregação posterior — média simples dessas colunas pode estar enviesada.

**Sem validação cruzada com outras fontes.** Os totais reportados pela SEGES não foram conferidos contra publicações alternativas (relatórios do TCU, dados da CGU, transparência do MGI). Em produção, seria recomendável esse cross-check.

**Sem perspectiva qualitativa.** O projeto é puramente quantitativo. Não há análise de motivos políticos, jurídicos ou administrativos por trás dos déficits — apenas a mensuração deles.

---

## 23. Próximos passos

Caminhos naturais de evolução do projeto:

**a) Incorporar série histórica.** A SEGES publica esta base mensalmente há mais de uma década. Concatenar 12+ meses transformaria o problema de análise de snapshot em análise temporal, viabilizando: tendência da taxa de ocupação ao longo do tempo, identificação de "ondas" de aposentadoria, detecção de impactos de eventos administrativos (reformas, novas carreiras, criação/extinção de órgãos). O pipeline atual já está preparado — basta loopar a leitura por competência.

**b) Construir um dashboard interativo.** O dataset final está pronto para consumo direto em Power BI, Looker Studio, Metabase ou Tableau. Sugestões de visões iniciais: painel executivo do MGI (KPIs federais), drill-down por ministério, dashboard de "carreiras em alerta" (taxa de vacância > X%), mapa de concentração de aposentadorias previstas.

**c) Aplicar clustering aos órgãos.** Usar as features `*_robust` em K-Means ou DBSCAN para identificar 3-5 perfis típicos de órgão. As features adequadas para isso já foram criadas no Notebook 03. Resultado esperado: clusters interpretáveis como "fiscalizadores enxutos", "prestadores de grande escala em déficit", "órgãos universitários", etc.

**d) Implementar detecção de anomalias mais sofisticada.** A flag `is_outlier` atual é baseada em IQR simples. Algoritmos como Isolation Forest ou Local Outlier Factor, aplicados sobre múltiplas dimensões simultaneamente, podem identificar combinações anômalas (ex.: órgão pequeno com vacância de aposentadoria desproporcionalmente alta).

**e) Construir modelo preditivo de aposentadorias.** Combinando esta base com SIAPE (idade dos servidores), seria possível treinar um modelo que projeta, para cada cargo, quantas vacâncias por aposentadoria são esperadas nos próximos 12 meses. Isso converteria o trabalho atual de descrição em planejamento prescritivo de concursos.

**f) Cruzar com dados de concursos públicos abertos.** Integrar com bases de editais publicados (Diário Oficial, sites de organizadoras) para gerar indicador de "tempo de resposta": quanto tempo passa entre uma vacância e a abertura de concurso para reposição.

**g) Versionar o pipeline com Git e DVC.** Em produção, recomenda-se versionamento explícito tanto do código (Git) quanto dos dados (Data Version Control), permitindo reproduzir exatamente o dataset gerado em qualquer competência passada.

**h) Automação do refresh mensal.** Quando a próxima competência for publicada, o pipeline atual pode ser executado novamente sem alterações de código. Próximo passo natural é agendar via cron, GitHub Actions ou Airflow para que o dataset final esteja sempre atualizado.

---

## Referências bibliográficas

BRASIL. **Lei nº 8.112, de 11 de dezembro de 1990.** Dispõe sobre o Regime Jurídico dos Servidores Públicos Civis da União, das autarquias e das fundações públicas federais. Especificamente o art. 33 (vacância). Disponível em: http://www.planalto.gov.br/ccivil_03/leis/L8112cons.htm. Acesso em: 2026.

BRASIL. **Secretaria de Gestão e Inovação (SEGES) / Ministério da Gestão e da Inovação em Serviços Públicos (MGI).** Conjunto de dados "Cargos Vagos e Vacâncias do Poder Executivo Federal Civil". Disponível em: https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---cargos-vagos-e-vacancias. Acesso em: 2026.

BRASIL. **SEGES/MGI.** Dicionário oficial dos campos da base — `Dicionario_CargosVagosVacancias.pdf`. Disponível no repositório oficial: https://repositorio.dados.gov.br/segrt/cargos%20vagos%20e%20vacancia/2026/Dicionario_CargosVagosVacancias.pdf. Acesso em: 2026.

CASTRO, L. N.; FERRARI, D. G. **Introdução à mineração de dados: conceitos básicos, algoritmos e aplicações.** São Paulo: Saraiva, 2016.

CERCHIARI DE ANDRADE, A. L. **Preparação e análise exploratória de dados.** SAGAH.

GOLDSCHMIDT, R.; BEZERRA, E.; PASSOS, E. **Data mining: conceitos, técnicas, algoritmos, orientações e aplicações.** Rio de Janeiro: Elsevier, 2015.

McKINNEY, W. **Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter.** 3rd ed. O'Reilly Media, 2022.

PEDREGOSA, F. et al. **Scikit-learn: Machine Learning in Python.** Journal of Machine Learning Research, v. 12, p. 2825-2830, 2011. (Referência para os scalers utilizados na seção 15.)

---

**Fim do relatório.**
