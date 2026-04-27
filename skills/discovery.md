# Skill: Discovery Analysis

Analisa notas brutas de uma call de discovery e produz um relatório estruturado pronto para alimentar o assessment.

---

## Como usar

Cole as notas brutas da call (transcrição, anotações manuais, resumo do CRM) e peça:

> "Use a skill de discovery nas notas abaixo e salve o output em outputs/<cliente>_<data>_discovery.md"

---

## Template de output

```markdown
# Discovery Analysis — <Nome do Cliente>
**Data da call:** <data>
**Segmento:** <varejo | financeiro | saude | outro>
**Participantes do cliente:** <nomes e cargos>
**Conduzido por:** <seu nome>

---

## 1. Dores Principais Identificadas

Liste cada dor em ordem de impacto percebido. Para cada uma:

- **Dor:** descrição clara do problema
- **Impacto:** o que está custando ao cliente (tempo, dinheiro, retenção, etc.)
- **Evidência:** trecho das notas que confirma essa dor
- **Prioridade:** Alta / Média / Baixa

Exemplo:
- **Dor:** Equipe de vendas não tem visibilidade do pipeline em tempo real
- **Impacto:** Previsão de receita imprecisa, reuniões de forecast de 2h semanais
- **Evidência:** "A gente olha para o Excel toda semana e nunca bate"
- **Prioridade:** Alta

---

## 2. Processos Atuais Mapeados

Descreva como o cliente opera hoje. Para cada processo:

- **Processo:** nome do processo
- **Como funciona hoje:** descrição do fluxo atual
- **Ferramentas usadas:** sistemas, planilhas, e-mail, etc.
- **Principal ineficiência:** o que mais trava esse processo

---

## 3. Sistemas Legados Citados

| Sistema | Função atual | Integração necessária? | Possível substituição? |
|---|---|---|---|
| <nome> | <o que faz> | Sim / Não / Talvez | Sim / Não |

---

## 4. Stakeholders e Papéis

| Nome | Cargo | Papel na decisão | O que mais importa para ele/ela |
|---|---|---|---|
| <nome> | <cargo> | Decisor / Influenciador / Usuário final / Bloqueador | <motivação principal> |

**Quem assina o contrato:** <nome ou cargo>
**Quem vai usar o sistema no dia a dia:** <perfis>
**Quem pode travar a decisão:** <nome ou cargo e por quê>

---

## 5. Prazo e Urgência

- **Prazo declarado pelo cliente:** <ex: "precisamos de algo rodando até o Q3">
- **Driver de urgência:** <o que está forçando a decisão agora>
- **Eventos críticos:** <datas importantes — lançamento de produto, auditoria, sazonalidade>
- **Urgência percebida (1–5):** <nota com justificativa>

---

## 6. Mapeamento para Salesforce Clouds

Com base nas dores e processos identificados, as clouds mais relevantes são:

| Cloud Salesforce | Dores que resolve | Fit (Alto/Médio/Baixo) |
|---|---|---|
| Sales Cloud | <dores mapeadas> | <fit> |
| Service Cloud | <dores mapeadas> | <fit> |
| Marketing Cloud | <dores mapeadas> | <fit> |
| Data Cloud | <dores mapeadas> | <fit> |
| Health Cloud | <dores mapeadas> | <fit> |
| Financial Services Cloud | <dores mapeadas> | <fit> |
| Experience Cloud | <dores mapeadas> | <fit> |
| Agentforce / Einstein | <dores mapeadas> | <fit> |

> Inclua apenas as clouds relevantes. Remova as demais.

---

## 7. Perguntas de Follow-up Recomendadas

Liste as perguntas mais importantes para a próxima call, priorizadas por impacto na qualificação:

1. **<Pergunta>** — Por que perguntar: <justificativa>
2. **<Pergunta>** — Por que perguntar: <justificativa>
3. ...

Categorize as perguntas quando possível:
- Perguntas técnicas (integrações, dados, infra)
- Perguntas de negócio (budget, ROI esperado, KPIs)
- Perguntas de processo de decisão (quem mais está envolvido, há RFP?)
- Perguntas de timing (o que impede começar agora?)

---

## 8. Resumo Executivo da Call

Em 3–5 linhas: o que esse cliente precisa, qual a principal oportunidade e qual o risco principal para fechar.

---

## Metadados

- **Qualidade das notas:** <Alta / Média / Baixa — explique>
- **Nível de maturidade digital percebido:** <1–5 com justificativa>
- **Próximo passo acordado:** <o que foi combinado ao final da call>
```
