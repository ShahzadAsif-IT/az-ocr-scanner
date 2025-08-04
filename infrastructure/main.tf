# main.tf

terraform {
    required_providers {
        # azapi   = { 
        #     source  = "Azure/azapi"
        # }
        azurerm = {
            source = "hashicorp/azurerm"
            version = "=4.38.1"
        }
    }
}
# 1. Provider and basic setup
# provider "azapi" {
#     subscription_id = var.subscription_id
# }

provider "azurerm" {
    subscription_id = var.subscription_id
    features {}
}

# Resource Group
resource "azurerm_resource_group" "rg" {
    name     = var.resource_group_name
    location = var.azure_region
}

# 2. Storage Account (for form files and function triggers)
resource "azurerm_storage_account" "storage" {
    name                     = var.storage_account_name           # must be globally unique
    resource_group_name      = azurerm_resource_group.rg.name
    location                 = azurerm_resource_group.rg.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

# Create a blob container for the uploads
resource "azurerm_storage_container" "forms" {
    name                  = "forms"
    storage_account_id    = azurerm_storage_account.storage.id
    container_access_type = "private"
}

# 3. Cognitive Service for Computer Vision (Document Intelligence)
resource "azurerm_cognitive_account" "compvision" {
    name                = var.computer_vision_name
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    kind                = "ComputerVision"                    # Specify the service type
    sku_name            = "S1"                                # S0 is a common tier for Form Recognizer
}

# 4. Azure OpenAI Resource
resource "azurerm_cognitive_account" "openai" {
    name                = var.openai_account_name
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    kind                = "OpenAI"                            # Azure OpenAI service
    sku_name            = "S0"
}

# Deploy GPT-4 model within Azure OpenAI (if using Azure OpenAI)
resource "azurerm_cognitive_deployment" "gpt-4" {
    name                  = "gpt-4" # Name your deployment
    cognitive_account_id  = azurerm_cognitive_account.openai.id

    model {
        name    = "gpt-4"
        version = "turbo-2024-04-09"
        format  = "OpenAI"
    }

    sku {
        name = "Standard"
    }
    
    version_upgrade_option = "OnceNewDefaultVersionAvailable"
}

# # 5. Azure Function App for the Python code
# # Create an App Service plan for the Function (consumption plan)
# resource "azurerm_service_plan" "func_plan" {
#     name                = "${var.project_name}-func-plan"
#     resource_group_name = azurerm_resource_group.rg.name
#     location            = azurerm_resource_group.rg.location
#     os_type             = "Linux"
#     sku_name            = "Y1"   # Y1 is the SKU for Linux consumption plan (serverless)
# }

# # The Function App itself
# resource "azurerm_linux_function_app" "function" {
#     name                       = "${var.project_name}-function"
#     resource_group_name        = azurerm_resource_group.rg.name
#     location                   = azurerm_resource_group.rg.location
#     service_plan_id            = azurerm_service_plan.func_plan.id
#     storage_account_name       = azurerm_storage_account.storage.name
#     storage_account_access_key = azurerm_storage_account.storage.primary_access_key

#     app_settings = {
#         # App settings for our function – including keys (could also use Key Vault references)
#         "FUNCTIONS_WORKER_RUNTIME"     = "python",
#         "AzureWebJobsStorage"          = azurerm_storage_account.storage.primary_connection_string,
#         "DOCAI_ENDPOINT"               = azurerm_cognitive_account.compvision.endpoint,
#         "DOCAI_KEY"                    = azurerm_cognitive_account.compvision.primary_access_key,
#         "AZURE_OPENAI_ENDPOINT"        = azurerm_cognitive_account.openai.endpoint,
#         "AZURE_OPENAI_KEY"             = azurerm_cognitive_account.openai.primary_access_key,
#         "OPENAI_DEPLOYMENT_NAME"       = azurerm_cognitive_deployment.gpt4.name,
#         # ... other settings like environment config
#     }

#     identity { type = "SystemAssigned" }  # enable managed identity if needed for Key Vault or Cognitive access
  
#     site_config {
#     }
# }

# (Optional) Key Vault to store secrets instead of putting in app_settings directly
# resource "azurerm_key_vault" "kv" { ... }
# (Optional) Azure Cognitive Search for advanced RAG indexing
# resource "azurerm_search_service" "cog_search" { ... }

# Output the endpoints and keys (to use in the application or testing)
output "DOCAI_ENDPOINT" {
    value = azurerm_cognitive_account.compvision.endpoint
}
output "DOCAI_ENDPOINT_KEY" {
    value = azurerm_cognitive_account.compvision.primary_access_key
    sensitive = true
}
output "OPENAI_ENDPOINT" {
    value = azurerm_cognitive_account.openai.endpoint
}
output "OPENAI_ENDPOINT_KEY" {
    value = azurerm_cognitive_account.openai.primary_access_key
    sensitive = true
}
output "OPENAI_MODEL" {
    value = azurerm_cognitive_deployment.gpt-4.model[0].name
}
output "OPENAI_API_VERSION" {
    value = "2025-01-01-preview"
}
output "STORAGE_ACCOUNT_NAME" {
    value = azurerm_storage_account.storage.name
}
