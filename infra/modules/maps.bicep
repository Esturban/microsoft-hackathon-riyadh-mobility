param location string
param accountName string

resource maps 'Microsoft.Maps/accounts@2023-06-01' = {
  name: accountName
  location: location
  sku: {
    name: 'G2'
  }
  kind: 'Gen2'
}

output primaryKey string = listKeys(maps.id, maps.apiVersion).primaryKey
