targetScope = 'resourceGroup'

param location string = resourceGroup().location
param envName string = 'dev'
param appName string = 'riyadh-mobility'
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param enableEventHubs bool = false

var suffix = uniqueString(resourceGroup().id, envName)
var storageName = 'striyadh${take(suffix, 15)}'
var cosmosName = 'cosmos-riyadh-mobility-${envName}'
var mapsName = 'maps-riyadh-mobility-${envName}'
var logName = 'log-riyadh-mobility-${envName}'
var appInsightsName = 'appi-riyadh-mobility-${envName}'
var containerEnvName = 'cae-riyadh-mobility-${envName}'
var containerAppName = 'ca-riyadh-mobility-api-${envName}'

module monitoring './modules/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    logAnalyticsName: logName
    appInsightsName: appInsightsName
  }
}

module storage './modules/storage.bicep' = {
  name: 'storage'
  params: {
    location: location
    storageAccountName: storageName
  }
}

module cosmos './modules/cosmos.bicep' = {
  name: 'cosmos'
  params: {
    location: location
    accountName: cosmosName
    databaseName: 'mobilitydb'
  }
}

module maps './modules/maps.bicep' = {
  name: 'maps'
  params: {
    location: location
    accountName: mapsName
  }
}

module containerApp './modules/container-app.bicep' = {
  name: 'containerApp'
  params: {
    location: location
    containerAppEnvironmentName: containerEnvName
    containerAppName: containerAppName
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsWorkspaceId
    logAnalyticsSharedKey: monitoring.outputs.logAnalyticsSharedKey
    appInsightsConnectionString: monitoring.outputs.appInsightsConnectionString
    containerImage: containerImage
    mapsKey: maps.outputs.primaryKey
    storageConnectionString: storage.outputs.connectionString
    cosmosEndpoint: cosmos.outputs.endpoint
    cosmosKey: cosmos.outputs.primaryKey
  }
}

module optionalEventHubs './modules/optional-eventhubs.bicep' = if (enableEventHubs) {
  name: 'optionalEventHubs'
  params: {
    location: location
    namespaceName: 'evhns-riyadh-${envName}'
  }
}

resource blobReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.outputs.storageAccountId, containerApp.outputs.principalId, 'blob-reader')
  scope: resourceId('Microsoft.Storage/storageAccounts', storageName)
  properties: {
    principalId: containerApp.outputs.principalId
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
    )
    principalType: 'ServicePrincipal'
  }
}

output WEB_APP_URL string = containerApp.outputs.url
output AZURE_MAPS_ACCOUNT_NAME string = mapsName
output STORAGE_ACCOUNT_NAME string = storageName
output COSMOS_DATABASE_NAME string = 'mobilitydb'
output RESOURCE_GROUP_NAME string = resourceGroup().name
