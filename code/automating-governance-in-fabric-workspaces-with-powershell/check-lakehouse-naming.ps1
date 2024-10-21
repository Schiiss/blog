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

$pattern = '^mycompany_lakehouse_(raw|enriched|enterprise)_[0-9]{2}$'

$data.value | ForEach-Object {
    $displayName = $_.displayName
    if ($displayName -match $pattern) {
        Write-Output "$displayName follows the naming standard."
    } else {
        Write-Output "$displayName does NOT follow the naming standard."
    }
}