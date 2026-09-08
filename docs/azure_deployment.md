# Azure Deployment

## Current Shared Dashboard

The verified public deployment is [Riyadh Mobility Dashboard](https://ca-rmd-api-riyadh-ud-ua-aesdq5.jollyplant-57daa6ab.uaenorth.azurecontainerapps.io/). It runs in `rg-riyadh-ud-uae-north` in UAE North. Azure Maps is deliberately provisioned in the `global` location as `maps-riyadh-mobility-riyadh-ud-uae-north`.

Confirm its health and active data path before sharing it:

```text
https://ca-rmd-api-riyadh-ud-ua-aesdq5.jollyplant-57daa6ab.uaenorth.azurecontainerapps.io/health
https://ca-rmd-api-riyadh-ud-ua-aesdq5.jollyplant-57daa6ab.uaenorth.azurecontainerapps.io/api/data-status
```

Use the local dashboard for development. Treat deployment and teardown as Azure-owner responsibilities because they can create or remove billable resources.

## Prerequisites

1. Install Azure CLI and Azure Developer CLI.
2. Run `az login`.
3. Run `azd auth login`.
4. Initialize an azd environment once with `azd init`.

## Deploy with the current azd environment

Run this helper script to show the active environment values before deployment:

```bash
bash scripts/deploy_azure.sh
```

To deploy the shared UAE North environment, select it and confirm its values first:

```bash
azd env select riyadh-ud-uae-north
azd env get-values
bash scripts/deploy_azure.sh uaenorth rg-riyadh-ud-uae-north
```

The script updates `AZURE_LOCATION` and `AZURE_RESOURCE_GROUP` only when you pass arguments, prints `azd env get-values`, and then runs `azd up`. Do not point the migration environment at a shared or unrelated resource group.

## Deployment Workflow

1. Reuse one resource group instead of creating new ones repeatedly.
2. Keep the same `azd` environment for the full demo cycle.
3. Run `azd env get-values` before each deploy so you can confirm the target resource group.
4. Use the deployed app for cloud smoke tests only, and do most iteration locally.
5. Keep all regional resources in UAE North; the `infra/modules/maps.bicep` module is the intentional exception and deploys Azure Maps in `global`.

## Migration record

The dashboard moved from `rg-riyadh-urban-hackathon-wus2` in West US 2 to `rg-riyadh-ud-uae-north` in UAE North. The UAE North deployment was checked at `/health` and `/api/data-status` before deletion of the West US 2 source group was submitted. The old Azure Maps account is removed with the West US 2 group; the replacement Maps account above is the global service retained for the dashboard.

## Spin down the whole resource group

When you are done testing, delete the current azd environment's resource group with the helper script:

```bash
bash scripts/destroy_resource_group.sh --yes
```

This is intentionally destructive and requires the explicit `--yes` flag.

## Manual equivalents

Deploy:

```bash
azd up
```

Delete the current resource group:

```bash
az group delete --name <resource-group-name> --yes --no-wait
```

## After deployment

1. Copy the `WEB_APP_URL` from `azd` output.
2. Open the deployed app in a browser.
3. Run the data scripts to upload processed files and seed Cosmos DB if you want Blob or Cosmos-backed mode.
