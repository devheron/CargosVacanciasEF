# Respostas ao Enunciado do PM3

**Projeto:** Tratamento de Dados — Cargos Vagos e Vacâncias do Executivo Federal Civil (03/2026)  
**Aluno(a):** _______________________

Este documento responde, de forma objetiva, a cada pergunta e exigência do enunciado da disciplina. Para detalhamento técnico aprofundado, consultar o `relatorio_final.docx`.

---

## Validação dos critérios mínimos da base (item 5)

| Critério exigido | Atendimento na base escolhida | Status |
|---|---|---|
| Pelo menos 300 registros | 12.769 linhas | ✓ Supera amplamente |
| Pelo menos 6 colunas úteis | 20 colunas originais (e 37 no dataset final) | ✓ Supera amplamente |
| Pelo menos uma variável numérica | 11 colunas numéricas (qtd_*, vac_*) | ✓ |
| Pelo menos uma variável categórica | 5 colunas categóricas (nivel, plano_carreira, em_extincao, etc.) | ✓ |
| Possibilidade de limpeza, transformação e AED | 1.618 nulos, inconsistências aritméticas, alta assimetria | ✓ Rico em problemas |
| Possibilidade de criar novas variáveis | 17 features criadas (taxa_ocupacao, deficit, etc.) | ✓ |
| Presença de problemas de qualidade | 10 problemas catalogados em `problemas_qualidade.xlsx` | ✓ |

---

## Respostas ao item 6.1 — Planejamento

### 1. Qual é o tema da base?

**Gestão quantitativa de pessoas no Poder Executivo Federal Civil brasileiro.** A base apresenta, mês a mês, a fotografia do quadro de servidores em cada órgão da administração federal direta, autárquica e fundacional — quantos cargos foram aprovados em lei, distribuídos, ocupados, vagos, e o fluxo mensal de servidores que saíram por sete causas distintas (aposentadoria, exoneração, demissão, promoção, readaptação, posse em outro cargo inacumulável, falecimento).

### 2. De onde os dados foram retirados?

Portal Brasileiro de Dados Abertos (`dados.gov.br`), conjunto de dados publicado pela **Secretaria de Gestão e Inovação (SEGES)** do Ministério da Gestão e da Inovação em Serviços Públicos (MGI). Arquivo `CargosVagosVacancias_202603.ods`, aba `por_Órgao_e_Cargo`. Licença CC BY 4.0. Acesso em 2026.

### 3. Qual problema ou situação essa base ajuda a compreender?

Cinco fenômenos centrais da política de pessoal federal:

- **Déficit estrutural de servidores** em órgãos críticos (INSS, MS, Receita).
- **Pressão de reposição por aposentadoria** — descobrimos que 76,7% das vacâncias são por aposentadoria.
- **Cargos formalmente em extinção** que ainda têm ocupantes (28% da base).
- **Concentração desigual** — alguns poucos cargos concentram milhares de servidores.
- **Reorganização ministerial** ao longo do tempo (criação/extinção de órgãos).

### 4. Quem poderia usar esses dados para tomar decisão?

| Ator | Decisão concreta |
|---|---|
| MGI / SEGES | Calendário de concursos públicos federais |
| Ministério do Planejamento | Previsão da folha de pagamento; impacto orçamentário |
| TCU (controle externo) | Fiscalização do cumprimento dos tetos legais |
| CGU (controle interno) | Auditorias sobre cessões e movimentações de pessoal |
| Comissões do Congresso | Pareceres sobre reestruturação de carreiras |
| Dirigentes dos órgãos | Solicitação de novos concursos; sucessão |
| Sindicatos de servidores | Acompanhamento da categoria |
| Pesquisadores e jornalistas | Estudos sobre o Estado brasileiro |

### 5. Como essa base poderia ser utilizada em Business Intelligence?

