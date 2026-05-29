#!/usr/bin/env bash

set -euo pipefail

if ! command -v azd >/dev/null 2>&1; then
  echo "azd is required but was not found in PATH."
  exit 1
fi

if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLI (az) is required but was not found in PATH."
  exit 1
fi

if [[ "${1:-}" != "--yes" ]]; then
  echo "Refusing to delete anything without explicit confirmation."
  echo "Run: scripts/destroy_resource_group.sh --yes"
  exit 1
fi

eval "$(azd env get-values)"

if [[ -z "${AZURE_RESOURCE_GROUP:-}" ]]; then
  echo "AZURE_RESOURCE_GROUP is not set in the current azd environment."
  exit 1
fi

echo "Deleting Azure resource group: ${AZURE_RESOURCE_GROUP}"
az group delete --name "${AZURE_RESOURCE_GROUP}" --yes --no-wait
echo "Delete request submitted."
