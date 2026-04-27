#!/usr/bin/env bash
# Verifica se a org demo-org está autenticada e exibe informações básicas.

set -euo pipefail

ORG_ALIAS="demo-org"

echo "======================================"
echo " SF Presales Toolkit — Check Org"
echo "======================================"
echo ""

# Verificar se o Salesforce CLI está instalado
if ! command -v sf &> /dev/null; then
  echo "[ERRO] Salesforce CLI (sf) não encontrado."
  echo "       Instale em: https://developer.salesforce.com/tools/salesforcecli"
  exit 1
fi

echo "[INFO] Salesforce CLI detectado: $(sf --version 2>/dev/null | head -1)"
echo ""

# Listar orgs autenticadas
echo "[INFO] Orgs autenticadas:"
sf org list 2>/dev/null || echo "       Nenhuma org autenticada encontrada."
echo ""

# Verificar se demo-org existe
echo "[INFO] Verificando org '$ORG_ALIAS'..."
if sf org display --target-org "$ORG_ALIAS" &> /dev/null; then
  echo "[OK] Org '$ORG_ALIAS' autenticada com sucesso."
  echo ""
  echo "--- Detalhes da org ---"
  sf org display --target-org "$ORG_ALIAS"
else
  echo "[AVISO] Org '$ORG_ALIAS' não encontrada ou sessão expirada."
  echo ""
  echo "Para autenticar uma nova org Developer Edition, execute:"
  echo "  sf org login web --alias $ORG_ALIAS --set-default"
  echo ""
  echo "Para autenticar com username/password (sandbox/DE):"
  echo "  sf org login web --alias $ORG_ALIAS --instance-url https://login.salesforce.com"
  exit 1
fi

echo ""
echo "[OK] Verificação concluída. A org está pronta para uso."
