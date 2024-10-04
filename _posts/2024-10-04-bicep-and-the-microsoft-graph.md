---
title: "Bicep and The Microsoft Graph 💪☁️"
date: 2024-10-04T6:00:00-04:00
categories:
  - IaC
tags:
  - Azure
  - Entra ID
  - Bicep
---

{% raw %}<img src="/blog/assets/images/blog_images/bicep-and-the-microsoft-graph/blog_image.jpg" alt="">{% endraw %}

I am a bit late to the party on this news, but I wanted to share Microsoft’s announcement on May 21st, 2024 around the public preview of Bicep supporting the creation of Microsoft Graph objects. Integration with the Microsoft Graph was always an area I thought Terraform had the upper hand on. Terraform has supported [Microsoft Graph integration](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/guides/microsoft-graph) for some time, and when scripting the creation of your environments in Azure, this is a really important feature. The ability to configure groups and access via code, alongside infrastructure creation, enables a repeatable and structured approach to managing security in the cloud.

## Supported Resources ☁️

As of writing this blog, the Microsoft Graph Bicep extension supports the following [resources](https://learn.microsoft.com/en-us/graph/templates/reference/overview?view=graph-bicep-1.0#supported-resources):

- [Applications](https://learn.microsoft.com/en-us/graph/templates/reference/applications?view=graph-bicep-1.0)

- [App role assignments](https://learn.microsoft.com/en-us/graph/templates/reference/approleassignedto?view=graph-bicep-1.0)

- [Federated identity credentials](https://learn.microsoft.com/en-us/graph/templates/reference/federatedidentitycredentials?view=graph-bicep-1.0)

- [Groups](https://learn.microsoft.com/en-us/graph/templates/reference/groups?view=graph-bicep-1.0)

- [OAuth2 permission grants (delegated permission grants)](https://learn.microsoft.com/en-us/graph/templates/reference/oauth2permissiongrants?view=graph-bicep-1.0)

- [Service principals](https://learn.microsoft.com/en-us/graph/templates/reference/serviceprincipals?view=graph-bicep-1.0)

Terraform supports the creation of quite a few more object types in the Graph, but I will say I have not used half of them. The primary objects I have created and managed in Terraform are groups, service principals, and applications. Bicep supports all of these today and I think will suffice for a majority of use cases out there.

## Microsoft Graph Bicep Extension in Practice 🤾‍♂️

I have created a few bicep files to test out the graph integration and [open-sourced]( https://github.com/Schiiss/blog/tree/master/code/bicep-and-the-microsoft-graph) the code. To enable the public preview of the Microsoft Graph extension, you must include the following in the bicepconfig.json file

```json
{
    "experimentalFeaturesEnabled": {
        "extensibility": true
    },
    "extensions": {
      "microsoftGraphV1_0": "br:mcr.microsoft.com/bicep/extensions/microsoftgraph/v1.0:0.1.8-preview"
    }
}
```

Now that we have enabled experimental features in Bicep, we can start deploying Graph resources using Bicep.

You will notice in my [main.bicep]( https://github.com/Schiiss/blog/tree/master/code/bicep-and-the-microsoft-graph/main.bicep) file, I have declared a [Microsoft.Graph/groups](https://learn.microsoft.com/en-us/graph/templates/reference/groups?view=graph-bicep-1.0) resource and passed through a few parameters to get a group created in Entra ID.

```bicep
extension microsoftGraph

resource group 'Microsoft.Graph/groups@v1.0' = {
  displayName: 'bicep-group'
  mailEnabled: false
  mailNickname: 'bicep-group'
  securityEnabled: true
  uniqueName: 'bicep-group'
}
```

I then reference the group’s object ID to assign it the RBAC Owner role on a new storage account.

```bicep
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
```

> **_NOTE:_**  You will notice in my bicep script where I deploy a storage account I am making reference to a remote module (ie: br/public:avm/res/storage/storage-account:0.9.1). This remote module is managed as apart of the [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/) project which is an amazing initiative 'to consolidate and set the standards for what a good Infrastructure-as-Code module looks like'. These templates make it very easy to deploy infrastructure with code and ensure you are following best practices. I highly recommend checking these out!

Jumping into Azure I can see the newly created storage account:

[![storage_account](/blog/assets/images/blog_images/bicep-and-the-microsoft-graph/storage_account_azure.png)](/blog/assets/images/blog_images/bicep-and-the-microsoft-graph/storage_account_azure.png){:target="_blank"}

And here is the RBAC assignment tab with the newly created 'bicep-group'

[![storage_account_azure_rbac](/blog/assets/images/blog_images/bicep-and-the-microsoft-graph/storage_account_azure_rbac.png)](/blog/assets/images/blog_images/bicep-and-the-microsoft-graph/storage_account_azure_rbac.png){:target="_blank"}

## Conclusion 🏁

Microsoft seems to be extending bicep through 'extensions' and it reminds me of [terraform providers](https://developer.hashicorp.com/terraform/language/providers). The key difference right now seems to be that these extensions are focused on the Azure stack. Bicep does not seem intended to be 'cross cloud' like Terraform, as stated in the 'non-goal' mentioned in the [README](https://github.com/Azure/bicep?tab=readme-ov-file#non-goals): 'Provide a first-class provider model for non-Azure related tasks. While we will likely introduce an extensibility model at some point, any extension points are intended to be focused on Azure infra or application deployment related tasks.'

I do not think this is a bad thing. Terraform gets a lot of attention for being 'cross cloud'. While it’s true that you can use the same 'language' to deploy across AWS and Azure, it's not as easy as pushing a button. You would need to retarget all your terraform scripts to point to the respective cloud provider (ie: azurerm and aws) for your scripts to be able to actually work 'cross cloud'.

I like that Bicep is focused on providing support for Azure/Microsoft resources instead of being a 'cross cloud' tool like Terraform and it will continue to be my first choice when selecting an IaC framework in the cloud!

Thanks for reading!
