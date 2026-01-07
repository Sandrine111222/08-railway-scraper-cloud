#!/bin/bash
# Deploy iRail Azure Function & dependencies

# Set variables
RESOURCE_GROUP="irail-rg"
LOCATION="westeurope"
STORAGE_ACCOUNT="irailstorage$RANDOM"
FUNCTION_APP="irail-pipeline-app"

# Login (interactive)
az login

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Create Azure Function App (Python 3.14, Functions v4)
az functionapp create \
  --name $FUNCTION_APP \
  --storage-account $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.14 \
  --functions-version 4

# Deploy ZIP package (build functionapp.zip first)
zip -r functionapp.zip *

az functionapp deployment source config-zip \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --src functionapp.zip

echo "✅ Deployment complete. Visit https://$FUNCTION_APP.azurewebsites.net"
