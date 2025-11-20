#!/bin/bash

# Azure Deployment Script for Restaurant Management API
# This script deploys the FastAPI application to Azure using Container Registry and Web App

set -e  # Exit on error

# Configuration variables (modify these as needed)
RESOURCE_GROUP="restaurant-api-rg"
LOCATION="eastus"
ACR_NAME="restaurantapiacr"
APP_SERVICE_PLAN="restaurant-api-plan"
WEB_APP_NAME="restaurant-api-app"
IMAGE_NAME="restaurant-api"
IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Restaurant API - Azure Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed${NC}"
    echo "Please install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure (if not already logged in)
echo -e "${YELLOW}Checking Azure login status...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Please log in to Azure...${NC}"
    az login
fi

# Step 1: Create Resource Group
echo -e "${YELLOW}Step 1: Creating Resource Group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Step 2: Create Azure Container Registry
echo -e "${YELLOW}Step 2: Creating Azure Container Registry...${NC}"
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true \
    --output table

# Step 3: Build and push Docker image to ACR
echo -e "${YELLOW}Step 3: Building and pushing Docker image...${NC}"
cd ..
az acr build \
    --registry $ACR_NAME \
    --image $IMAGE_NAME:$IMAGE_TAG \
    --file Dockerfile \
    .

# Step 4: Create App Service Plan (Linux)
echo -e "${YELLOW}Step 4: Creating App Service Plan...${NC}"
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --is-linux \
    --sku B1 \
    --output table

# Step 5: Create Web App from container
echo -e "${YELLOW}Step 5: Creating Web App...${NC}"
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --deployment-container-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
    --output table

# Step 6: Configure ACR credentials for Web App
echo -e "${YELLOW}Step 6: Configuring ACR credentials...${NC}"
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
az webapp config container set \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --docker-custom-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
    --docker-registry-server-url https://$ACR_NAME.azurecr.io \
    --docker-registry-server-user $ACR_NAME \
    --docker-registry-server-password $ACR_PASSWORD \
    --output table

# Step 7: Configure Web App settings
echo -e "${YELLOW}Step 7: Configuring environment variables...${NC}"
echo -e "${YELLOW}Please enter your database credentials:${NC}"
read -p "DB_SERVER: " DB_SERVER
read -p "DB_NAME: " DB_NAME
read -p "DB_USER: " DB_USER
read -sp "DB_PASSWORD: " DB_PASSWORD
echo

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        DB_SERVER="$DB_SERVER" \
        DB_NAME="$DB_NAME" \
        DB_USER="$DB_USER" \
        DB_PASSWORD="$DB_PASSWORD" \
        DB_DRIVER="ODBC Driver 17 for SQL Server" \
        PORT="8000" \
        CORS_ORIGINS="*" \
        DEBUG="false" \
        RELOAD="false" \
        SQL_ECHO="false" \
        WEBSITES_PORT="8000" \
    --output table

# Step 8: Enable continuous deployment
echo -e "${YELLOW}Step 8: Enabling continuous deployment...${NC}"
az webapp deployment container config \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --enable-cd true \
    --output table

# Step 9: Restart Web App
echo -e "${YELLOW}Step 9: Restarting Web App...${NC}"
az webapp restart \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

# Get Web App URL
WEB_APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "defaultHostName" -o tsv)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Web App URL: https://$WEB_APP_URL${NC}"
echo -e "${GREEN}API Docs: https://$WEB_APP_URL/docs${NC}"
echo -e "${GREEN}Health Check: https://$WEB_APP_URL/health${NC}"
echo -e "${GREEN}========================================${NC}"
