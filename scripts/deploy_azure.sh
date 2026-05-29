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

if [[ "${1:-}" != "" ]]; then
  azd env set AZURE_LOCATION "$1"
fi

if [[ "${2:-}" != "" ]]; then
  azd env set AZURE_RESOURCE_GROUP "$2"
fi

echo "Current azd environment values:"
azd env get-values

echo
echo "Starting Azure deployment with azd up..."
azd up
