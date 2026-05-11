### Azure Manual Deployment
#### Command history used to deploy the container to Azure App Service.
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

* Configure Container Settings (Allow Web app to pull from ACR)
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

* Whenever changes are made:
```
docker build -t ayodeji-app .
```
```
docker tag ayodeji-app <acr-name>.azurecr.io/ayodeji-app:v1
```
```
docker push <acr-name>.azurecr.io/ayodeji-app:v1
```
```
az webapp restart --name <app-name> --resource-group <resource-group>
```
