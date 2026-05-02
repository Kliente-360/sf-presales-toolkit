# SF Presales Toolkit

Projeto de apoio a atividades de pré-venda Salesforce. Usado por consultores certificados para analisar oportunidades, gerar assessments e preparar demos personalizadas.

---

## Objetivo

Transformar notas brutas de calls de discovery em entregáveis profissionais:
assessments estruturados, roteiros de demo e antecipação de objeções — tudo
conectado a um ambiente Salesforce Developer Edition pronto para demonstração.

---

## Segmentos suportados

Antes de gerar qualquer assessment ou demo, **sempre pergunte o segmento do cliente**:

- `varejo` — Retail, e-commerce, franquias
- `financeiro` — Bancos, seguradoras, fintechs
- `saude` — Hospitais, clínicas, planos de saúde, healthtechs
- `outro` — Descreva o segmento antes de prosseguir

O segmento determina qual pasta de dados e metadados será usada nos scripts.

---

## Skills disponíveis

| Skill | Arquivo | Quando usar |
|---|---|---|
| Discovery Analysis | `skills/discovery.md` | Após receber notas brutas de uma call |
| Assessment | `skills/assessment.md` | Para gerar o documento formal de diagnóstico |
| Demo Script | `skills/demo-script.md` | Para preparar o roteiro antes da demo |
| Objections | `skills/objections.md` | Para antecipar perguntas difíceis |

Para acionar uma skill, diga: *"Use a skill de discovery nas notas abaixo"* e cole o conteúdo.

---

## Fluxo completo de trabalho

```
1. DISCOVERY
   └─ Cole as notas brutas da call
   └─ Acione skills/discovery.md
   └─ Salve o output em outputs/<cliente>_<data>_discovery.md

2. ASSESSMENT
   └─ Use o output do discovery como input
   └─ Acione skills/assessment.md
   └─ Salve em outputs/<cliente>_<data>_assessment.md

3. DEMO SETUP
   └─ Execute scripts/check-org.sh para verificar a org
   └─ Execute scripts/deploy-demo.sh <segmento>
   └─ Execute scripts/load-data.sh <segmento>
   └─ Acione skills/demo-script.md para gerar o roteiro
   └─ Salve em outputs/<cliente>_<data>_demo-script.md

4. PREP OBJEÇÕES
   └─ Use o output do assessment como contexto
   └─ Acione skills/objections.md
   └─ Salve em outputs/<cliente>_<data>_objections.md
```

---

## Convenção de nomenclatura de outputs

Todos os arquivos gerados devem ser salvos em `/outputs/` com o padrão:

```
outputs/<nome-cliente>_<YYYY-MM-DD>_<tipo>.md
```

Exemplos:
- `outputs/banco-meridian_2026-04-27_assessment.md`
- `outputs/rede-flores_2026-04-27_demo-script.md`

**Sempre salve os outputs nessa pasta.** Nunca sobrescreva um arquivo existente sem confirmar.

---

## Org de demo

- **Alias:** `demo-org`
- **Tipo:** Salesforce Developer Edition

### Comandos SFDX principais

```bash
# Verificar autenticação e status da org
sf org display --target-org demo-org

# Abrir a org no browser
sf org open --target-org demo-org

# Deploy de metadados
sf project deploy start --target-org demo-org --source-dir force-app/

# Import de dados (via plano JSON)
sf data import tree --target-org demo-org --plan data/<segmento>/plan.json

# Listar orgs autenticadas
sf org list
```

### Autenticar uma nova org

```bash
# Login via browser (recomendado para Developer Edition)
sf org login web --alias demo-org --set-default

# Verificar se autenticou
scripts/check-org.sh
```

---

## Salesforce Clouds de referência

Mapeie as dores identificadas no discovery para as clouds abaixo:

| Cloud | Casos de uso típicos |
|---|---|
| Sales Cloud | Pipeline, gestão de oportunidades, previsão de receita |
| Service Cloud | Atendimento ao cliente, casos, knowledge base, field service |
| Marketing Cloud | Jornadas multicanal, email, SMS, personalização |
| Data Cloud | Unificação de dados, CDP, segmentação em tempo real |
| Commerce Cloud | Storefront B2C/B2B, checkout, gestão de pedidos |
| Health Cloud | Coordenação de cuidados, pacientes, planos de saúde |
| Financial Services Cloud | Gestão de relacionamento, planejamento financeiro, compliance |
| Experience Cloud | Portais de cliente, parceiro, autoatendimento |
| Einstein / Agentforce | IA generativa, copilots, automação inteligente |

---

## Notas importantes

- Sempre confirme o **segmento** antes de iniciar qualquer análise.
- Outputs ficam em `/outputs/` — nunca em `/inputs/`.
- A pasta `/inputs/` é para colar notas brutas e arquivos do cliente.
- Scripts em `/scripts/` assumem que o CLI `sf` (Salesforce CLI v2) está instalado.
- Metadados por segmento ficam em `/force-app/` organizados por pasta.
- Dados de demo ficam em `/data/<segmento>/`.

---

## Funil Comercial de Diagnóstico

Pipeline automatizado que transforma respostas de formulário em entregáveis profissionais prontos para envio.

### Fluxo completo para um novo cliente

```bash
# 1. Processar formulário (JSON, CSV ou entrada manual)
python pipeline/ingestao.py
# → salva em inputs/{cliente}_{data}_formulario.json

# 2. Gerar diagnóstico (~1 min)
python pipeline/diagnostico.py <slug-cliente>
# → salva em outputs/{cliente}_{data}_diagnostico.md

# 3a. Setup da demo — Pacotes 2 e 3
python pipeline/demo_setup.py <slug-cliente>
# → deploy na demo-org + outputs/{cliente}_{data}_roteiro.md + _objecoes.md

# 3b. Gerar proposta — Pacote 3
python pipeline/proposta.py <slug-cliente>
# → salva em outputs/{cliente}_{data}_proposta.md
```

### Pacotes e entregáveis

| Pacote | Preço | Scripts usados | Entregáveis |
|---|---|---|---|
| Diagnóstico | R$ 497 | `ingestao` + `diagnostico` | `_diagnostico.md` |
| Diag + Demo | R$ 997 | + `demo_setup` | + `_roteiro.md`, `_objecoes.md` |
| Diag + Demo + Proposta | R$ 1.997 | + `proposta` | + `_proposta.md` |

### Arquivos do funil

| Arquivo | Descrição |
|---|---|
| `funil/formulario.md` | Estrutura do formulário para configurar no Typeform / Google Forms |
| `funil/pacotes.md` | Definição dos pacotes, critérios de upsell e scripts de abordagem |
| `funil/email_templates.md` | Templates de email prontos para cada etapa (5 emails) |

### Templates de output

Os templates em `outputs/templates/` são a referência estrutural dos documentos gerados.
Os scripts preenchem os placeholders `{VARIAVEL}` automaticamente — não edite os placeholders.

### Critérios de upsell automáticos (detectados por `ingestao.py`)

- Empresa > 50 funcionários → sugerir Pacote 3
- Budget declarado > R$ 30k → sugerir Pacote 3
- Prazo imediato → sugerir Pacote 2 ou 3
- Já usa Salesforce → sugerir Pacote 2 (demo de evolução)
- 3+ dores críticas marcadas → sugerir Pacote 3