- **Dashboard executivo no Power BI/Looker:** taxa de ocupação federal, ranking de órgãos deficitários, evolução das vacâncias.
- **KPIs derivados:** taxa de ocupação, déficit nominal, taxa de vacância mensal — todos já implementados como features no Notebook 03.
- **Drill-down hierárquico:** Executivo Federal → Ministério → Órgão → Plano → Cargo.
- **Painéis por ministério ou por carreira** — cada gestor vê o que lhe interessa.

### 6. Como essa base poderia ser utilizada em Data Mining?

- **Clustering de órgãos** em perfis típicos (K-Means usando as features `*_robust`).
- **Detecção de anomalias** (Isolation Forest sobre múltiplas dimensões; já implementamos versão básica com flag `is_outlier`).
- **Regras de associação** (Apriori): quais cargos coexistem nos mesmos órgãos.
- **Classificação:** prever se um cargo tende a estar em extinção a partir do seu perfil.
- **Previsão:** com série histórica, projetar volume de aposentadorias por órgão.

### 7. Quais perguntas poderiam ser respondidas com esses dados?

**Descritivas (BI clássico):**
1. Quais órgãos têm mais vagas em aberto?
2. Qual a taxa de ocupação por nível de escolaridade?
3. Top 10 cargos por quantitativo total?
4. Peso de cada uma das 7 causas de vacância?
5. Quantos cargos em extinção ainda têm ocupantes?

**Comparativas:**
6. Cargos de NS têm ocupação maior ou menor que NI?
7. Órgãos pequenos vs grandes — comportamentos diferentes?
8. Exoneração se concentra em alguma carreira específica?

**Estruturais (DM):**
9. É possível agrupar os 211 órgãos em perfis típicos?
10. Quais cargos coexistem em quais órgãos?
11. Há outliers institucionais que merecem segmentação?

---

## Respostas ao item 6.2 — Relação com BI, Big Data e Data Mining

### 1. Como os dados poderiam apoiar decisões?

Diretamente: o MGI decide **onde abrir concursos** com base no déficit nominal por órgão; o TCU **fiscaliza** se órgãos respeitam o teto legal usando a taxa de ocupação; o Congresso **estima impacto fiscal** de leis de reestruturação de carreira usando os totais agregados. Cada um desses atores precisa de uma agregação diferente — todas suportadas pela granularidade da base.

### 2. Quais padrões poderiam ser descobertos?

- **Pirâmide etária por órgão**, via proxy `pct_aposentadoria`: órgãos onde quase 100% das vacâncias é por aposentadoria estão envelhecidos.
- **Tipologia de órgãos** via clustering: prestador de serviço × fiscalizador × regulador × universitário.
- **Cargos correlacionados** que aparecem juntos em vários órgãos (Apriori).
- **Anomalias administrativas:** órgãos com taxa de vacância desproporcional ao seu tamanho.

### 3. Que tipo de análise poderia ser feita?

Analítica descritiva (BI) e analítica de descoberta (DM). Como a base inclui dimensões temporais, espaciais (órgão) e tipológicas (carreira), suporta todos os tipos clássicos: relatório, dashboard, segmentação, associação, classificação e — com série histórica — previsão.

### 4. A base poderia ser usada em dashboards?

Sim, e com facilidade. O dataset final tem estrutura **dimensão × medida** clássica:

- **Dimensões:** órgão, cargo, nível, plano de carreira, em_extincao, porte_cargo, faixa_taxa_ocupacao (estas duas últimas criadas no projeto).
- **Medidas aditivas:** todas as `qtd_*` e `vac_*`, mais `total_vacancias` e `deficit_nominal`.
- **Medidas não-aditivas (taxas):** taxa_ocupacao, taxa_vacancia_mensal, pct_aposentadoria — usadas em widgets específicos com cuidado.

### 5. A base poderia ser usada para classificação, agrupamento, previsão ou descoberta de padrões?

