# Templates de Email — Funil Comercial SF Presales Toolkit

Templates prontos para cada etapa do funil. Todos em PT-BR, tom consultivo e direto.
Substitua os campos `{VARIAVEL}` antes de enviar.

---

## EMAIL 1 — Confirmação de recebimento (enviar imediatamente após pagamento)

**Assunto:** Recebemos seu formulário — diagnóstico em 24h, {NOME_CONTATO}

---

Olá, {NOME_CONTATO}.

Confirmamos o recebimento do seu formulário e do pagamento referente ao **{NOME_PACOTE}**.

Aqui está o que acontece agora:

**Nas próximas 24 horas:**
Vou analisar as respostas que você compartilhou e preparar o diagnóstico personalizado para {NOME_EMPRESA}. O documento cobre situação atual, dores mapeadas, solução Salesforce recomendada e estimativa de investimento.

**O que você vai receber:**
{SE_PACOTE_1}
- Documento de diagnóstico completo (formato PDF, ~10–15 páginas)
- Email com os 3 principais achados e CTA para uma call de apresentação
{/SE_PACOTE_1}
{SE_PACOTE_2_3}
- Documento de diagnóstico completo (formato PDF, ~10–15 páginas)
- Link para agendar a demo ao vivo de 45 minutos
- Org Salesforce configurada com dados do seu segmento
{/SE_PACOTE_2_3}
{SE_PACOTE_3}
- Proposta técnica completa de implementação (após a demo)
{/SE_PACOTE_3}

**Alguma dúvida urgente?**
Responda este email ou me chame no WhatsApp: {WHATSAPP}.

Até amanhã,
{SEU_NOME}
{EMPRESA} | Consultor Salesforce Certificado

---

## EMAIL 2 — Entrega do diagnóstico

**Assunto:** Seu diagnóstico Salesforce está pronto — {NOME_EMPRESA}

---

Olá, {NOME_CONTATO}.

O diagnóstico de {NOME_EMPRESA} está pronto. Segue em anexo.

Analisei as respostas do formulário e identifiquei **três pontos que merecem atenção imediata**:

**1. {ACHADO_PRINCIPAL_1}**
{DESCRICAO_ACHADO_1_2_LINHAS}

**2. {ACHADO_PRINCIPAL_2}**
{DESCRICAO_ACHADO_2_2_LINHAS}

**3. {ACHADO_PRINCIPAL_3}**
{DESCRICAO_ACHADO_3_2_LINHAS}

O documento completo detalha cada um desses pontos com a solução recomendada, casos de uso específicos para {SEGMENTO} e uma estimativa de investimento e ROI.

{SE_PACOTE_1}
**Quer que eu apresente o diagnóstico?**
Ofereço uma call de 30 minutos para apresentar os achados e responder perguntas — sem custo adicional. Se fizer sentido, posso preparar também uma **demo ao vivo** (Pacote 2, R$ 997) ou uma **proposta técnica completa** (Pacote 3, R$ 1.997).

→ [Agendar call de 30 minutos]({LINK_CALENDLY})
{/SE_PACOTE_1}
{SE_PACOTE_2_3}
**Próximo passo: a demo**
Sua org Salesforce já está sendo configurada com dados do segmento {SEGMENTO}. Escolha o horário que funciona melhor:

→ [Agendar demo de 45 minutos]({LINK_CALENDLY})

Recomendo agendar ainda essa semana para aproveitar o contexto fresco do diagnóstico.
{/SE_PACOTE_2_3}

Qualquer dúvida sobre o documento, responda este email.

{SEU_NOME}
{EMPRESA} | Consultor Salesforce Certificado

---

## EMAIL 3 — Agendamento da demo (Pacotes 2 e 3)

**Assunto:** Demo preparada para {NOME_EMPRESA} — confirmar horário

---

Olá, {NOME_CONTATO}.

A demo para {NOME_EMPRESA} está pronta.

**O que configurei para você:**
- Org Salesforce Developer Edition com dados realistas do segmento {SEGMENTO}
- Roteiro personalizado para as dores que você identificou no formulário
- Foco em: {DORES_PRIORIZADAS}

