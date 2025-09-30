# Work Item Details Command

To retrieve details about a specific work item using MCP, you can use the following command:

## Get Work Item Details

```json
{
  "command": "mcp_ado_wit_get_work_item",
  "parameters": {
    "project": "Test MCP Server ADO",
    "id": 123
  }
}
```

Or using NPX:

```
npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_get_work_item --project "Test MCP Server ADO" --id 123
```

### Additional Parameters

The command supports these optional parameters:
- `fields`: Array of specific field names to retrieve
- `expand`: Options include 'all', 'fields', 'links', 'none', and 'relations'
- `asOf`: Retrieve the work item as it was at a specific date/time

### Example with Optional Parameters

```json
{
  "command": "mcp_ado_wit_get_work_item",
  "parameters": {
    "project": "Test MCP Server ADO",
    "id": 123,
    "fields": ["System.Title", "System.Description", "System.State"],
    "expand": "fields"
  }
}
```

### Note on Permissions

This command requires appropriate permissions to view the requested work item. In our test environment with the public project "Test MCP Server ADO", we received an authorization error indicating the current user doesn't have access to work items.

```
TF400813: The user '03174c70-c2d6-69fb-b03b-1c5b24ecb7fd' is not authorized to access this resource.
```

For your production environment, ensure your PAT or other authentication method has sufficient permissions to read work items and that it includes the 'Work Items (Read)' scope.

# My Work Items Command

To retrieve work items assigned to or created by the current user, you can use the following command:

## Get My Work Items

```json
{
  "command": "mcp_ado_wit_my_work_items",
  "parameters": {
    "project": "Test MCP Server ADO"
  }
}
```

Or using NPX:

```
npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_my_work_items --project "Test MCP Server ADO"
```

### Additional Parameters

The command supports these optional parameters:
- `type`: Type of work items to retrieve. Options are 'assignedtome' (default) or 'myactivity'
- `top`: Maximum number of work items to return (default is 50)
- `includeCompleted`: Whether to include completed work items (default is false)

### Example with Optional Parameters

```json
{
  "command": "mcp_ado_wit_my_work_items",
  "parameters": {
    "project": "Test MCP Server ADO",
    "type": "myactivity",
    "top": 10,
    "includeCompleted": true
  }
}
```

### Note on Permissions

This command requires appropriate permissions to view work items. In our test environment with the public project "Test MCP Server ADO", we received an authorization error indicating the current user doesn't have access to work items:

```
TF400813: The user '03174c70-c2d6-69fb-b03b-1c5b24ecb7fd' is not authorized to access this resource.
```

For your production environment, ensure your PAT or other authentication method has sufficient permissions to read work items and that it includes the 'Work Items (Read)' scope.

# Working with My Work Items in PowerShell

Here's how you can use the `mcp_ado_wit_my_work_items` command in a PowerShell script to retrieve and process your work items:

```powershell
# Execute MCP command to get my work items and convert the result to JSON
$workItems = npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_my_work_items --project "Your Project Name" --top 20 --type assignedtome | ConvertFrom-Json

# Check if we have work items
if ($workItems -and $workItems.Count -gt 0) {
    Write-Host "Found $($workItems.Count) work items assigned to me:"
    
    # Process each work item
    foreach ($item in $workItems) {
        Write-Host "ID: $($item.id) - Title: $($item.fields.'System.Title') - State: $($item.fields.'System.State')"
    }
    
    # Filter to only active items
    $activeItems = $workItems | Where-Object { $_.fields.'System.State' -eq 'Active' }
    Write-Host "Found $($activeItems.Count) active work items"
    
    # Get most recently updated item
    $mostRecent = $workItems | Sort-Object { $_.fields.'System.ChangedDate' } -Descending | Select-Object -First 1
    Write-Host "Most recently updated: $($mostRecent.fields.'System.Title')"
} else {
    Write-Host "No work items found or you don't have permission to access them"
}
```

### Error Handling Example

Here's how you can handle the authorization error we encountered:

```powershell
try {
    $result = npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_my_work_items --project "Test MCP Server ADO" 2>&1
    
    # Check if the result contains an error message
    if ($result -match "TF400813") {
        Write-Host "Authorization error: You don't have permission to access work items in this project"
        Write-Host "Please check your PAT and ensure it has 'Work Items (Read)' scope"
    } else {
        # Process successful result
        $workItems = $result | ConvertFrom-Json
        Write-Host "Successfully retrieved $($workItems.Count) work items"
    }
} catch {
    Write-Host "An error occurred: $_"
}
```

