terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  required_version = ">= 1.3.0"

  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "tfstate3678"
    container_name       = "tfstate"
    key                  = "cloudmonitor/terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
