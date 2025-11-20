#!/bin/bash

# Azure Update Script for Restaurant Management API
# This script updates the existing deployment with a new Docker image

set -e  # Exit on error

# Configuration variables (must match deployment script)
ACR_NAME="restaurantapiacr"
IMAGE_NAME="restaurant-api"
IMAGE_TAG="latest"
RESOURCE_GROUP="restaurant-api-rg"
WEB_APP_NAME="restaurant-api-app"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Restaurant API - Azure Update${NC}"
echo -e "${GREEN}========================================${NC}"

# Step 1: Build and push new Docker image
echo -e "${YELLOW}Step 1: Building and pushing new Docker image...${NC}"
cd ..
az acr build \
    --registry $ACR_NAME \
    --image $IMAGE_NAME:$IMAGE_TAG \
    --file Dockerfile \
    .

# Step 2: Restart Web App to pull new image
echo -e "${YELLOW}Step 2: Restarting Web App to pull new image...${NC}"
az webapp restart \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --output table

# Get Web App URL
WEB_APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "defaultHostName" -o tsv)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Update Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Web App URL: https://$WEB_APP_URL${NC}"
echo -e "${GREEN}API Docs: https://$WEB_APP_URL/docs${NC}"
echo -e "${GREEN}========================================${NC}"
