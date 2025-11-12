# Azure Infrastructure as Code (IaC)

This directory contains the Infrastructure as Code (IaC) files for deploying the BP Calculator application to Azure.

## Files

- **main.bicep**: Main Bicep template that defines Azure resources
- **parameters.json**: Parameters file for the Bicep template

## Resources Created

The Bicep template creates the following Azure resources:

1. **App Service Plan** (Linux-based)

   - SKU: B1 (Basic) - configurable
   - OS: Linux
   - Python 3.12 runtime

2. **Web App** (App Service)

   - Linux container with Python 3.12
   - HTTPS only
   - Automatic build during deployment
   - Managed identity enabled

3. **Key Vault**
   - For storing application secrets
   - Integrated with Web App via managed identity
   - Soft delete enabled

## Prerequisites

- Azure CLI installed
- Azure subscription
- Appropriate permissions to create resources

## Manual Deployment (Optional)

If you want to deploy manually before setting up CI/CD:

```bash
# Login to Azure
az login

# Create resource group
az group create --name bp-calculator-rg --location eastus

# Deploy infrastructure
az deployment group create \
  --resource-group bp-calculator-rg \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/parameters.json

# Get the Web App URL
az deployment group show \
  --resource-group bp-calculator-rg \
  --name main \
  --query properties.outputs.webAppUrl.value
```

## Automated Deployment

The infrastructure is automatically deployed via GitHub Actions CI/CD pipeline. See `.github/workflows/azure-deploy.yml` for details.

## Configuration

### Modify Parameters

Edit `parameters.json` to customize:

- `webAppName`: Name of your web application
- `location`: Azure region (e.g., eastus, westus2)
- `sku`: App Service Plan pricing tier (F1, B1, B2, S1, etc.)
- `linuxFxVersion`: Python runtime version

### Environment Variables

The following environment variables are configured:

- `FLASK_ENV`: Set to 'production'
- `SECRET_KEY`: Retrieved from Key Vault
- `SCM_DO_BUILD_DURING_DEPLOYMENT`: Enables automatic pip install

## Security

- Application uses HTTPS only
- Secrets stored in Azure Key Vault
- Managed Identity for secure Key Vault access
- Soft delete enabled on Key Vault

## Cost Optimization

- Default SKU is B1 (Basic tier) which costs ~$13/month
- For development/testing, consider F1 (Free tier)
- For production, consider scaling up to S-tier or P-tier

## Cleanup

To remove all resources:

```bash
az group delete --name bp-calculator-rg --yes --no-wait
```
