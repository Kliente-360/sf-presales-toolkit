# Skill: Objections Handler

Antecipa objeções e prepara respostas estruturadas com base no segmento do cliente e nas notas de discovery.

---

## Como usar

Forneça o assessment ou as notas de discovery como contexto e peça:

> "Use a skill de objections com base no assessment abaixo e salve em outputs/<cliente>_<data>_objections.md"

---

## Template de output

```markdown
# Antecipação de Objeções — <Nome do Cliente>
**Data:** <data>
**Segmento:** <varejo | financeiro | saude | outro>
**Baseado em:** <arquivo de discovery / assessment de referência>

---

## Como usar este documento

Para cada objeção:
1. **Ouça completamente** — não interrompa, deixe o cliente terminar
2. **Valide** — "Faz todo sentido essa preocupação"
3. **Responda** com a estrutura: contexto → fato → exemplo → pergunta de retorno
4. **Verifique** — "Isso responde sua dúvida?"

---

## Parte 1: Objeções Universais Salesforce

Objeções que aparecem em praticamente todos os ciclos de venda, independente do segmento.

---

### O1. "É muito caro para o nosso porte"

**Contexto:** objeção de preço que normalmente esconde medo de não ter ROI claro.

**Resposta:**
> "Entendo a preocupação. O investimento no Salesforce é real — e justamente por isso 
> trabalhamos com você para mapear o retorno esperado antes de qualquer contrato. 
> Clientes do porte de vocês que implementaram [módulo específico] relatam recuperação 
> do investimento em [X meses], principalmente por [benefício específico ao contexto deles]. 
> O que ajudaria a visualizar melhor esse retorno — um modelo financeiro simples ou cases 
> de empresas similares?"

**Evidências de suporte:**
- Calculadora de ROI da Salesforce (disponível no Salesforce.com/roi)
- Cases de clientes do mesmo segmento e porte
- Estrutura de licenciamento modular (começa pequeno, escala)

**Pergunta de retorno:** "Se o custo ficasse dentro do budget de vocês, o que mais precisaria estar claro para avançar?"

---

### O2. "Já tentamos um CRM antes e não funcionou"

**Contexto:** experiência negativa anterior, normalmente com adoção baixa ou implementação mal feita.

**Resposta:**
> "Você não está sozinho — isso é mais comum do que parece. Na maioria dos casos que vejo, 
> o problema não foi o sistema em si, mas a forma como foi implementado: sem treinar os 
> usuários, sem adaptar os processos antes de migrar, ou sem um champion interno. 
> A pergunta que gosto de fazer é: o que especificamente não funcionou da última vez? 
> Porque dependendo da resposta, posso mostrar exatamente como evitaríamos o mesmo problema."

**Evidências de suporte:**
- Metodologia de implementação (Salesforce Success Plans, parceiros certificados)
- Dados de adoção: [X]% dos usuários ativos após 90 dias com treinamento adequado
- Programa de change management

**Pergunta de retorno:** "O que teria sido diferente para o projeto anterior ter dado certo?"

---

### O3. "Nossa TI não vai aprovar / vai demorar muito para integrar"

**Contexto:** medo de complexidade técnica, resistência da TI ou dependência de um processo de aprovação longo.

**Resposta:**
> "Faz sentido envolver a TI desde cedo — e na verdade, quanto antes melhor. O Salesforce 
> tem uma biblioteca de mais de 3.000 integrações prontas via MuleSoft e APIs nativas, 
> então na maioria dos casos a conversa com TI é mais simples do que parece no início. 
> Podemos organizar uma call técnica separada onde eu respondo diretamente às perguntas 
> da equipe de TI — costuma desbloquear o processo rapidamente. Faz sentido?"

**Evidências de suporte:**
- AppExchange: 7.000+ apps e integrações
- Salesforce Shield para segurança e compliance
- Arquitetura multi-tenant, atualizações automáticas

**Pergunta de retorno:** "Quais sistemas específicos a TI estaria preocupada em integrar?"

---

### O4. "Precisamos pensar melhor / não é o momento"

**Contexto:** adiamento sem motivo claro — normalmente indica que o valor não ficou claro ou há um decisor não mapeado.

**Resposta:**
> "Claro, decisões assim merecem tempo. Só quero entender melhor: quando você diz que 
> não é o momento, é mais uma questão de budget agora, de prioridade interna, ou de 
> precisar de mais informações? Pergunto porque posso ajudar de formas diferentes 
> dependendo do que está travando."

**Evidências de suporte:** (depende da resposta — direcione conforme o motivo real)

**Pergunta de retorno:** "O que precisaria acontecer nos próximos 30 dias para isso virar prioridade?"

---

### O5. "Vamos avaliar outras soluções também (SAP, HubSpot, Microsoft...)"

**Contexto:** processo competitivo. Não entre em modo defensivo.

**Resposta:**
> "Faz todo sentido avaliar. Inclusive recomendo que façam isso — decisão de plataforma 
> é para 5–10 anos. O que posso garantir é que vou ajudar vocês a construir um critério 
> de avaliação justo. Quer que eu compartilhe uma matriz de comparação com os critérios 
> mais importantes para o caso de vocês?"

**Evidências de suporte:**
- Gartner Magic Quadrant (Salesforce como líder consistente)
- Forrester Wave CRM
- G2 e TrustRadius reviews
- Diferencial específico para o segmento

**Pergunta de retorno:** "Quais são os 3 critérios mais importantes para vocês nessa avaliação?"

---

## Parte 2: Objeções por Segmento

---

### Segmento: Varejo

**O-V1. "Nosso volume de SKUs/transações é muito alto para um CRM"**
> "O Salesforce foi construído para escala — temos clientes com bilhões de registros ativos. 
> E com o Data Cloud, conseguimos unificar dados de PDV, e-commerce e programa de fidelidade 
> em tempo real, não em batch. Posso mostrar como isso funciona?"

**O-V2. "Já temos um ERP que faz isso"**
> "ERP e CRM resolvem problemas diferentes — o ERP cuida do back-office, o CRM cuida do 
> relacionamento com o cliente. A pergunta é: seu ERP te diz qual cliente está prestes a 
> churnar antes que ele vá embora? Ou qual produto recomendar para cada cliente no momento 
> certo? Isso é o que o Salesforce faz que o ERP não faz."

---

### Segmento: Financeiro

**O-F1. "LGPD e regulamentação do Banco Central são um risco"**
> "Compliance é exatamente onde o Salesforce se diferencia no setor financeiro. O Salesforce 
> Shield oferece criptografia em nível de campo, trilha de auditoria imutável e controles de 
> acesso granulares — tudo auditável para o Bacen e LGPD. O Financial Services Cloud foi 
> construído com esses requisitos em mente. Posso conectar você com nosso time de segurança 
> para uma sessão técnica?"

**O-F2. "Dados sensíveis de clientes não podem sair do nosso ambiente"**
> "Entendo a preocupação — e é uma das mais comuns no setor. O Salesforce tem opções de 
> residência de dados no Brasil e configurações de soberania de dados. Mas antes de irmos 
> para os detalhes técnicos: que tipo de dados específicos preocupam mais? Porque às vezes 
> a solução é mais simples do que parece."

---

### Segmento: Saúde

**O-S1. "LGPD com dados de pacientes é uma barreira intransponível"**
> "Health Cloud foi construído especificamente para esse contexto — com suporte a HIPAA nos 
> EUA e LGPD no Brasil. Configurações de consentimento, anonimização e controle de acesso 
> são nativos. Temos clientes como [referência de hospital/operadora] operando com esses 
> controles. Posso compartilhar um overview técnico?"

**O-S2. "Os médicos nunca vão usar um novo sistema"**
> "Adoção de médicos é um desafio real — e por isso o Health Cloud tem uma interface 
> construída para o fluxo clínico, não para o fluxo de vendas. A chave é envolver 2–3 
> médicos no design antes de implementar. Você tem algum 'early adopter' na equipe que 
> poderia ser o champion?"

---

## Parte 3: Objeções Específicas deste Cliente

> Esta seção deve ser preenchida com base nas notas de discovery e no perfil do cliente.

**Instrução:** analise as dores, sistemas legados e stakeholders mapeados no discovery e 
gere aqui 3–5 objeções altamente específicas ao contexto desse cliente, com respostas 
personalizadas.

---

### O-E1. <Objeção específica baseada no discovery>

**Origem:** <trecho do discovery que indica essa objeção>
**Quem provavelmente vai levantar:** <persona>

**Resposta:**
> "<resposta personalizada usando contexto do cliente>"

**Evidências:** <case, dado ou referência específica>

**Pergunta de retorno:** "<pergunta>"

---

### O-E2. <Objeção específica>

**Origem:** <trecho>
**Quem vai levantar:** <persona>

**Resposta:**
> "<resposta>"

**Evidências:** <>

**Pergunta de retorno:** "<pergunta>"

---

## Parte 4: Sinais de Compra a Observar

Comportamentos que indicam que o cliente está pronto para avançar — mesmo que não diga explicitamente:

- Perguntas sobre prazo de implementação
- Perguntas sobre integrações com sistemas específicos deles
- Pedido para ver mais detalhes de uma funcionalidade específica
- Menção de budget ou ciclo orçamentário
- Solicitar referências ou cases do setor deles
- Pedir para incluir mais pessoas da empresa na próxima call

**Quando identificar esses sinais:** proponha próximo passo concreto imediatamente.

---

## Parte 5: Quando Escalar

Situações que exigem envolver outras pessoas da sua equipe:

| Situação | Quem envolver | Como acionar |
|---|---|---|
| Dúvidas técnicas profundas de integração | Solution Engineer / Arquiteto | Marcar call técnica separada |
| Negociação de contrato / desconto | Account Executive / Manager | Alinhar internamente antes |
| Referências de clientes do setor | Customer Success / Marketing | Solicitar via programa de referências |
| Prova de conceito (POC) | SE + time de implementação | Definir critérios de sucesso antes |
```
