---
title: "Automating Governance in Fabric Workspaces with PowerShell"
date: 2024-10-21T10:00:00-04:00
categories:
  - Fabric
tags:
  - PowerShell
  - Governance
---

{% raw %}<img src="/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/blog_image.jpeg" alt="">{% endraw %}

While scaling Fabric workloads in a production environment, I have had to deal with challenges around the governance of objects in a Fabric workspace. I have been thinking of Fabric workspaces as being similar to resource groups in Azure. It is important to enforce and monitor specific configurations for the objects created within them, especially as you open the environment up for 'citizen development'.

Traditionally, I have used tools like [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) to enforce/monitor governance on resources created in a resource group. I have used Azure Policy to check for things like ensuring resources are deployed to the approved regions and naming standards are followed on a resource type basis.

Fabric does not seem to have functionality like Azure Policy today. In search of an alternative, I found the [Microsoft Fabric REST API](https://learn.microsoft.com/en-us/rest/api/fabric/articles/using-fabric-apis) and in the [examples](https://learn.microsoft.com/en-us/rest/api/fabric/articles/using-fabric-apis#automation-examples), they mention governance as a use case. They say the API can be leveraged for; ‘Ensuring that authors adhere to best practices and organization rules while creating reports and semantic models is crucial. To do this, navigate to your workspace and perform a comprehensive analysis of report definitions to determine whether they align with the best practices established by your organization.’

To demonstrate the value of the API, I put together some [PowerShell scripts](https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell) and wrote them in an object-oriented fashion so you can leverage them for your use cases.

## The Use Case 🧑‍💻

In this example we are going to step through detecting when naming standards are not being followed on existing Lakehouses created in a Fabric workspace.

We are going to leverage an SPN for authentication and build a PowerShell wrapper on top of the API that is extendable. Fabric exposes a lot of endpoints to interact with over REST. I have not run into a case yet where I could perform an operation in the UI that I could not perform via the API. It seems very exhaustive, which is great!

For our use case, we will leverage the [List Lakehouses](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/list-lakehouses?tabs=HTTP) API endpoint to recursively list all the lakehouses in a workspace. Let’s jump into some PowerShell and see how we would implement this in practice!

## Authorization to Call the Fabric API 📞

The first thing we need to do is login as the SPN to authorize our API calls to Fabric. To follow the principal of least privilege, I would recommend assigning the SPN [‘viewer’](https://learn.microsoft.com/en-us/fabric/get-started/roles-workspaces#-workspace-roles) permissions at the workspace level.

Now that the SPN has viewer permissions to our workspace, the next step is to generate a JWT that can be passed to subsequent API calls to authorize the SPN. I have created a [Fabric Utilities](https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell/fabricutilities.ps1) class and in it, I have a login method that can be leveraged to generate the JWT.

```powershell
[void]Login([string]$clientId, [string]$tenantId, [string]$clientSecret){
    $this.clientId = $clientId
    $this.tenantId = $tenantId
    $this.clientSecret = $clientSecret
    $body = "grant_type=client_credentials&client_id=$clientId&client_secret=$clientSecret&resource=$($this.resourceUrl)"
    $response = Invoke-RestMethod -Method Post -Uri $this.apiUri -ContentType "application/x-www-form-urlencoded" -Body $body
    $this.token = $response.access_token
}
```

This method accepts three arguments:

1. The SPN client ID

2. The SPN client Secret

3. The tenant ID your Fabric workspace exists in

Effectively all we are doing in this login method is leveraging the PowerShell cmdlet [Invoke-RestMethod](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.4) to make an API call to login.microsoftonline.com to get a JWT back.

To call this login function, I created a script called [check-lakehouse-naming.ps1]( https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell/check-lakehouse-naming.ps1). Like mentioned earlier, these scripts have been built in an object-oriented fashion, so it becomes very easy to extend and build on top of the Fabric Utility class.

```powershell
[cmdletbinding(SupportsShouldProcess=$true)]
param(
    [Parameter(Mandatory=$true)]
    [PSCredential]$spCredential,
    [string]$tenantId,
    [string]$fabricWorkspaceId
)

. "$PSScriptRoot.\fabricutilities.ps1"

$fabricHelper = [FabricUtility]::new($fabricWorkspaceId)

$fabricHelper.Login($spCredential.GetNetworkCredential().UserName,$tenantId,$spCredential.GetNetworkCredential().Password)
```

Notice that I instantiate the FabricUtility class and call the login method passing through the previously mentioned three arguments. I am leveraging the [PSCredential Class](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.pscredential?view=powershellsdk-7.4.0) to allow you to pass through your client id and client secret in a secure fashion.

```powershell
.\check-lakehouse-naming.ps1 -tenantId "your-tenant-id" -fabricWorkspaceId "your-workspace-id"
```

After running this, you should see the following prompt asking for both your client ID and client secret.

[![script_credential_prompt](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/script_credential_prompt.png)](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/script_credential_prompt.png){:target="_blank"}

If all goes well, you will get a JWT back from the login method that can be leveraged for subsequent API calls. Let’s extend out the PowerShell script to get all Lakehouses in our workspace and validate they are named properly.

## Validating Lakehouse Names 👮

Now that we have code to authorize our SPN to call the Fabric API and we have built the scripts in an object-oriented fashion, this all becomes very easy to extend.

Leveraging the previously mentioned [List Lakehouses](https://learn.microsoft.com/en-us/rest/api/fabric/lakehouse/items/list-lakehouses?tabs=HTTP) endpoint, I have added a method to our Fabric Utilities class to list the lakehouses in our workspace.

```powershell
[string]GetLakeHouses([string]$workspaceGuid){
    $uri = "https://api.fabric.microsoft.com/v1/workspaces/{0}/lakehouses" -f $workspaceGuid
    return $this.ExecuteAPICall($uri,'Get')
}
```

To call this method requires a small update to our [check-lakehouse-naming.ps1](https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell/check-lakehouse-naming.ps1) script:

```powershell
[cmdletbinding(SupportsShouldProcess=$true)]
param(
    [Parameter(Mandatory=$true)]
    [PSCredential]$spCredential,
    [string]$tenantId,
    [string]$fabricWorkspaceId
)

. "$PSScriptRoot.\fabricutilities.ps1"

$fabricHelper = [FabricUtility]::new($fabricWorkspaceId)

$fabricHelper.Login($spCredential.GetNetworkCredential().UserName,$tenantId,$spCredential.GetNetworkCredential().Password)

$lakehouse = $fabricHelper.GetLakeHouses($fabricWorkspaceId)

$data = $lakehouse | ConvertFrom-Json

$data
```

Notice at the bottom of the script, we call the GetLakeHouses() method and pass through our workspace ID. Since I have a few existing lakehouses in my workspace, the output of the above script looks as follows:

[![get_lakehouses_raw](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/get_lakehouses_raw.png)](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/get_lakehouses_raw.png){:target="_blank"}

I can see a few of the lakehouses get returned in an object that we can parse later on in our script to check if the lakehouse name follows our standards.

For reference, here are the lakehouses in my workspace.

[![lakehouses_in_fabric](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/lakehouses_in_fabric.png)](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/lakehouses_in_fabric.png){:target="_blank"}

Now that we are pulling all the lakehouses in our workspace, let’s tie into that data variable containing all of them and check if they follow our naming standard. For demonstration purposes, I wrote the following regex statement: ^mycompany_lakehouse_(raw|enriched|enterprise)_[0-9]{2}$, to check the naming of the lakehouses.

In this example, any of the below example names would be valid:

- mycompany_lakehouse_raw_01

- mycompany_lakehouse_raw_02

- mycompany_lakehouse_enriched_01

- mycompany_lakehouse_enterprise_01

Extending the script with a foreach loop to check each of the lakehouse names will help close off the example:

```powershell
$pattern = '^mycompany_lakehouse_(raw|enriched|enterprise)_[0-9]{2}$'

$data.value | ForEach-Object {
    $displayName = $_.displayName
    if ($displayName -match $pattern) {
        Write-Output "$displayName follows the naming standard."
    } else {
        Write-Output "$displayName does NOT follow the naming standard."
    }
}
```

Depending on the names of the lakehouses created in your workspace, you will get an output similar to the following:

[![validate_lakehouse_names](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/validate_lakehouse_names.png)](/blog/assets/images/blog_images/automating-governance-in-fabric-workspaces-with-powershell/validate_lakehouse_names.png){:target="_blank"}

This output can be exported to a report for review and future remediation.

## Extending the Scripts

I think there are plenty of use cases that can be fulfilled via the Fabric API. As mentioned earlier, these scripts can be extended by adding a new method in the Fabric Utility class for the API you want to call. Once you add the API endpoint you need, you can build scripts on top of the [fabricutility](https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell/fabricutilities.ps1) similar to the [check-lakehouse-naming]( https://github.com/Schiiss/blog/tree/master/code/automating-governance-in-fabric-workspaces-with-powershell/check-lakehouse-naming.ps1) for your specific use case or governance scenario.

Feel free to leverage these scripts as templates! Thanks for reading 😀
