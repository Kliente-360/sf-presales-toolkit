# SF Presales Toolkit

Toolkit para consultores Salesforce certificados apoiarem atividades de pré-venda: discovery, assessment, setup de demo e antecipação de objeções.

## Pré-requisitos

- [Salesforce CLI v2](https://developer.salesforce.com/tools/salesforcecli) (`sf`)
- Uma Salesforce Developer Edition autenticada com alias `demo-org`
- Claude Code (para uso das skills via CLAUDE.md)

## Início rápido

```bash
# 1. Verificar org
./scripts/check-org.sh

# 2. Deploy para um segmento
./scripts/deploy-demo.sh varejo

# 3. Carregar dados de demo
./scripts/load-data.sh varejo
```

## Estrutura

```
sf-presales-toolkit/
├── CLAUDE.md           # Instruções para o Claude Code
├── inputs/             # Notas brutas de calls (não versionar dados de clientes)
├── outputs/            # Assessments e roteiros gerados
├── skills/             # Templates de skill para o Claude
├── force-app/          # Metadados Salesforce para deploy
├── data/               # Dados de demo por segmento
└── scripts/            # Shell scripts SFDX
```

## Fluxo de trabalho

1. Cole notas da call em `inputs/` e acione a skill de **discovery**
2. Gere o **assessment** a partir do output do discovery
3. Faça deploy da demo com os scripts e prepare o **roteiro**
4. Antecipe **objeções** antes da reunião

Veja `CLAUDE.md` para instruções detalhadas de uso com Claude Code.