This script shows how to:
1. Call the MCP command with parameters
2. Process the returned work items
3. Filter and sort the results
4. Handle potential authorization errors

Remember to replace "Your Project Name" with your actual Azure DevOps project name.

# Work Items Batch Retrieval Command

To retrieve multiple work items in a single API call, you can use the batch retrieval command:

## Get Work Items Batch by IDs

```json
{
  "command": "mcp_ado_wit_get_work_items_batch_by_ids",
  "parameters": {
    "project": "Test MCP Server ADO",
    "ids": [1, 2, 3, 4, 5]
  }
}
```

Or using NPX:

```
npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_get_work_items_batch_by_ids --project "Test MCP Server ADO" --ids "[1, 2, 3, 4, 5]"
```

### Benefits of Batch Retrieval

- **Efficiency**: Fetch multiple work items in a single API call
- **Reduced Overhead**: Minimize network latency compared to multiple individual calls
- **Consistent State**: All work items are retrieved at the same point in time
- **Performance**: Better performance when retrieving large numbers of work items

### Response Format

The response contains an array of work items, each with its fields, relationships, and links. For work items that don't exist or the user doesn't have access to, the corresponding array element will be null.

### Note on Permissions

This command requires appropriate permissions to view the requested work items. In our test environment with the public project "Test MCP Server ADO", authorization is limited, resulting in null responses for work items.

For your production environment, ensure your PAT or other authentication method has sufficient permissions to read work items and includes the 'Work Items (Read)' scope.

# Real-World Example: Retrieving Work Item #180

Here's an example of retrieving a specific work item (ID: 180) from the "Test MCP Server ADO" project:

```json
{
  "command": "mcp_ado_wit_get_work_item",
  "parameters": {
    "project": "Test MCP Server ADO",
    "id": 180
  }
}
```

Using NPX:

```
npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_get_work_item --project "Test MCP Server ADO" --id 180
```

## Sample Response

The command returns detailed information about the work item:

```json
{
  "id": 180,
  "rev": 2,
  "fields": {
    "System.AreaPath": "Test MCP Server ADO",
    "System.TeamProject": "Test MCP Server ADO",
    "System.IterationPath": "Test MCP Server ADO",
    "System.WorkItemType": "Bug",
    "System.State": "New",
    "System.Reason": "New defect reported",
    "System.AssignedTo": {
      "displayName": "Stefano Sguotti"
      // Additional user details omitted for brevity
    },
    "System.CreatedDate": "2025-07-14T20:14:46.157Z",
    "System.ChangedDate": "2025-07-14T21:08:52.047Z",
    "System.Title": "test MCP Server",
    "System.BoardColumn": "New",
    "System.BoardColumnDone": false,
    "Microsoft.VSTS.Common.Priority": 2,
    "Microsoft.VSTS.Common.Severity": "3 - Medium",
    "Microsoft.VSTS.Common.ValueArea": "Business",
    "Microsoft.VSTS.TCM.SystemInfo": "<div>test MCP Server<br> </div>"
  }
  // Additional fields omitted for brevity
}
```

## Extracting Key Information with PowerShell

Here's how you could extract and display key information from this work item using PowerShell:

```powershell
# Execute command and convert to PowerShell object
$workItem = npx mcp --service-url "https://azmcpdfasint.azurewebsites.net" mcp_ado_wit_get_work_item --project "Test MCP Server ADO" --id 180 | ConvertFrom-Json

# Display key information
Write-Host "Work Item #$($workItem.id)"
Write-Host "Title: $($workItem.fields.'System.Title')"
Write-Host "Type: $($workItem.fields.'System.WorkItemType')"
Write-Host "State: $($workItem.fields.'System.State')"
Write-Host "Assigned To: $($workItem.fields.'System.AssignedTo'.displayName)"
Write-Host "Created: $($workItem.fields.'System.CreatedDate')"
Write-Host "Priority: $($workItem.fields.'Microsoft.VSTS.Common.Priority')"
Write-Host "Severity: $($workItem.fields.'Microsoft.VSTS.Common.Severity')"
Write-Host "Area Path: $($workItem.fields.'System.AreaPath')"
Write-Host "Iteration Path: $($workItem.fields.'System.IterationPath')"
```

This example demonstrates:
1. How to retrieve a specific work item by ID
2. The structure of a real work item response
3. How to extract and use key fields from the response
