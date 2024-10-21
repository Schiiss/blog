class FabricUtility{
    [string]$workspaceId
    [string]$token
    hidden [string] $clientId
    hidden [string] $tenantId
    hidden [string] $clientSecret
    [string]$apiUri="https://login.microsoftonline.com/$tenantId/oauth2/token"
    [string]$resourceUrl = "https://api.fabric.microsoft.com"


    FabricUtility([string]$workspaceGuid){
        $this.workspaceId = $workspaceGuid
    }

    [void]Login([string]$clientId, [string]$tenantId, [string]$clientSecret){
        $this.clientId = $clientId
        $this.tenantId = $tenantId
        $this.clientSecret = $clientSecret
        $body = "grant_type=client_credentials&client_id=$clientId&client_secret=$clientSecret&resource=$($this.resourceUrl)"
        $response = Invoke-RestMethod -Method Post -Uri $this.apiUri -ContentType "application/x-www-form-urlencoded" -Body $body
        $this.token = $response.access_token
    }

    [void]Login([string]$token){
        $this.token = $token
    }

    [object]GetHeaders(){
        $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
        $headers.Add("Authorization", "Bearer {0}" -f $this.token)
        $headers.Add("x-ms-version","2018-11-09")
        return $headers
    }

    [object]ExecuteAPICall([string]$uri,[string]$method){
        $response = Invoke-WebRequest -Method $method -Uri $uri -Headers $this.GetHeaders() -Verbose
        Write-Verbose ("RESPONSE: {0}" -f $response)
        return $response
    }

    [string]GetLakeHouses([string]$workspaceGuid){
        $uri = "https://api.fabric.microsoft.com/v1/workspaces/{0}/lakehouses" -f $workspaceGuid
        return $this.ExecuteAPICall($uri,'Get')
    }
}