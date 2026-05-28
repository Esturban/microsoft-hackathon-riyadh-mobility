# Agent Build Notes

## Sources reviewed

- Azure Maps Code Samples: GeoJSON layers, popups, and control patterns
- Azure Container Apps overview: single-container hosting model
- Azure Blob Storage overview: raw and processed file storage path
- Azure Cosmos DB overview: summary-document storage model
- Azure Event Hubs overview: stretch-path event ingestion
- Azure Stream Analytics overview: optional event aggregation
- Azure Developer CLI overview: `azd up` deployment flow
- Azure Bicep overview: infra-as-code structure

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
