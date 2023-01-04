#initial backend of the terraform
#define resource group

resource "azurerm_resource_group" "rgdeploy" {
  name     = var.azure_resource_group_name
  location = var.azure_resource_group_location
}

#create Azure Data Lake storage account for this deployment
resource "azurerm_storage_account" "storagedeploy" {
  name                = var.azure_storage_account_name
  resource_group_name = azurerm_resource_group.rgdeploy.name
  location            = azurerm_resource_group.rgdeploy.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"

}

#creating synapse folder under the deployment storage account
resource "azurerm_storage_data_lake_gen2_filesystem" "fsdeploy" {
  name               = var.azure_storage_date_lake_file_system
  storage_account_id = azurerm_storage_account.storagedeploy.id
}

#create azurebilling folder
resource "azurerm_storage_data_lake_gen2_filesystem" "fsdeployazurebilling" {
  name               = var.azure_storage_date_lake_file_system_azure_billing
  storage_account_id = azurerm_storage_account.storagedeploy.id
}

#create hetzner billing
resource "azurerm_storage_data_lake_gen2_filesystem" "fsdeployhetznerbilling" {
  name               = var.azure_storage_date_lake_file_system_hetzner_billing
  storage_account_id = azurerm_storage_account.storagedeploy.id
}

#create synapse notebook
resource "azurerm_synapse_workspace" "senecnotebookdeploy" {
  name                                 = var.azure_synapse_workspace_name
  resource_group_name                  = azurerm_resource_group.rgdeploy.name
  location                             = azurerm_resource_group.rgdeploy.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.fsdeploy.id
  sql_administrator_login              = "sqladmin"
  sql_administrator_login_password     = "test@me210"
  depends_on                           = [azurerm_storage_account.storagedeploy]

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "deployment"
    source      = "terraform"
  }

}

#create synapse spark pool which is associated with the notebook
resource "azurerm_synapse_spark_pool" "senecsparkpooldeployment" {
  name                 = var.azure_synapse_spark_pool_deployment
  synapse_workspace_id = azurerm_synapse_workspace.senecnotebookdeploy.id
  node_size_family     = "MemoryOptimized"
  node_size            = "Small"
  cache_size           = 100

  auto_scale {
    max_node_count = 50
    min_node_count = 3
  }

  auto_pause {
    delay_in_minutes = 15
  }


  tags = {
    ENV = "Production"
  }
}

#set firewall rule for this notebook
resource "azurerm_synapse_firewall_rule" "senecfirewall" {
  name                 = "AllowAll"
  synapse_workspace_id = azurerm_synapse_workspace.senecnotebookdeploy.id
  start_ip_address     = "0.0.0.0"
  end_ip_address       = "255.255.255.255"
}

data "azurerm_client_config" "current" {}

#role assignments for all the assets

resource "azurerm_role_assignment" "adf_storage_ra" {
  scope                = azurerm_storage_account.storagedeploy.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}