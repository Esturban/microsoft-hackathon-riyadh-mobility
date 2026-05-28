param location string
param accountName string
param databaseName string

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: accountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: []
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  name: '${cosmos.name}/${databaseName}'
  properties: {
    resource: {
      id: databaseName
    }
  }
}

resource routes 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  name: '${cosmos.name}/${databaseName}/routes'
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
  name: '${cosmos.name}/${databaseName}/districts'
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
  name: '${cosmos.name}/${databaseName}/events'
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
