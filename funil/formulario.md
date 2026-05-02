# Formulário de Discovery — SF Presales Toolkit

Estrutura completa do formulário de discovery para configurar no Typeform, Google Forms ou ferramenta similar.
Os campos e opções aqui definem exatamente o que `pipeline/ingestao.py` espera como entrada.

---

## BLOCO 1 — EMPRESA

**1.1 Nome da empresa** *(obrigatório)*
> Texto livre

**1.2 Segmento** *(obrigatório — escolha única)*
- Varejo / E-commerce / Franquias
- Financeiro / Fintech / Seguradora
- Saúde / Healthtech / Plano de saúde
- Serviços profissionais / Consultoria
- Indústria / Manufatura
- Outro (especifique)

**1.3 Porte da empresa** *(obrigatório — escolha única)*
- 1–10 funcionários
- 11–50 funcionários
- 51–200 funcionários
- 201–500 funcionários
- Acima de 500 funcionários

**1.4 Número de vendedores / atendentes** *(obrigatório — número)*
> Campo numérico (ex: 8)

**1.5 Faturamento anual estimado** *(obrigatório — escolha única)*
- Até R$ 1 milhão
- R$ 1 milhão – R$ 5 milhões
- R$ 5 milhões – R$ 20 milhões
- R$ 20 milhões – R$ 100 milhões
- Acima de R$ 100 milhões
- Prefiro não informar

**1.6 Seu cargo** *(obrigatório — escolha única)*
- CEO / Sócio / Fundador
- VP / Diretor de Vendas
- Gerente Comercial / de Operações
- Consultor / Analista
- TI / Tecnologia
- Outro

---

## BLOCO 2 — SITUAÇÃO ATUAL

**2.1 Usa CRM hoje?** *(obrigatório — escolha única)*
- Sim, uso um CRM dedicado
- Não, registro em planilha (Excel / Google Sheets)
- Não registro nada formalmente

**2.2 Qual CRM usa atualmente?** *(condicional — aparece se 2.1 = "Sim")*
- Salesforce
- HubSpot
- Pipedrive
- RD Station CRM
- Microsoft Dynamics
- Outro (especifique)

**2.3 Há quanto tempo usa o CRM atual?** *(condicional — aparece se 2.1 = "Sim")*
- Menos de 1 ano
- 1 a 3 anos
- Mais de 3 anos

**2.4 Taxa de adoção estimada do time** *(condicional — aparece se 2.1 = "Sim")*
- Menos de 30% do time usa regularmente
- 30% a 60% do time usa
- 60% a 80% do time usa
- Acima de 80% do time usa

**2.5 Quantas ferramentas diferentes o time usa para registrar vendas e atendimento?** *(obrigatório — escolha única)*
- 1 (tudo centralizado)
- 2 a 3 ferramentas
- 4 a 5 ferramentas
- Mais de 5 ferramentas

---

## BLOCO 3 — DORES PRINCIPAIS

**3.1 Selecione as situações que mais impactam seu negócio hoje** *(múltipla escolha)*

- Não sei onde estão minhas oportunidades em andamento
- Meu time não registra as atividades de vendas
- Perco negócios sem entender o motivo
- Meu ciclo de vendas é muito longo
- Não consigo fazer previsão de receita confiável
- Meu atendimento não tem histórico do cliente
- Leads chegam mas não são seguidos adequadamente
- Não sei a performance individual de cada vendedor
- Dados duplicados e inconsistentes entre sistemas
- Integração difícil entre as ferramentas que uso
- Relatórios demoram muito para serem gerados
- Falta visibilidade do funil em tempo real

---

## BLOCO 4 — OBJETIVO E CONTEXTO

**4.1 O que você quer resolver nos próximos 90 dias?** *(obrigatório — texto livre)*
> Campo de texto longo

**4.2 Já tentou resolver antes? O que aconteceu?** *(opcional — texto livre)*
> Campo de texto longo

**4.3 Qual seria o resultado ideal em 6 meses?** *(obrigatório — texto livre)*
> Campo de texto longo

**4.4 Tem equipe de TI ou parceiro técnico?** *(obrigatório — escolha única)*
- Sim, equipe interna de TI
- Sim, parceiro / agência terceirizado
- Não tenho suporte técnico

**4.5 Qual o prazo para tomar a decisão?** *(obrigatório — escolha única)*
- Imediato — quero começar este mês
- 1 a 3 meses
- 3 a 6 meses
- Ainda estou explorando, sem prazo definido

**4.6 Qual o orçamento estimado para o projeto de implementação?** *(obrigatório — escolha única)*
- Até R$ 10.000
- R$ 10.000 – R$ 30.000
- R$ 30.000 – R$ 80.000
- R$ 80.000 – R$ 200.000
- Acima de R$ 200.000
- Ainda não definido

---

## BLOCO 5 — PACOTE DE INTERESSE

**5.1 Qual pacote tem interesse?** *(obrigatório — escolha única)*

- **Diagnóstico (R$ 497)** — Documento completo de diagnóstico Salesforce entregue em 24h
- **Diagnóstico + Demo (R$ 997)** — Diagnóstico + demo ao vivo de 45 min com org configurada
- **Diagnóstico + Demo + Proposta (R$ 1.997)** — Pacote completo com proposta técnica pronta para aprovação

**5.2 Como conheceu nosso trabalho?** *(obrigatório — escolha única)*
- LinkedIn
- Indicação de conhecido
- Google / pesquisa
- Evento ou palestra
- YouTube / conteúdo online
- Outro

**5.3 Tem alguma pergunta ou contexto adicional que queira compartilhar?** *(opcional — texto livre)*
> Campo de texto longo

---

## Notas de configuração

- **Lógica condicional:** os campos 2.2, 2.3 e 2.4 só aparecem se 2.1 = "Sim"
- **Export:** configure o export automático em JSON para facilitar o uso com `pipeline/ingestao.py`
- **Webhook:** se usar Typeform, configure webhook para POST em JSON para automação completa
- **Obrigatórios:** campos marcados como obrigatórios não devem permitir avanço sem resposta
- **Identificador único:** use o e-mail ou nome da empresa como identificador do respondente
