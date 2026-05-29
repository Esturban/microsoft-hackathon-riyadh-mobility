param location string
param containerAppEnvironmentName string
param containerAppName string
param logAnalyticsWorkspaceId string
param logAnalyticsSharedKey string
param appInsightsConnectionString string
param containerImage string
param serviceName string
param mapsKey string
param storageConnectionString string
param cosmosEndpoint string
param cosmosKey string
param registryServer string
param registryUsername string
@secure()
param registryPassword string

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppEnvironmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspaceId
        sharedKey: logAnalyticsSharedKey
      }
    }
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  tags: {
    'azd-service-name': serviceName
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      registries: [
        {
          server: registryServer
          username: registryUsername
          passwordSecretRef: 'registry-password'
        }
      ]
      ingress: {
        external: true
        targetPort: 80
      }
      secrets: [
        {
          name: 'maps-key'
          value: mapsKey
        }
        {
          name: 'storage-connection'
          value: storageConnectionString
        }
        {
          name: 'cosmos-key'
          value: cosmosKey
        }
        {
          name: 'registry-password'
          value: registryPassword
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'web'
          image: containerImage
          env: [
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsightsConnectionString
            }
            {
              name: 'AZURE_MAPS_KEY'
              secretRef: 'maps-key'
            }
            {
              name: 'AZURE_STORAGE_CONNECTION_STRING'
              secretRef: 'storage-connection'
            }
            {
              name: 'COSMOS_ENDPOINT'
              value: cosmosEndpoint
            }
            {
              name: 'COSMOS_KEY'
              secretRef: 'cosmos-key'
            }
            {
              name: 'PORT'
              value: '80'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
    }
  }
}

output url string = app.properties.configuration.ingress.fqdn
output principalId string = app.identity.principalId
