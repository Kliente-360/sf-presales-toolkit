# Pacotes de Oferta — SF Presales Toolkit

Definição completa dos três pacotes de diagnóstico e pré-venda Salesforce.

---

## PACOTE 1 — Diagnóstico (R$ 497)

### O que está incluído

**Documento de diagnóstico Salesforce** (formato PDF, ~10–15 páginas):

- Sumário executivo escrito para o CEO (2 minutos de leitura)
- Mapeamento detalhado das dores identificadas com impacto no negócio
- Solução Salesforce recomendada com justificativa por segmento
- 3–5 casos de uso específicos para o modelo de negócio do cliente
- Plano de ação em 90 dias (Fundação → Automação → Otimização)
- Estimativa de investimento (licenças + implementação) com faixas de mercado
- ROI estimado com premissas explícitas e memória de cálculo
- Próximos passos com CTA claro

### SLA e esforço

- **Tempo de entrega:** 24 horas após confirmação do pagamento
- **Tempo de preparação estimado:** ~1 hora (revisão do output gerado + personalização final)
- **Gerado por:** `pipeline/diagnostico.py` + revisão manual

### Quando recomendar

- Cliente com budget até R$ 10.000
- Empresa com menos de 20 funcionários
- Decisão em 3–6 meses ("ainda explorando")
- Primeiro contato sem urgência clara

---

## PACOTE 2 — Diagnóstico + Demo (R$ 997)

### O que está incluído

Tudo do Pacote 1, mais:

- **Demo ao vivo de 45 minutos** com org Salesforce configurada
- Org Developer Edition com dados realistas do segmento do cliente
- Roteiro de demo personalizado para as dores específicas identificadas
- Respostas preparadas para as objeções prováveis do perfil do cliente
- Gravação da demo disponibilizada após a call (opcional, com consentimento)

### SLA e esforço

- **Tempo de entrega do diagnóstico:** 24 horas após pagamento
- **Demo:** agendada pelo cliente via link Calendly (prazo: 5 dias úteis)
- **Tempo de preparação estimado:** ~2 horas (diagnóstico + setup da demo)
- **Gerado por:** `pipeline/diagnostico.py` + `pipeline/demo_setup.py`

### Quando recomendar

- Empresa entre 20 e 100 funcionários
- Budget entre R$ 10.000 e R$ 80.000
- Prazo de decisão: imediato ou 1–3 meses
- Cliente que já usa outro CRM (Pipedrive, HubSpot) e avalia migração
- Urgência clara declarada no formulário

---

## PACOTE 3 — Diagnóstico + Demo + Proposta (R$ 1.997)

### O que está incluído

Tudo do Pacote 2, mais:

- **Proposta técnica completa de implementação**, pronta para aprovação e assinatura:
  - Escopo detalhado (inclusos e excluídos explicitamente)
  - Arquitetura técnica proposta em linguagem de negócio
  - Cronograma por fase (30 / 60 / 90 dias ou por sprints)
  - Equipe necessária (papéis do cliente e do parceiro)
  - Tabela de riscos e mitigações
  - Investimento detalhado com opções de pacote de implementação
  - Condições comerciais e termos básicos

### SLA e esforço

- **Diagnóstico:** 24 horas após pagamento
- **Demo:** agendada pelo cliente (prazo: 5 dias úteis)
- **Proposta:** entregue em até 48 horas após a demo
- **Tempo de preparação estimado:** ~3 horas no total
- **Gerado por:** `pipeline/diagnostico.py` + `pipeline/demo_setup.py` + `pipeline/proposta.py`

### Quando recomendar

- Empresa acima de 50 funcionários
- Budget declarado acima de R$ 30.000
- Prazo imediato ("quero começar este mês")
- Múltiplas dores críticas no formulário (3 ou mais marcadas como impacto alto)
- CEO ou VP presente — decisor com poder de assinar

---

## Critérios de Upsell Durante a Entrega

Use esses critérios para sugerir upgrade durante a entrega do diagnóstico:

| Sinal | Upgrade sugerido | Script de abordagem |
|---|---|---|
| Empresa > 50 funcionários | Pacote 1 → 3 | "Com o porte de vocês, a proposta técnica evita surpresas na negociação interna" |
| Budget declarado > R$ 30k | Pacote 1 → 3 | "Com esse investimento em vista, faz sentido ter o escopo documentado antes de avançar" |
| Prazo imediato | Pacote 1 → 2 | "Se a urgência é real, a demo acelera a decisão do time — posso preparar para essa semana" |
| Já usa Salesforce | Pacote 1 → 2 | "A demo vai mostrar exatamente o delta entre o que vocês têm hoje e o que estão deixando na mesa" |
| 3+ dores críticas | Pacote 1 → 3 | "Com tantos pontos de dor, o diagnóstico só é o começo — a proposta fecha o ciclo" |
| Sem equipe de TI | Pacote 2 → 3 | "Sem TI interna, ter o escopo e cronograma documentados protege vocês na hora de contratar" |

---

## Posicionamento Comercial

### Objeção: "Por que pagar pelo diagnóstico se posso pedir uma proposta grátis?"

> "Qualquer proposta grátis é genérica por definição — cabe no cliente A, B e C sem mudança.
> O diagnóstico que entrego é específico para o seu negócio, suas dores, seu segmento e seu porte.
> Ele serve tanto para você tomar a decisão certa quanto para eu preparar uma proposta que
> realmente faz sentido. É a diferença entre comprar roupa no manequim e comprar sob medida."

### Objeção: "R$ 1.997 é caro para uma proposta"

> "Compare com o custo de contratar a implementação errada. Uma proposta técnica mal feita
> resulta em escopo aberto, aditivos e projetos que dobram de custo. O que entrego aqui é
> exatamente o documento que você vai usar para negociar internamente e com parceiros —
> com escopo, cronograma e investimento fechados."
