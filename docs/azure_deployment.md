# Azure Deployment

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

You can also set the location and resource group in the same command:

```bash
bash scripts/deploy_azure.sh eastus rg-riyadh-ud-eastus
```

The script updates `AZURE_LOCATION` and `AZURE_RESOURCE_GROUP` when you pass arguments, prints `azd env get-values`, and then runs `azd up`.

## Deployment Workflow

1. Reuse one resource group instead of creating new ones repeatedly.
2. Keep the same `azd` environment for the full demo cycle.
3. Run `azd env get-values` before each deploy so you can confirm the target resource group.
4. Use the deployed app for cloud smoke tests only, and do most iteration locally.

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
