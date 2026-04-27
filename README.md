# SF Presales Toolkit

Template para consultores Salesforce certificados apoiarem atividades de pré-venda: discovery, assessment, setup de demo e antecipação de objeções.

## Usar este template

1. Clique em **"Use this template"** no GitHub para criar um novo repositório
2. Clone o novo repositório: `git clone <url-do-seu-repo>`
3. Autentique sua org de demo (veja abaixo)
4. Pronto — abra no Claude Code e siga o fluxo em `CLAUDE.md`

## Pré-requisitos

- [Salesforce CLI v2](https://developer.salesforce.com/tools/salesforcecli) (`sf`)
- Uma Salesforce Developer Edition autenticada com alias `demo-org`
- Claude Code (para uso das skills via `CLAUDE.md`)

## Configuração inicial (primeira vez)

```bash
# Autenticar sua Developer Edition
sf org login web --alias demo-org --set-default

# Verificar se está tudo certo
./scripts/check-org.sh
```

## Início rápido

```bash
# Deploy dos metadados para um segmento
./scripts/deploy-demo.sh varejo   # ou: financeiro | saude

# Carregar dados de demo
./scripts/load-data.sh varejo

# Abrir a org
sf org open --target-org demo-org
```

## Estrutura

```
sf-presales-toolkit/
├── CLAUDE.md               # Instruções para o Claude Code
├── sfdx-project.json       # Configuração do projeto Salesforce CLI
├── inputs/                 # Notas brutas de calls (não versionar dados reais)
├── outputs/                # Assessments e roteiros gerados (ignorado pelo git)
├── skills/
│   ├── discovery.md        # Análise de notas de call
│   ├── assessment.md       # Documento de diagnóstico profissional
│   ├── demo-script.md      # Roteiro de demo personalizado
│   └── objections.md       # Antecipação e resposta a objeções
├── force-app/              # Metadados Salesforce para deploy
├── data/
│   ├── varejo/             # Dados de demo — varejo/e-commerce/franquias
│   ├── financeiro/         # Dados de demo — bancos/seguradoras/fintechs
│   └── saude/              # Dados de demo — hospitais/planos/healthtechs
└── scripts/
    ├── check-org.sh        # Verifica autenticação da org
    ├── deploy-demo.sh      # Deploy de metadados por segmento
    └── load-data.sh        # Importa dados de demo por segmento
```

## Fluxo de trabalho com Claude Code

```
1. DISCOVERY   → cole notas da call → acione skills/discovery.md
2. ASSESSMENT  → use o discovery como input → acione skills/assessment.md
3. DEMO SETUP  → scripts de deploy → acione skills/demo-script.md
4. OBJEÇÕES    → use o assessment como contexto → acione skills/objections.md
```

Outputs são salvos automaticamente em `outputs/` com o padrão `<cliente>_<data>_<tipo>.md`.
A pasta `outputs/` está no `.gitignore` para proteger dados de clientes.

Veja `CLAUDE.md` para instruções detalhadas de uso com Claude Code.
