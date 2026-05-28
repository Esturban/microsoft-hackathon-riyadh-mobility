# Agent Build Notes

## Phase 0 scope restatement

- Repo target: `riyadh-mobility-intelligence-dashboard`
- Required Azure services: Container Apps, Azure Maps, Blob Storage, Cosmos DB, Log Analytics, Application Insights, `azd`, and Bicep
- Local/sample fallback: required, with bundled sample GeoJSON and JSON
- No Kubernetes: kept out of scope
- No production ML: kept out of scope

## Sources reviewed

- Azure Maps Code Samples: GeoJSON layers, popups, and control patterns
  - https://github.com/Azure-Samples/AzureMapsCodeSamples
- Azure Container Apps overview: single-container hosting model
  - https://learn.microsoft.com/en-us/azure/container-apps/overview
- Azure Blob Storage overview: raw and processed file storage path
  - https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction
- Azure Cosmos DB overview: summary-document storage model
  - https://learn.microsoft.com/en-us/azure/cosmos-db/overview
- Azure Event Hubs overview: stretch-path event ingestion
  - https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about
- Azure Stream Analytics overview: optional event aggregation
  - https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction
- Azure Developer CLI overview: `azd up` deployment flow
  - https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview
- Azure Bicep overview: infra-as-code structure
  - https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview

## Patterns reused

- Thin FastAPI API plus static frontend hosting
- GeoJSON line and point layers with popups
- Blob-first file loading with sample fallback
- Cosmos summary documents for routes, districts, and events
- One resource group deployment shape for Container Apps, Storage, Cosmos, Maps, and monitoring

## Intentionally not included

- Kubernetes or AKS
- Authentication system
- Production ML or CCTV integration
- Heavy frontend framework complexity
- Hard dependency on live public endpoints at runtime
