extension microsoftGraph

resource group 'Microsoft.Graph/groups@v1.0' = {
  displayName: 'bicep-group'
  mailEnabled: false
  mailNickname: 'bicep-group'
  securityEnabled: true
  uniqueName: 'bicep-group'
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.9.1' = {
  name: 'storageAccountDeployment'
  params: {
    name: 'bicepandthegraph'
    kind: 'BlobStorage'
    location: 'East US'
    skuName: 'Standard_LRS'
    roleAssignments: [
      {
        principalId: group.id
        principalType: 'Group'
        roleDefinitionIdOrName: 'Owner'
      }
    ]
  }
}
