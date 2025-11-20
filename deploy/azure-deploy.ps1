# Azure Deployment Script for Restaurant Management API (PowerShell)
# This script deploys the FastAPI application to Azure using Container Registry and Web App

# Configuration variables (modify these as needed)
$RESOURCE_GROUP = "restaurant-api-rg"
$LOCATION = "eastus"
$ACR_NAME = "restaurantapiacr"
$APP_SERVICE_PLAN = "restaurant-api-plan"
$WEB_APP_NAME = "restaurant-api-app"
$IMAGE_NAME = "restaurant-api"
$IMAGE_TAG = "latest"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Restaurant API - Azure Deployment" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if Azure CLI is installed
try {
    az --version | Out-Null
} catch {
    Write-Host "Error: Azure CLI is not installed" -ForegroundColor Red
    Write-Host "Please install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Login to Azure (if not already logged in)
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    az account show | Out-Null
} catch {
    Write-Host "Please log in to Azure..." -ForegroundColor Yellow
    az login
}

# Step 1: Create Resource Group
Write-Host "Step 1: Creating Resource Group..." -ForegroundColor Yellow
az group create `
    --name $RESOURCE_GROUP `
    --location $LOCATION `
    --output table

# Step 2: Create Azure Container Registry
Write-Host "Step 2: Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create `
    --resource-group $RESOURCE_GROUP `
    --name $ACR_NAME `
    --sku Basic `
    --admin-enabled true `
    --output table

# Step 3: Build and push Docker image to ACR
Write-Host "Step 3: Building and pushing Docker image..." -ForegroundColor Yellow
Set-Location ..
az acr build `
    --registry $ACR_NAME `
    --image "${IMAGE_NAME}:${IMAGE_TAG}" `
    --file Dockerfile `
    .

# Step 4: Create App Service Plan (Linux)
Write-Host "Step 4: Creating App Service Plan..." -ForegroundColor Yellow
az appservice plan create `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --is-linux `
    --sku B1 `
    --output table

# Step 5: Create Web App from container
Write-Host "Step 5: Creating Web App..." -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $APP_SERVICE_PLAN `
    --name $WEB_APP_NAME `
    --deployment-container-image-name "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" `
    --output table

# Step 6: Configure ACR credentials for Web App
Write-Host "Step 6: Configuring ACR credentials..." -ForegroundColor Yellow
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
az webapp config container set `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --docker-custom-image-name "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" `
    --docker-registry-server-url "https://${ACR_NAME}.azurecr.io" `
    --docker-registry-server-user $ACR_NAME `
    --docker-registry-server-password $ACR_PASSWORD `
    --output table

# Step 7: Configure Web App settings
Write-Host "Step 7: Configuring environment variables..." -ForegroundColor Yellow
Write-Host "Please enter your database credentials:" -ForegroundColor Yellow
$DB_SERVER = Read-Host "DB_SERVER"
$DB_NAME = Read-Host "DB_NAME"
$DB_USER = Read-Host "DB_USER"
$DB_PASSWORD = Read-Host "DB_PASSWORD" -AsSecureString
$DB_PASSWORD_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($DB_PASSWORD))

az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --settings `
        DB_SERVER="$DB_SERVER" `
        DB_NAME="$DB_NAME" `
        DB_USER="$DB_USER" `
        DB_PASSWORD="$DB_PASSWORD_PLAIN" `
        DB_DRIVER="ODBC Driver 17 for SQL Server" `
        PORT="8000" `
        CORS_ORIGINS="*" `
        DEBUG="false" `
        RELOAD="false" `
        SQL_ECHO="false" `
        WEBSITES_PORT="8000" `
    --output table

# Step 8: Enable continuous deployment
Write-Host "Step 8: Enabling continuous deployment..." -ForegroundColor Yellow
az webapp deployment container config `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --enable-cd true `
    --output table

# Step 9: Restart Web App
Write-Host "Step 9: Restarting Web App..." -ForegroundColor Yellow
az webapp restart `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --output table

# Get Web App URL
$WEB_APP_URL = az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "defaultHostName" -o tsv

Write-Host "========================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Web App URL: https://$WEB_APP_URL" -ForegroundColor Green
Write-Host "API Docs: https://$WEB_APP_URL/docs" -ForegroundColor Green
Write-Host "Health Check: https://$WEB_APP_URL/health" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
