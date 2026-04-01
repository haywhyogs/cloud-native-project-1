## Project Title -  Cloud-Native Monitoring Service on Azure

### Overview

This project demonstrates how to design, containerize, and deploy a cloud-native monitoring service using Docker and Azure.

It follows a real-world workflow:
- Build and containerize a Python Flask application
- Push the image to Azure Container Registry (ACR)
- Deploy it to Azure App Service
- Monitor system-level metrics (CPU, memory, disk)

The project focuses on understanding container lifecycle, cloud deployment behavior, authentication between services, and debugging real-world issues.


### Dockerized Flask App – Phase 1


This project demonstrates how to package a simple Python web application into a Docker container and run it locally.

### What I Did
* Built a simple Flask application.
* Created a Dockerfile to containerize the app
* Built a Docker image
* Ran the container locally with port mapping
* Verified the application via browser.

### How to Run
```
docker build -t ayodeji-app .

docker run -p 5000:5000 ayodeji-app
```
Visit: 
```
http://localhost:5000
```
### Challenges Faced

* Fixed incorrect Docker build command (missing build context)
* Resolved Docker permission issue by adding user to docker group
* Understood port mapping and why 0.0.0.0 is required.

### Next Steps
* Push image to Azure Container Registry
* Deploy container to Azure App Service
* Automate deployment with Terraform.

### Cloud Deployment with Azure (Phase 2)
### Overview

After successfully containerizing and running the Flask application locally using Docker, the next step was to deploy the application to the cloud using Azure.

#### Application Features
The monitoring service exposes the following endpoints:
* /health – basic health check
*  /uptime – application uptime in seconds
* /metrics – system‑level metrics (CPU, memory, disk)

All responses are returned in JSON format.

#### Architecture
Local Machine → Docker Image → Azure Container Registry → Azure App Service → Public Web URL
### Deployment Steps
* Build Docker Image Locally

```
docker build -t ayodeji-app .
```

* Login

```
az login
```
* Create Resource Group

```
az group create --name <resource-group> --location canadacentral
```
* Create Azure Container Registry (ACR)
```
az acr create \
  --resource-group <resource-group> \
  --name <acr-name> \
  --sku Basic
  ```
* Tag Image for Azure Container Registry (ACR)

```
docker tag ayodeji-app <acr-name>.azurecr.io/ayodeji-app:v1
```

* Login to ACR (WSL-safe method)
```
echo "<password>" | docker login <acr-name>.azurecr.io \
  --username <username> \
  --password-stdin
  ```
* Enable ACR Authentication
```
az acr update --name <acr-name> --admin-enabled true
```

* Push Image to ACR
```
docker push <acr-name>.azurecr.io/ayodeji-app:v1
```
* Verify with 
```
az acr repository list --name acrusername -o table
```

* Create App Service Plan (Compute and SKU) Size,availability and cost.

```
az appservice plan create \
  --name <plan-name> \
  --resource-group <resource-group> \
  --sku B1 \
  --is-linux
  ```
* Create Web App (Container-Based)
```
az webapp create \
  --resource-group <resource-group> \
  --plan <plan-name> \
  --name <app-name> \
  --deployment-container-image-name <acr-name>.azurecr.io/ayodeji-app:v1
  ```

9. Configure Container Settings (Allow Web app to pull from ACR)
```
az webapp config container set \
  --name <app-name> \
  --resource-group <resource-group> \
  --docker-custom-image-name <acr-name>.azurecr.io/ayodeji-app:v1 \
  --docker-registry-server-url https://<acr-name>.azurecr.io
  ```
* Set Required Port Configuration
```
az webapp config appsettings set \
  --name <app-name> \
  --resource-group <resource-group> \
  --settings WEBSITES_PORT=80
  ```
* Restart Web App
```
az webapp restart \
  --name <app-name> \
  --resource-group <resource-group>
  ```
* Access the Application
```
https://<app-name>.azurewebsites.net
```

Access locally:
``` 
http://localhost:5000
```

### Challenges Faced & Solutions
#### Docker Login Failure (WSL Issue)

Docker login failed with credential storage errors

* Cause:

Conflict between WSL and Docker Desktop credential helper

* Solution:

Removed credential helper from Docker config
Used --password-stdin for login

#### Application Not Loading (504 Error)

Azure App Service requires explicit port configuration. The application was updated to run on port 80 to align with platform expectations.

Set:
WEBSITES_PORT=80

### Whenever changes are made:
```
docker build -t ayodeji-app .
docker tag ayodeji-app <acr-name>.azurecr.io/ayodeji-app:v1
docker push <acr-name>.azurecr.io/ayodeji-app:v1
az webapp restart --name <app-name> --resource-group <resource-group>
```

### System Monitoring Service (Phase 3)

* Evolved the application into a monitoring service by adding health, uptime, and system metrics endpoints
* Integrated system-level metrics collection using psutil
* Deployed the updated service using the same Docker → Azure workflow

#### Key Learnings from This Phase
* Container images must be explicitly authorized for pull access when using private registries.
* System metrics in cloud containers reflect the broader runtime environment, not just application logic.
* Many cloud deployment issues only surface through hands‑on troubleshooting.

Access locally:
``` 
https://monitoring-webapp.azurewebsites.net/uptime
https://monitoring-webapp.azurewebsites.net/metrics
https://monitoring-webapp.azurewebsites.net/health
```
### Version Evolution

- v1: Basic Flask application
- v2: Dockerized application
- v3: Deployed to Azure App Service
- v4: Monitoring service with system metrics endpoints

Each version was built, tagged, and deployed using Docker and Azure Container Registry.

### Final Outcome
* Application successfully containerized using Docker
* Image stored in Azure Container Registry
* Application deployed to Azure App Service
* Public URL accessible via browser
### Screenshots

#### Monitoring Endpoint (Live)
![Metrics Endpoint](images/metrics.png)

#### Azure App Service Overview
![Azure App Service](images/azure-overview.png)

#### Log Streaming (Debugging)
![Logs](images/logs.png)