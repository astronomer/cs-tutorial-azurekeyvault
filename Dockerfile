FROM quay.io/astronomer/ap-airflow:2.2.3-onbuild

# Found in App Registration Page:
ENV AZURE_CLIENT_ID="YOUR_CLIENT_ID"

# Found in App Registration Page:
ENV AZURE_TENANT_ID="YOUR_TENANT_ID"

# Found in App Registration Page > Client Secrets >> 'Value':
ENV AZURE_CLIENT_SECRET="YOUR_CLIENT_SECRET"

ENV AIRFLOW__SECRETS__BACKEND="airflow.providers.microsoft.azure.secrets.azure_key_vault.AzureKeyVaultBackend"

# Option 1 - Using prefixes and default '-' separator:
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "your_vault_url"}'

# Option 2 - Using no prefixes and no separator:
# ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "", "sep":"", "variables_prefix": "", "sep":"", "vault_url": "your_vault_url"}'