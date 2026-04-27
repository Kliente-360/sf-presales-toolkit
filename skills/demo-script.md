# Skill: Demo Script

Gera um roteiro de demo personalizado e narrativo com base no assessment e no perfil das personas presentes na reunião.

---

## Como usar

Forneça o assessment e a lista de participantes esperados na reunião de demo e peça:

> "Use a skill de demo-script com base no assessment abaixo e salve em outputs/<cliente>_<data>_demo-script.md"

---

## Template de output

```markdown
# Roteiro de Demo — <Nome do Cliente>
**Data da demo:** <data>
**Local / Link:** <presencial ou link da reunião>
**Duração total estimada:** <XX minutos>
**Org de demo:** demo-org
**Segmento:** <varejo | financeiro | saude | outro>

---

## 1. Objetivo da Demo

Em 2–3 linhas: o que essa demo precisa provar para esse cliente específico.

> Não é "mostrar o Salesforce". É: "demonstrar que o Salesforce resolve o problema X do <cliente>, 
> gerando o resultado Y, de um jeito que o sistema deles hoje não consegue."

**Critério de sucesso da reunião:** o que precisa acontecer para a demo ser considerada um sucesso?
- [ ] <critério 1>
- [ ] <critério 2>

---

## 2. Personas Presentes e o que Cada Uma Quer Ver

| Persona | Nome | Cargo | Principal preocupação | O que vai impressioná-la |
|---|---|---|---|---|
| Decisor de negócio | <nome> | <cargo> | ROI, velocidade de implementação | Dashboards executivos, casos de referência |
| Usuário final | <nome> | <cargo> | Facilidade de uso, mobile | UX simplificada, automação que poupa tempo |
| TI / Segurança | <nome> | <cargo> | Integração, dados, compliance | APIs, segurança, histórico de uptime |
| <adicionar personas específicas do cliente> | | | | |

**Quem vai apresentar:** <seu nome>
**Quem vai operar o sistema durante a demo:** <seu nome ou parceiro>

---

## 3. Mensagem Central da Demo

A frase que resume o valor da solução para esse cliente — repita ela no início, meio e fim:

> "<Mensagem central — ex: Com o Salesforce, sua equipe comercial vai parar de perder tempo em 
> relatórios manuais e começar a focar no que realmente importa: fechar negócios.>"

---

## 4. Roteiro de Telas e Flows

### Bloco 1: Abertura e Contextualização
**Duração:** 5 min
**Objetivo:** criar conexão com a realidade do cliente antes de entrar no sistema

**Narrativa:**
> "Vocês me contaram que hoje o processo de [processo X] funciona assim: [descreva o processo atual doloroso]. 
> Isso faz com que [impacto negativo]. Deixa eu mostrar como ficaria com o Salesforce."

**O que mostrar:** nada ainda — falar, não clicar.

**Ponto de pausa:** confirmar com o grupo se a descrição do problema está correta.

---

### Bloco 2: <Nome do módulo / funcionalidade>
**Duração:** <X min>
**Objetivo:** <o que esse bloco precisa provar>
**Dor que resolve:** <dor mapeada no discovery>
**Persona que mais se beneficia:** <persona>

**Narrativa:**
> "<Contexto de negócio antes de abrir a tela>"

**Passos no sistema:**
1. Navegar para: <menu / app / objeto>
2. Mostrar: <o que deve estar na tela>
3. Demonstrar: <ação específica — criar, filtrar, executar flow, etc.>
4. Destacar: <o detalhe que impressiona — campo calculado, automação, IA, etc.>

**Frase de impacto:** "<frase que conecta o que foi visto ao valor de negócio>"

**Ponto de pausa:** <pergunta para engajar o grupo>

---

### Bloco 3: <Nome do módulo / funcionalidade>
**Duração:** <X min>
**Objetivo:** <o que esse bloco precisa provar>
**Dor que resolve:** <dor mapeada no discovery>
**Persona que mais se beneficia:** <persona>

**Narrativa:**
> "<contexto>"

**Passos no sistema:**
1. ...
2. ...
3. ...

**Frase de impacto:** "<frase>"

**Ponto de pausa:** <pergunta>

---

> Repita blocos conforme necessário. Recomendado: 3–5 blocos de funcionalidade.

---

### Bloco Final: Visão de Futuro e ROI
**Duração:** 5–8 min
**Objetivo:** fechar com o impacto esperado e provocar a discussão de próximos passos

**Narrativa:**
> "O que vocês viram hoje é a fase 1. Em 90 dias, uma equipe como a de vocês já estaria [resultado 1]. 
> Em 6 meses, [resultado 2]. Clientes do setor [segmento] como [referência de case] conseguiram [resultado mensurável]."

**O que mostrar:** dashboard executivo com KPIs / relatório de pipeline / app no mobile

**Pergunta de fechamento:** "O que vocês viram hoje responde às perguntas que tinham antes de entrar aqui?"

---

## 5. Dados de Demo a Usar

| Dado | Valor no sistema | Por que usar esse valor |
|---|---|---|
| Nome da conta de exemplo | <nome fictício realista pro segmento> | Parece real, sem expor dados |
| Volume de registros | <quantidade que impressiona sem travar> | |
| Cenário de negócio | <qual história de negócio está configurada> | |

**Org a abrir:** `sf org open --target-org demo-org`

---

## 6. Preparação Técnica (checklist pré-demo)

- [ ] Executar `scripts/check-org.sh` e confirmar autenticação
- [ ] Executar `scripts/deploy-demo.sh <segmento>`
- [ ] Executar `scripts/load-data.sh <segmento>`
- [ ] Abrir a org e navegar pelos blocos ao menos uma vez antes da reunião
- [ ] Testar todos os flows e automações que serão demonstrados
- [ ] Configurar o App Launcher com os apps na ordem certa
- [ ] Ter a org aberta no browser antes do cliente entrar na reunião
- [ ] Backup: ter screenshots dos momentos-chave caso a internet falhe

---

## 7. Gestão de Tempo

| Bloco | Início | Duração | Responsável |
|---|---|---|---|
| Abertura | 0:00 | 5 min | <nome> |
| <Bloco 2> | 0:05 | <X> min | <nome> |
| <Bloco 3> | 0:XX | <X> min | <nome> |
| Visão de futuro | 0:XX | 8 min | <nome> |
| Q&A e próximos passos | 0:XX | 10 min | <nome> |
| **Total** | | **<XX> min** | |

**Buffer de segurança:** reserve sempre 10 min de margem. Se um bloco atrasar, corte o próximo — nunca o de fechamento.

---

## 8. Frases a Evitar

Não diga durante a demo:
- "Deixa eu só abrir aqui..." (passa impressão de improviso)
- "Esse é um bug conhecido..." (nunca admitir bugs em demo)
- "Normalmente funciona assim mas..." (cria dúvida)
- "Você consegue fazer isso com qualquer ferramenta..." (não diferencie para baixo)

---

## 9. Próximos Passos a Propor ao Final da Demo

1. <ação concreta — ex: "marcar call técnica com o time de TI">
2. <ação — ex: "enviar proposta comercial até <data>">
3. <ação — ex: "disponibilizar acesso a um ambiente trial por 30 dias">
```
