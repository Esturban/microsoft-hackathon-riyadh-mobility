targetScope = 'resourceGroup'

param location string = resourceGroup().location
param envName string = 'dev'
param appName string = 'riyadh-mobility'
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param enableEventHubs bool = false

var suffix = uniqueString(resourceGroup().id, envName)
var storageName = 'striyadh${take(suffix, 15)}'
var cosmosName = 'cosmos-riyadh-${envName}'
var mapsName = 'maps-riyadh-${envName}'
var logName = 'log-riyadh-${envName}'
var appInsightsName = 'appi-riyadh-${envName}'
var containerEnvName = 'cae-riyadh-${envName}'
var containerAppName = 'ca-riyadh-api-${envName}'

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

output containerAppUrl string = containerApp.outputs.url
output storageAccountName string = storageName
output cosmosEndpoint string = cosmos.outputs.endpoint
