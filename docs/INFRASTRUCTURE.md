
# 🏗️ Infrastructure — Terraform, VM, and Cloud Initialization

This document covers the full infrastructure setup for the monitoring service,
including Terraform, remote state, cloud-init VM bootstrap, and Managed Identity.

All infrastructure is defined as code and fully reproducible from scratch.

---

## 📌 Overview

The infrastructure is split into key concerns:

| Concern | Tool | What it does |
|---------|------|-------------|
| Cloud resources | Terraform | Provisions VM, networking, NSG, identity, role assignment |
| VM configuration | cloud-init | Installs Docker, writes compose file, starts containers |
| State management | Azure Blob Storage | Stores Terraform state remotely |
| Authentication | Managed Identity | VM authenticates to ACR without credentials |

> Even with full automation, this remains an **IaaS model** — the OS, runtime,
> and container lifecycle are explicitly managed.

---

## 🧱 Infrastructure Components

| Resource | Purpose |
|----------|--------|
| Resource Group | Logical container |
| Virtual Network | Isolated network |
| Subnet | VM segment |
| NSG | Firewall rules |
| Public IP | External access |
| NIC | Network interface |
| VM | Runs containers |
| Managed Identity | Secure ACR access |
| Role Assignment | Grants AcrPull |

---

## 🌐 Networking Architecture

```

Internet → Public IP → NIC → Subnet → NSG → VM → Docker Containers

```

### Key Principles

- NSG controls ALL inbound traffic  
- Opening a port ≠ application listening  
- Separate rules:
  - SSH → 22  
  - App → 5000–5002  

Priority example:

```

100 → SSH
200 → App traffic

```

---

## 🏗️ Terraform

---

### File Structure

```

terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
└── cloud-init.yml

````

---

### Provider + Backend Configuration

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

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
````

---

### VM Resource (Managed Identity + cloud-init)

```hcl
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  size                = var.vm_size
  admin_username      = var.admin_username

  custom_data = base64encode(file("${path.module}/cloud-init.yml"))

  identity {
    type = "SystemAssigned"
  }

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.ssh_public_key_path)
  }

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]
}
```

⚠️ Important:

```
Use base64encode(file()) instead of filebase64() on Windows/WSL
```

---

### ACR Role Assignment (Least Privilege)

```hcl
data "azurerm_container_registry" "acr" {
  name                = "monitoringacr3678"
  resource_group_name = var.acr_resource_group
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = data.azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_virtual_machine.vm.identity[0].principal_id
}
```

**Why `data`:**

* ACR already exists
* Terraform reads it, does not manage it

---

### NSG Rules

```hcl
resource "azurerm_network_security_rule" "allow_ssh" {
  priority = 100
  destination_port_range = "22"
}

resource "azurerm_network_security_rule" "allow_app" {
  priority = 200
  destination_port_range = "5000-5003"
}
```

---

### Terraform Commands

```bash
terraform init
terraform plan
terraform apply
terraform destroy

terraform state list

terraform taint azurerm_linux_virtual_machine.vm
terraform apply

terraform init -reconfigure
```

---

### Terraform Behavior Insights

* Terraform manages infrastructure, NOT runtime
* Does not generate SSH keys
* Injects public key into VM

```
Private key → local  
Public key → VM
```

---

### Variables Strategy

Use variables if:

* Environment-specific
* Reused
* Likely to change
* Sensitive

---

## 📦 Remote State

---

### Why Remote State

* Prevents drift
* Enables collaboration
* Required for CI/CD

---

### Setup (Before `terraform init`)

```bash
az group create --name rg-tfstate --location uksouth

az storage account create \
  --name tfstate3678 \
  --resource-group rg-tfstate \
  --sku Standard_LRS

az storage container create \
  --name tfstate \
  --account-name tfstate3678
```

---

### Verify State

```bash
terraform state list

az storage blob list \
  --container-name tfstate \
  --account-name tfstate3678 \
  --output table
```

---

### .gitignore

```
*.tfstate
*.tfstate.*
.terraform/

# KEEP
.terraform.lock.hcl
```

---

## 🖥️ VM + Docker Setup (Reference)

```bash
az vm create ...

ssh azureuser@<ip>

sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io

sudo systemctl enable docker
sudo systemctl start docker
```

---

## ⚙️ cloud-init

---

### What It Does

```
Terraform → VM → boot → cloud-init → installs + configures everything
```

---

### Execution Order

```
1. packages
2. write_files
3. runcmd
```

---

### Final cloud-init.yml

```yaml
#cloud-config
package_update: true

write_files:
  - path: /home/azureuser/docker-compose.yml
    content: |
      services:
        web1:
          image: monitoringacr3678.azurecr.io/monitoring-app:latest
          ports:
            - "5000:80"
```

---

### Critical Rules

* Must start with `#cloud-config`
* Spaces only (no tabs)
* Validate YAML
* Do not set ownership in write_files

---

### Debugging

```bash
sudo cat /var/log/cloud-init-output.log | tail -50
sudo cat /var/log/cloud-init.log | tail -50

cat -A cloud-init.yml
ls -la /home/azureuser/
```

---

## 🔐 Managed Identity

---

### What It Is

Azure-managed identity attached to VM.

No credentials stored anywhere.

---

### Flow

```
VM → Azure metadata → identity → RBAC check → token → ACR access
```

---

### Commands

```bash
az login --identity
az acr login --name <acr-name>
```

---

### Why It’s Better

| Method           | Risk       |
| ---------------- | ---------- |
| Credentials      | Can leak   |
| Managed Identity | No secrets |

---

## 🌍 Operational Insights

* VM = control + responsibility
* NSG must be attached
* Region capacity matters
* Public vs Private IP:

```
Public → user access  
Private → internal system
```

---

## 🧠 Key Takeaways

* Infrastructure must be reproducible
* Remote state prevents drift
* cloud-init bridges infra → runtime
* Terraform defines structure, not execution
* Managed Identity removes credential management
````