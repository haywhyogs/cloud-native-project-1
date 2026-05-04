variable "location" {
  description = "Azure region"
  default     = "canadacentral"
}

variable "resource_group_name" {
  description = "Resource group name"
  default     = "monitoring-rg"
}
variable "vm_name" {
  type        = string
  description = "Name of the VM"
  default     = "monitoring-vm"
}

variable "admin_username" {
  type        = string
  default     = "azureuser"
}
variable "vm_size" {
  default = "Standard_D2s_v3"
}
variable "app_ports" {
  description = "Ports for application containers"
  default     = ["5000", "5001", "5002", "5003"]
}