**O que você vai ver na demo (45 min):**
1. {BLOCO_DEMO_1} — {DESCRICAO_BLOCO_1}
2. {BLOCO_DEMO_2} — {DESCRICAO_BLOCO_2}
3. {BLOCO_DEMO_3} — {DESCRICAO_BLOCO_3}
4. Visão executiva: dashboards e previsão de receita

**Para aproveitar melhor os 45 minutos:**
- Traga 1 ou 2 pessoas do time que vão usar o sistema
- Se puder, tenha em mãos um exemplo de negócio que perderam recentemente — vamos usá-lo ao vivo na demo

→ [Escolher horário]({LINK_CALENDLY})

Até lá,
{SEU_NOME}
{EMPRESA} | Consultor Salesforce Certificado

---

## EMAIL 4 — Follow-up pós-demo

**Assunto:** Próximos passos após nossa conversa — {NOME_EMPRESA}

---

Olá, {NOME_CONTATO}.

Foi ótimo conversar com você e o time de {NOME_EMPRESA} hoje.

**Resumo do que discutimos:**
- {PONTO_DISCUTIDO_1}
- {PONTO_DISCUTIDO_2}
- {PONTO_DISCUTIDO_3}

**O que ficou claro para mim:**
{OBSERVACAO_PERSONALIZADA}

{SE_PACOTE_2_UPSELL}
**Próximo passo recomendado: Proposta Técnica**
Com base no que vimos, faz sentido avançar para a proposta completa de implementação. Posso ter isso pronto em 48 horas.

→ [Contratar Proposta Técnica — R$ 1.000 (complemento)]({LINK_PAGAMENTO})
{/SE_PACOTE_2_UPSELL}
{SE_PACOTE_3}
**Proposta em anexo**
A proposta técnica completa está em anexo — pronta para revisão interna.

**Condições válidas por 30 dias.**

Sugiro uma call de 30 minutos para revisar juntos: [{LINK_CALENDLY}]
{/SE_PACOTE_3}

Qualquer dúvida, estou à disposição.

{SEU_NOME}
{EMPRESA} | Consultor Salesforce Certificado

---

## EMAIL 5 — Follow-up sem resposta (enviar após 7 dias sem retorno)

**Assunto:** Ainda faz sentido evoluirmos? — {NOME_EMPRESA}

---

Olá, {NOME_CONTATO}.

Só passando para checar se o diagnóstico foi útil e se ainda faz sentido evoluirmos a conversa.

Entendo que às vezes as prioridades mudam — não tem problema nenhum.

Caso ainda esteja avaliando: o principal ponto identificado no diagnóstico de {NOME_EMPRESA} foi **{ACHADO_MAIS_CRITICO}**. Esse tipo de gap tende a aumentar de custo com o tempo.

**Recurso adicional sem custo:**
→ {LINK_CASE_OU_CONTEUDO}

Se o timing mudar, é só responder este email. Guardo o contexto do diagnóstico por 90 dias.

{SEU_NOME}
{EMPRESA} | Consultor Salesforce Certificado

---

## Guia de personalização

| Variável | Onde buscar |
|---|---|
| `{NOME_CONTATO}` | Campo 1.6 do formulário |
| `{NOME_EMPRESA}` | Campo 1.1 do formulário |
| `{NOME_PACOTE}` | Campo 5.1 do formulário |
| `{SEGMENTO}` | Campo 1.2 normalizado por `ingestao.py` |
| `{ACHADO_PRINCIPAL_1..3}` | Output de `diagnostico.py` — seção "Dores Identificadas" |
| `{DORES_PRIORIZADAS}` | Top 3 dores do campo 3.1 por impacto |
| `{BLOCO_DEMO_1..3}` | Output de `demo_setup.py` — seção "Roteiro de Telas" |
| `{LINK_CALENDLY}` | Seu link Calendly pessoal |
| `{LINK_PAGAMENTO}` | Link do checkout (Hotmart, Stripe, etc.) |
| `{WHATSAPP}` | Seu número com DDI: +55 11 9xxxx-xxxx |
