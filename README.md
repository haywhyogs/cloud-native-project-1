## Project Title
### Dockerized Flask App – Phase 1

### Overview

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