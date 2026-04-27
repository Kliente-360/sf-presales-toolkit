#!/usr/bin/env bash
# Carrega dados de demo na org demo-org a partir da pasta data/<segmento>/.
# Uso: ./scripts/load-data.sh <segmento>
# Segmentos válidos: varejo | financeiro | saude

set -euo pipefail

ORG_ALIAS="demo-org"
VALID_SEGMENTS=("varejo" "financeiro" "saude")
DATA_BASE_DIR="data"
PLAN_FILE="plan.json"

echo "======================================"
echo " SF Presales Toolkit — Load Data"
echo "======================================"
echo ""

# Validar parâmetro de segmento
if [ $# -eq 0 ]; then
  echo "[ERRO] Segmento não informado."
  echo "Uso: $0 <segmento>"
  echo "Segmentos válidos: ${VALID_SEGMENTS[*]}"
  exit 1
fi

SEGMENT="$1"

VALID=false
for s in "${VALID_SEGMENTS[@]}"; do
  if [ "$s" = "$SEGMENT" ]; then
    VALID=true
    break
  fi
done

if [ "$VALID" = false ]; then
  echo "[ERRO] Segmento '$SEGMENT' inválido."
  echo "Segmentos válidos: ${VALID_SEGMENTS[*]}"
  exit 1
fi

DATA_DIR="$DATA_BASE_DIR/$SEGMENT"
PLAN_PATH="$DATA_DIR/$PLAN_FILE"

echo "[INFO] Segmento selecionado: $SEGMENT"
echo "[INFO] Diretório de dados: $DATA_DIR"
echo "[INFO] Org alvo: $ORG_ALIAS"
echo ""

# Verificar autenticação
echo "[INFO] Verificando autenticação da org..."
if ! sf org display --target-org "$ORG_ALIAS" &> /dev/null; then
  echo "[ERRO] Org '$ORG_ALIAS' não autenticada. Execute primeiro:"
  echo "  ./scripts/check-org.sh"
  exit 1
fi
echo "[OK] Org autenticada."
echo ""

# Verificar se o diretório de dados existe
if [ ! -d "$DATA_DIR" ]; then
  echo "[ERRO] Diretório de dados não encontrado: $DATA_DIR"
  exit 1
fi

# Verificar se o plano de importação existe
if [ ! -f "$PLAN_PATH" ]; then
  echo "[AVISO] Arquivo de plano não encontrado: $PLAN_PATH"
  echo ""
  echo "Para criar dados de demo, adicione arquivos JSON em '$DATA_DIR/' e"
  echo "crie um '$PLAN_FILE' com a estrutura abaixo:"
  echo ""
  cat << 'PLAN_EXAMPLE'
  Exemplo de plan.json:
  [
    {
      "sobject": "Account",
      "saveRefs": true,
      "resolveRefs": false,
      "files": ["accounts.json"]
    },
    {
      "sobject": "Contact",
      "saveRefs": true,
      "resolveRefs": true,
      "files": ["contacts.json"]
    },
    {
      "sobject": "Opportunity",
      "saveRefs": false,
      "resolveRefs": true,
      "files": ["opportunities.json"]
    }
  ]
PLAN_EXAMPLE
  exit 0
fi

# Verificar se há arquivos de dados além do gitkeep
DATA_COUNT=$(find "$DATA_DIR" -type f ! -name '.gitkeep' ! -name "$PLAN_FILE" | wc -l)
if [ "$DATA_COUNT" -eq 0 ]; then
  echo "[AVISO] Nenhum arquivo de dados encontrado em '$DATA_DIR'."
  echo "        Adicione arquivos JSON de dados antes de importar."
  exit 0
fi

echo "[INFO] Arquivos de dados encontrados: $DATA_COUNT"
echo "[INFO] Iniciando importação de dados..."
echo ""

# Importar dados via plano
sf data import tree \
  --target-org "$ORG_ALIAS" \
  --plan "$PLAN_PATH"

echo ""
echo "[OK] Dados carregados com sucesso para o segmento '$SEGMENT'."
echo ""
echo "Abrir a org para verificar:"
echo "  sf org open --target-org $ORG_ALIAS"
