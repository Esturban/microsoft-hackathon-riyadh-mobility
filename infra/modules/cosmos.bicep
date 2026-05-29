param location string
param accountName string
param databaseName string

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: accountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  name: databaseName
  parent: cosmos
  properties: {
    resource: {
      id: databaseName
    }
  }
}

resource routes 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  name: 'routes'
  parent: database
  dependsOn: [
    database
  ]
  properties: {
    resource: {
      id: 'routes'
      partitionKey: {
        paths: ['/type']
        kind: 'Hash'
      }
    }
  }
}

resource districts 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  name: 'districts'
  parent: database
  dependsOn: [
    database
  ]
  properties: {
    resource: {
      id: 'districts'
      partitionKey: {
        paths: ['/districtId']
        kind: 'Hash'
      }
    }
  }
}

resource events 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  name: 'events'
  parent: database
  dependsOn: [
    database
  ]
  properties: {
    resource: {
      id: 'events'
      partitionKey: {
        paths: ['/routeId']
        kind: 'Hash'
      }
    }
  }
}

output endpoint string = cosmos.properties.documentEndpoint
output primaryKey string = listKeys(cosmos.id, cosmos.apiVersion).primaryMasterKey
