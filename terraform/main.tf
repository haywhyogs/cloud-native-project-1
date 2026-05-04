resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "monitoring-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_subnet" "subnet" {
  name                 = "monitoring-subnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "pip" {
  name                = "monitoring-pip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_security_group" "nsg" {
  name                = "monitoring-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name
}
resource "azurerm_network_security_rule" "allow_ssh" {
  name                        = "allow-ssh"              
  priority                    = 100                      
  direction                   = "Inbound"                
  access                      = "Allow"                  
  protocol                    = "Tcp"                    
  source_port_range           = "*"                      
  destination_port_ranges     = ["22"]                   
  source_address_prefix       = "*"                      
  destination_address_prefix  = "*"                      
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.nsg.name
}
resource "azurerm_network_security_rule" "allow_app" {
  name                        = "allow-app-ports"        
  priority                    = 200                      
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_ranges     = var.app_ports  
  source_address_prefix       = "*"                      
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.nsg.name
}
resource "azurerm_subnet_network_security_group_association" "nsg_assoc" {
  subnet_id                 = azurerm_subnet.subnet.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}
resource "azurerm_network_interface" "nic" {
  name                = "monitoring-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "internal"                     
    subnet_id                     = azurerm_subnet.subnet.id       
    private_ip_address_allocation = "Dynamic"                      
    public_ip_address_id          = azurerm_public_ip.pip.id       
  }
}
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  resource_group_name = var.resource_group_name
  location            = var.location
  size                = var.vm_size         
  admin_username      = var.admin_username              

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  admin_ssh_key {
    username   = var.admin_username                     
    public_key = file("~/.ssh/id_rsa.pub")       
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
  
}

