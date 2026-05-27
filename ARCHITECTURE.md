
# 🏗️ Cloud-Native Monitoring Service — Architecture

## 📌 Overview

This project demonstrates the design and evolution of a cloud-native monitoring service built using Docker and deployed on Azure.

It follows a real-world progression from a simple containerized application to a fully automated, multi-container cloud system using Infrastructure as Code and secure identity-based access.

---

## 🧭 Architecture Evolution (Phases)


### 🟢 Phase 1 — Dockerized Flask Application

Built and containerized a simple Python Flask application and ran it locally.

**Architecture:**

```

Local Machine → Docker Container → Browser

```

**Key Work:**
- Built Flask app
- Created Dockerfile
- Built image and ran container locally
- Verified via browser

---

### 🔵 Phase 2 — Cloud Deployment (Azure App Service)

Deployed the containerized application to Azure using a managed platform.

**Architecture:**

```

Local Machine → Docker Image → Azure Container Registry → Azure App Service → Public URL

```

**Live endpoints (decommissioned):**
```
https://monitoring-webapp.azurewebsites.net/health
https://monitoring-webapp.azurewebsites.net/uptime
https://monitoring-webapp.azurewebsites.net/metrics
https://monitoring-webapp.azurewebsites.net/status
https://monitoring-webapp.azurewebsites.net/check
```

**Key Characteristics:**
- Managed runtime and lifecycle
- Automatic restarts and health monitoring
- Minimal infrastructure responsibility

---

### 🟣 Phase 3 — Monitoring & Observability

Expanded the application into a monitoring service.

**Endpoints added:**
- `/health` — basic health check  
- `/uptime` — runtime duration  
- `/metrics` — CPU, memory, disk usage  
- `/status` — aggregated system view  
- `/check` — dependency reachability  

**Key Insight:**
System metrics in cloud environments reflect the broader runtime environment, not just the application.

---

### 🟡 Phase 4 — VM Deployment (IaaS Model)

Deployed the same containerized application on an Azure Linux VM.

**Architecture:**

```

Azure VM → Docker → Containerized Application → Public IP Access

```

**Key Differences from PaaS:**
- Full control over OS and runtime
- Manual responsibility for:
  - Networking (NSG rules)
  - Process lifecycle
  - Restart behavior
  - Security configuration

---

### 🟠 Phase 5 — Infrastructure as Code (Terraform)

Transitioned from manual infrastructure setup to a fully declarative model.

**Implementation:**
- Provisioned VM, networking, NSG, and SSH using Terraform
- Introduced variables for flexibility
- Configured remote state in Azure Blob Storage
- Used cloud-init to automate VM setup (Docker + app startup)

**Key Outcome:**
Infrastructure became fully reproducible — no manual setup required.

---

### 🔴 Phase 6 — Multi-Container Architecture & Private Registry

Evolved into a distributed container system.

**Architecture:**

```

Azure VM
└── Docker Compose
├── web1 → port 5000
├── web2 → port 5001
└── web3 → port 5002

```

**Network Architecture:**

```

Internet
└── Azure NSG
└── Azure VM (Public IP)
└── Docker bridge network
├── web1 (:80 → 5000)
├── web2 (:80 → 5001)
└── web3 (:80 → 5002)

```

**Implementation:**
- Three container instances running simultaneously
- Each container monitors the others via `/check`
- Used Docker internal DNS (service names)
- Pulled private images from ACR using Managed Identity

**Key Insights:**
- `localhost` inside a container ≠ VM localhost  
- Container communication uses service names (`web2:80`)  
- NSG controls external access, not internal container traffic  

---

### 🟣 Phase 7 — CI/CD & Automated Deployment

Introduced a fully automated pipeline using GitHub Actions.

**Architecture:**

```

Developer → GitHub → GitHub Actions → ACR → Azure VM → Docker Compose → Containers

```

**Full Deployment Flow:**

```

git push → GitHub Actions
├── Login to Azure (OIDC)
├── Build Docker image
├── Push image to ACR (SHA tagged)
└── SSH to VM
└── docker-compose up -d --pull always

```

**Key Features:**
- OIDC authentication (no stored secrets)
- Automated build → push → deploy pipeline
- Zero manual deployment steps
- Always pulls latest built image (by SHA)

---

## 🔐 Identity & Access Architecture

| Component | Authentication | Role | Permission |
|----------|--------------|------|-----------|
| GitHub Actions | OIDC (federated identity) | AcrPush | Push images |
| Azure VM | Managed Identity | AcrPull | Pull images |
| Developer | az login | Owner | Full access |

**No credentials are stored anywhere.**

---

### 🔑 Identity Flow

**OIDC (GitHub → Azure):**
```

GitHub → Azure AD → short-lived token → ACR push

```

**Managed Identity (VM → ACR):**
```

VM → Azure metadata service → token → ACR pull

```

---

## 📦 Versioning Strategy

The application evolved through versioned container images:

- v1 → Basic Flask app  
- v2 → Dockerized application  
- v3 → App Service deployment  
- v4 → Monitoring endpoints  
- v5 → Multi-container architecture  

Later improvement:
- Switched to **commit SHA tagging** for:
  - Reproducibility  
  - Traceability  
  - Rollback capability  

---

## ⚖️ Design Trade-offs

### PaaS (App Service)
✔ Managed lifecycle  
✔ Auto recovery  
❌ Limited control  

### IaaS (VM)
✔ Full control  
✔ Flexible architecture  
❌ Operational overhead  

---

## 🧠 Key Architectural Learnings

- Private registries require explicit authorization  
- Managed Identity removes credential management  
- Containers do not share localhost  
- Infrastructure state ≠ runtime state  
- Remote state prevents drift  
- Restart policies are required for resilience  
- Many issues only surface through real deployments  

---

## 🧪 Debugging Flow

When troubleshooting:

```

Internet → Public IP → NIC → Subnet → NSG → VM → Docker → Container

```

---

## 🎯 Final Outcome

- Fully containerized application
- Versioned images stored in ACR
- CI/CD pipeline with OIDC authentication
- Multi-container deployment via Docker Compose
- Secure image pulls using Managed Identity
- Fully reproducible infrastructure via Terraform
- Zero manual deployment steps
- System resilient across restarts

---

## 🚀 Summary

This project demonstrates the transition from:

- Local development → Cloud deployment  
- Manual setup → Infrastructure as Code  
- Single container → Distributed system  
- Credential-based auth → Identity-based access  

Resulting in a secure, automated, and production-aware cloud-native architecture.

