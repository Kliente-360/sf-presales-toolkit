# Skill: Assessment

Gera um documento de assessment profissional a partir do output do discovery. Esse documento é entregue ao cliente ou usado internamente como base da proposta.

---

## Como usar

Forneça o arquivo de discovery como contexto e peça:

> "Use a skill de assessment com base no discovery abaixo e salve em outputs/<cliente>_<data>_assessment.md"

---

## Template de output

```markdown
# Assessment Salesforce — <Nome do Cliente>
**Versão:** 1.0
**Data:** <data>
**Preparado por:** <seu nome / empresa>
**Segmento:** <varejo | financeiro | saude | outro>
**Confidencial**

---

## 1. Sumário Executivo

Parágrafo de 5–8 linhas descrevendo:
- Quem é o cliente e o contexto do negócio
- Os principais desafios identificados
- A solução Salesforce recomendada em alto nível
- O valor esperado da transformação

> Escreva como se o CEO fosse ler primeiro. Sem jargão técnico. Foco em resultado de negócio.

---

## 2. Perfil do Cliente

| Campo | Detalhe |
|---|---|
| Empresa | <nome> |
| Segmento | <segmento> |
| Porte | <nº de funcionários / receita estimada> |
| Modelo de negócio | <B2B / B2C / B2B2C / outro> |
| Maturidade digital | <1–5 com descrição> |
| Principais concorrentes | <se mencionado> |
| Momento atual | <crescimento / reestruturação / crise / expansão> |

---

## 3. Diagnóstico de Maturidade Atual

Avalie o estado atual do cliente em cada dimensão abaixo. Use: Inicial (1) / Em desenvolvimento (2) / Definido (3) / Gerenciado (4) / Otimizado (5).

| Dimensão | Nota | Evidências |
|---|---|---|
| Gestão de relacionamento com clientes | <1–5> | <trecho do discovery> |
| Processos comerciais | <1–5> | <evidência> |
| Uso de dados e analytics | <1–5> | <evidência> |
| Automação e produtividade | <1–5> | <evidência> |
| Experiência do cliente | <1–5> | <evidência> |
| Integração entre sistemas | <1–5> | <evidência> |

**Nota de maturidade geral:** <média ponderada> / 5

---

## 4. Principais Gaps Identificados

Para cada gap, estruture assim:

### Gap 1: <título curto e direto>
- **Situação atual:** o que está acontecendo hoje
- **Impacto no negócio:** custo, risco ou oportunidade perdida
- **Causa raiz:** por que esse gap existe
- **Urgência:** Alta / Média / Baixa

Repita para cada gap relevante (normalmente 3–6 gaps).

---

## 5. Solução Salesforce Recomendada

### 5.1 Arquitetura de solução

Descreva em linguagem de negócio (não técnica) como o Salesforce endereça os gaps:

**Componentes recomendados:**

| Produto / Cloud | O que resolve | Benefício esperado |
|---|---|---|
| <cloud> | <gap que resolve> | <resultado de negócio> |

### 5.2 Justificativa da recomendação

Por que essa combinação de produtos é a mais adequada para esse cliente? Mencione:
- Fit com o segmento
- Cases de referência relevantes (sem citar clientes confidenciais)
- Vantagens competitivas do Salesforce para esse cenário

### 5.3 O que não está no escopo inicial

Liste explicitamente o que foi deixado fora e por quê (priorização, budget, maturidade).

---

## 6. Quick Wins

Ações que podem gerar valor visível em 30–90 dias, antes mesmo da implementação completa:

| Quick Win | Esforço | Impacto | Prazo estimado |
|---|---|---|---|
| <ação> | Baixo/Médio/Alto | Baixo/Médio/Alto | <dias/semanas> |

> Quick wins aumentam buy-in interno e justificam o investimento inicial.

---

## 7. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação sugerida |
|---|---|---|---|
| Resistência à mudança | <Alta/Média/Baixa> | <Alto/Médio/Baixo> | <plano> |
| Qualidade dos dados legados | | | |
| Dependência de integrações | | | |
| <risco específico do cliente> | | | |

---

## 8. Próximos Passos Recomendados

Lista ordenada de ações imediatas:

1. **<Ação>** — Responsável: <cliente ou parceiro> — Prazo: <data ou prazo>
2. **<Ação>** — Responsável: <> — Prazo: <>
3. ...

**Próxima reunião sugerida:** <objetivo da próxima call>

---

## 9. Indicadores de Sucesso (KPIs sugeridos)

Métricas que o cliente deve monitorar para medir o valor da implementação:

| KPI | Baseline atual | Meta em 12 meses | Como medir no Salesforce |
|---|---|---|---|
| <métrica> | <valor atual se conhecido> | <meta> | <dashboard / report> |

---

## Apêndice: Perguntas em aberto

Pontos que precisam ser confirmados antes de avançar para a proposta formal:

- [ ] <pergunta>
- [ ] <pergunta>
```
