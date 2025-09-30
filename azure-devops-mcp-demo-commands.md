# Azure DevOps MCP - Working Commands for Demo

*Tested on July 14, 2025 with the public project "Test MCP Server ADO"*

## Setup

- Organization: `ssguotti`
- Project: `Test MCP Server ADO`
- Repository ID: `1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7`

## ✅ Working Commands

### Repository Management

**List project repositories**
```json
{
  "command": "mcp_ado_repo_list_repos_by_project",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

**Get repository details**
```json
{
  "command": "mcp_ado_repo_get_repo_by_name_or_id",
  "parameters": {
    "project": "Test MCP Server ADO",
    "repositoryNameOrId": "Test MCP Server ADO"
  }
}
```

**List repository branches**
```json
{
  "command": "mcp_ado_repo_list_branches_by_repo",
  "parameters": {
    "repositoryId": "1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7",
    "top": 20
  }
}
```

**Get branch details**
```json
{
  "command": "mcp_ado_repo_get_branch_by_name",
  "parameters": {
    "repositoryId": "1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7",
    "branchName": "main"
  }
}
```

### Work Item Types (Schema)

**Work Item Type "Bug" schema**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Bug"
  }
}
```

**Work Item Type "Task" schema**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Task"
  }
}
```

**Work Item Type "Epic" schema**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Epic"
  }
}
```

### Build & Release

**List build definitions**
```json
{
  "command": "mcp_ado_build_get_definitions",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

**List release definitions**
```json
{
  "command": "mcp_ado_release_get_definitions",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

### Wiki

**List project wikis**
```json
{
  "command": "mcp_ado_wiki_list_wikis",
  "parameters": {
    "project": "Test MCP Server ADO"
  }
}
```

### Projects

**List accessible projects**
```json
{
  "command": "mcp_ado_core_list_projects",
  "parameters": {
    "top": 10,
    "stateFilter": "wellFormed"
  }
}
```

---

*Only tested and working commands, ready for your demo (July 14, 2025)*

*Tested on July 14, 2025 with the public project "Test MCP Server ADO"*
## Setup

- Organization: `ssguotti`
- Project: `Test MCP Server ADO`
- Repository ID: `1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7`
## ✅ Working Commands

### 📁 Repository Management
**List project repositories**
```json
{
**Get repository details**
```json
{
**List repository branches**
```json
{
**Get branch details**
```json
{
### 🏷️ Work Item Types (Schema)

**Work Item Type "Bug" schema**
**Work Item Type "Task" schema**
```json
{
**Work Item Type "Epic" schema**
```json
{
### 🔧 Build & Release

**List build definitions**
**List release definitions**
```json
{
### 📚 Wiki

**List project wikis**
### 🔍 Projects

**List accessible projects**
---

*Only tested and working commands, ready for your demo (July 14, 2025)*
# Azure DevOps MCP - Comandi Funzionanti per Demo

*Testato il 14 Luglio 2025 sul progetto pubblico "Test MCP Server ADO"*

## Setup

- Organization: `ssguotti`
- Project: `Test MCP Server ADO`
- Repository ID: `1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7`

## Comandi Funzionanti

### Repository

**Lista repository del progetto**
```json
{
  "command": "mcp_ado_repo_list_repos_by_project",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

**Dettagli repository**
```json
{
  "command": "mcp_ado_repo_get_repo_by_name_or_id",
  "parameters": {
    "project": "Test MCP Server ADO",
    "repositoryNameOrId": "Test MCP Server ADO"
  }
}
```

**Lista branch del repository**
```json
{
  "command": "mcp_ado_repo_list_branches_by_repo",
  "parameters": {
    "repositoryId": "1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7",
    "top": 20
  }
}
```

**Dettagli branch**
```json
{
  "command": "mcp_ado_repo_get_branch_by_name",
  "parameters": {
    "repositoryId": "1c7a2ebf-7551-4c89-bcfd-8b3c83aa56f7",
    "branchName": "main"
  }
}
```

### Work Item Types (Schema)

**Schema "Bug"**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Bug"
  }
}
```

**Schema "Task"**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Task"
  }
}
```

**Schema "Epic"**
```json
{
  "command": "mcp_ado_wit_get_work_item_type",
  "parameters": {
    "project": "Test MCP Server ADO",
    "workItemType": "Epic"
  }
}
```

### Build & Release

**Lista build definitions**
```json
{
  "command": "mcp_ado_build_get_definitions",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

**Lista release definitions**
```json
{
  "command": "mcp_ado_release_get_definitions",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

### Wiki

**Lista wiki del progetto**
```json
{
  "command": "mcp_ado_wiki_list_wikis",
  "parameters": {
    "project": "Test MCP Server ADO"
  }
}
```

### Progetti

**Lista progetti accessibili**
```json
{
  "command": "mcp_ado_core_list_projects",
  "parameters": {
    "top": 10,
    "stateFilter": "wellFormed"
  }
}
```

---

*Solo comandi testati e funzionanti, pronti per la demo (14 Luglio 2025)*
