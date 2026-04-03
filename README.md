## Project Title -  Cloud-Native Monitoring Service on Azure

### Overview

This project demonstrates how to design, containerize, and deploy a cloud-native monitoring service using Docker and Azure.

It follows a real-world workflow:
- Build and containerize a Python Flask application
- Push the image to Azure Container Registry (ACR)
- Deploy it to Azure App Service
- Monitor system-level metrics (CPU, memory, disk)

The project focuses on understanding container lifecycle, cloud deployment behavior, authentication between services, and debugging real-world issues.

## Project Evolution

### Dockerized Flask App – Phase 1


This project demonstrates how to package a simple Python web application into a Docker container and run it locally.

### What I Did
* Built a simple Flask application.
* Created a Dockerfile to containerize the app
* Built a Docker image
* Ran the container locally with port mapping
* Verified the application via browser.

### Next Steps
* Push image to Azure Container Registry
* Deploy container to Azure App Service

### Cloud Deployment with Azure (Phase 2)
### Overview

After successfully containerizing and running the Flask application locally using Docker, the next step was to deploy the application to the cloud using Azure.

#### Application Features
The monitoring service exposes the following endpoints:
* /health – basic health check
* /uptime – application uptime in seconds
* /metrics – system‑level metrics (CPU, memory, disk)

All responses are returned in JSON format.

Access:
``` 
https://monitoring-webapp.azurewebsites.net/uptime
https://monitoring-webapp.azurewebsites.net/metrics
https://monitoring-webapp.azurewebsites.net/health
```

#### *Required troubleshooting around image pulls, port binding, and container restarts (details in troubleshooting notes)*

#### Architecture
Local Machine → Docker Image → Azure Container Registry → Azure App Service → Public Web URL


### System Monitoring Service and Observability (Phase 3)
Deployed the updated service using the same Docker → Azure workflow and evolved the application by adding:
* /status – aggregated runtime status
* /check – external connectivity check
* Integrated system-level metrics collection using psutil.

Access:
``` 
https://monitoring-webapp.azurewebsites.net/check
https://monitoring-webapp.azurewebsites.net/status
```
### Version Evolution

- v1: Basic Flask application.
- v2: Dockerized application.
- v3: Deployed to Azure App Service.
- v4: Monitoring service with system metrics endpoints.

Each version was built, tagged, and deployed using Docker and Azure Container Registry.

### Challenges Faced

* Versioned images enable safe deployments and rollbacks.
* Container images must be explicitly authorized for pull access when using private registries.
* System metrics in cloud containers reflect the broader runtime environment, not just application logic.
* Many cloud deployment issues only surface through hands‑on troubleshooting.

### Final Outcome
* Application successfully containerized using Docker.
* Image stored in Azure Container Registry.
* Application deployed to Azure App Service.
* Public URL accessible via browser.
### Screenshots

#### Monitoring Endpoint (Live)
![Metrics Endpoint](images/metrics.png)

#### Azure App Service Overview
![Azure App Service](images/azure-overview.png)

#### Log Streaming (Debugging)
![Logs](images/logs.png)