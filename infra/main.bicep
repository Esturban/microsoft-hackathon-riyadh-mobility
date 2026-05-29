targetScope = 'resourceGroup'

param location string = resourceGroup().location
param envName string = 'dev'
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param enableEventHubs bool = false

var envSlug = toLower(replace(envName, '_', '-'))
var suffix = uniqueString(resourceGroup().id, envName)
var storageName = 'striyadh${take(suffix, 15)}'
var cosmosName = 'cosmos-riyadh-mobility-${envSlug}'
var mapsName = 'maps-riyadh-mobility-${envSlug}'
var logName = 'log-riyadh-mobility-${envSlug}'
var appInsightsName = 'appi-riyadh-mobility-${envSlug}'
var containerEnvName = 'cae-riyadh-mobility-${envSlug}'
var shortEnvSlug = take(envSlug, 12)
var shortSuffix = take(suffix, 6)
var containerAppName = 'ca-rmd-api-${shortEnvSlug}-${shortSuffix}'

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
    namespaceName: 'evhns-riyadh-${envSlug}'
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' existing = {
  name: storageName
}

resource blobReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageName, containerAppName, 'blob-reader')
  scope: storageAccount
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
