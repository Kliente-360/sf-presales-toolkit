#!/usr/bin/env bash
# Faz deploy dos metadados de demo para a org demo-org.
# Uso: ./scripts/deploy-demo.sh <segmento>
# Segmentos válidos: varejo | financeiro | saude

set -euo pipefail

ORG_ALIAS="demo-org"
VALID_SEGMENTS=("varejo" "financeiro" "saude")
SOURCE_DIR="force-app/main/default"

echo "======================================"
echo " SF Presales Toolkit — Deploy Demo"
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

echo "[INFO] Segmento selecionado: $SEGMENT"
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

# Verificar se o diretório de metadados existe
if [ ! -d "$SOURCE_DIR" ]; then
  echo "[ERRO] Diretório de metadados não encontrado: $SOURCE_DIR"
  echo "       Certifique-se de estar na raiz do projeto sf-presales-toolkit."
  exit 1
fi

# Verificar se há metadados para deploy
METADATA_COUNT=$(find "$SOURCE_DIR" -type f ! -name '.gitkeep' | wc -l)
if [ "$METADATA_COUNT" -eq 0 ]; then
  echo "[AVISO] Nenhum metadado encontrado em '$SOURCE_DIR'."
  echo "        Adicione seus metadados Salesforce antes de fazer deploy."
  echo "        Estrutura esperada: $SOURCE_DIR/classes/, $SOURCE_DIR/objects/, etc."
  exit 0
fi

echo "[INFO] Metadados encontrados: $METADATA_COUNT arquivo(s)"
echo "[INFO] Iniciando deploy para '$ORG_ALIAS'..."
echo ""

# Deploy dos metadados
sf project deploy start \
  --target-org "$ORG_ALIAS" \
  --source-dir "$SOURCE_DIR" \
  --wait 10

echo ""
echo "[OK] Deploy concluído com sucesso para o segmento '$SEGMENT'."
echo ""
echo "Próximo passo: carregar os dados de demo:"
echo "  ./scripts/load-data.sh $SEGMENT"
echo ""
echo "Abrir a org:"
echo "  sf org open --target-org $ORG_ALIAS"