**Sim para todos os quatro** — cada um com viabilidade diferente:

- **Agrupamento (cluster):** **alta viabilidade imediata**. Variáveis prontas (versões `*_robust` normalizadas no Notebook 03), 211 órgãos como unidades de análise.
- **Classificação:** **boa viabilidade.** Rótulo natural seria `em_extincao` — prever se um cargo de perfil X tende a estar em extinção.
- **Descoberta de padrões / regras de associação:** **boa viabilidade.** Cargos × órgãos é matriz natural para Apriori.
- **Previsão:** **viável com extensão** — exige concatenar série histórica mensal disponível na SEGES. Pipeline já preparado (colunas `ano`, `mes`, `trimestre` criadas).

---

## Checklist dos entregáveis obrigatórios (item 7)

| # | Entregável exigido | Localização no projeto |
|---|---|---|
| 1 | Base de dados original | `dados_brutos/CargosVagosVacancias_202603.ods` (preservada intacta) |
| 2 | Dataset final tratado | `dados_tratados/dataset_final_tratado.csv` e `.xlsx` |
| 3 | Notebook ou script Python | 6 notebooks em `notebooks/` (`00_*` a `04_*`) |
| 4 | Relatório final | `documentacao/relatorio_final.docx` (também em `.md`) |
| 5 | Catálogo de dados | `documentacao/catalogo_dados.xlsx` (2 planilhas) |
| 6 | Evidências da AED | 7 gráficos PNG em `evidencias_aed/` (gerados no Notebook 02b) |
| 7 | Tabela com problemas de qualidade | `documentacao/problemas_qualidade.xlsx` (10 problemas) |
| 8 | Descrição das etapas de limpeza | Notebook 02 + seção 10 do relatório final |
| 9 | Demonstração: tratamento de valores faltantes | Notebook 02, seção 5 + seção 11 do relatório |
| 10 | Demonstração: tratamento de outliers | Notebook 02, seção 6 + seção 12 do relatório |
| 11 | Demonstração: transformação dos dados | Notebooks 02 e 03 + seção 13 do relatório |
| 12 | Demonstração: agregação dos dados | Notebook 03 seção 2 + 3 arquivos CSV em `dados_tratados/agregacoes/` |
| 13 | Demonstração: normalização ou padronização | Notebook 03 seção 3 (RobustScaler) + seção 15 do relatório |
| 14 | Demonstração: discretização | Notebook 03 seção 4 + seção 16 do relatório |
| 15 | Demonstração: Feature Engineering | Notebook 03 seção 1 (9 features criadas) + seção 17 do relatório |
| 16 | Explicação sobre uso em BI e DM | Notebook 00 seções 2.1, 2.2, 2.3 + seção 6 do relatório |

**Todos os 16 entregáveis estão presentes no projeto.**

---

## Observações finais sobre conformidade

| Orientação do enunciado (item 9) | Como foi atendida |
|---|---|
| Base deve ser real | Sim — fonte oficial governamental (SEGES/MGI) com licença CC BY 4.0 |
| Fonte dos dados informada | Sim — em múltiplos lugares: Notebook 00, relatório, catálogo |
| Base original preservada | Sim — `.ods` em `dados_brutos/`, nunca modificado |
| Dataset final diferente da base original | Sim — 37 colunas vs 20; 17 colunas novas; tipos corretos |
| Decisões justificadas | Sim — cada decisão técnica tem markdown explicativo no notebook correspondente |
| Notebook organizado e executável | Sim — 6 notebooks com caminhos relativos, executados ponta-a-ponta sem erro |
| Explicação além do código | Sim — markdowns abundantes em todos os notebooks |
| Interpretação dos gráficos | Sim — cada um dos 7 PNGs tem leitura no Notebook 02b e no relatório seção 8 |
| Documentação completa | Sim — catálogo XLSX, relatório, README, este documento |

---

**Fim do documento.**
