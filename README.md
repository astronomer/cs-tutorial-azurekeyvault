# cs-tutorial-azurekeyvault
Showcasing the implementation Azure Key Vault as a Secrets Backend and some of the options available.

## Description

In addition to retrieving connections & variables from environment variables or the metastore database, you can enable an alternative secrets backend to retrieve Airflow connections or Airflow variables.

Two sample DAGs are provided, one for getting a Variable, and one for using Connections from your secrets backend. It is important to note that the method for using variables/connections is the same as not using a secrets backend - the key components for making this work are the entries in your Dockerfile.

## Getting Started

### Dependencies
To implement Azure Key Vault, add this to your requirements.txt:
```
apache-airflow-providers-microsoft-azure
```

Additionally, add the ENV Vars found in the Dockerfile in this repo, populated with values from your Azure instance.
```
ENV AZURE_CLIENT_ID="YOUR_CLIENT_ID" # Found in App Registration Page
ENV AZURE_TENANT_ID="YOUR_TENANT_ID" # Found in App Registration Page
ENV AZURE_CLIENT_SECRET="YOUR_CLIENT_SECRET" # Found in App Registration Page > Client Secrets >> 'Value'

ENV AIRFLOW__SECRETS__BACKEND="airflow.providers.microsoft.azure.secrets.azure_key_vault.AzureKeyVaultBackend"

# Using prefixes and default '-' separator:
ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "vault_url": "your_vault_url"}'

# Using no prefixes and no separator:
# ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "", "sep":"", "variables_prefix": "", "sep":"", "vault_url": "your_vault_url"}'
```
### Installing

In order to run these demos on your localhost, be sure to install:

* [Docker](https://www.docker.com/products/docker-desktop)

* [Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/resources/cli-reference)


### Executing demos

Clone this repository, then navigate to the ```cs-tutorial-azurekeyvault``` directory and start your local Airflow instance:
```
astro dev start
```

In your browser, navigate to ```http://localhost:8080/```

* Username: ```admin```

* Password: ```admin```


### Usage and Options available:
**Variables:**

- The default separator is `-` unless specified in  `ENV AIRFLOW__SECRETS__BACKEND_KWARGS`
    - i.e. When creating a variable, you must include the prefix name **and** the separator being used
        
        **Example:**
        
    - If using a prefix such as `"variables_prefix": "airflow-variables"` with the default `-` separator:
        - Create a secret named `airflow-variables-test` with a value `my-test-variable`
        - When retrieving the variable, call it with everything after the prefix + separator (in this case, `test` which comes after `airflow-variables-`
        
        ```python
        from airflow.models import Variable
        
        def print_var():
            my_var = Variable.get("test")
            print(f'My variable is: {my_var}')
        
        ....
        # Printed logs:
        {logging_mixin.py:109} INFO - My variable is: my-test-variable
        ```
      


**Connections:**

- Similar to the Variables example above, the connections prefix set in our Dockerfile was `airflow-connections` with the default `-` separator being used.
- **Example using a localhost instance postgres metadatadb:**
    - In your Key Vault, Create a secret named `airflow-connections-postgresdb` with the connection URI as the value. For the default localhost postgres db, the URI is: `postgres://postgres:postgres@postgres:5432/postgres`
    - In order to use the `postgresdb`secret you just created, simply use the value `postgresd` anywhere you would typically enter a connection_id. For example:
        
        ```python
        # Example 1:
        postgres_hook = PostgresHook(postgres_conn_id='postgresdb')
        
        # Example 2:
        t1 = PostgresOperator(
                task_id='postgres_query',
                postgres_conn_id='postgresdb',
                sql="""select * from dag""")
        ```
        

**Prefixes & Separators:**

- If you would like to not use prefixes or separators, update this line in your Dockerfile accordingly.
    - To use no connections_prefix (e.g. `airflow-connections`), update your ENV var to: `"connections_prefix": ""`
    - To use no variables_prefix, add `"variables_prefix": ""`
    - To use no separator (e.g. no longer use the default `-` separator), add `"sep":""`
    
    ```python
    ENV AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "", "sep":"", "variables_prefix": "", "sep":"", "vault_url": "your_vault_url"}'
    ```
    
    **Examples using no prefix and no separator:**
    
    - **Variable Example -** In Key Vault, create a variable named `variable-no-prefix` with a value, for example `This-is-my-no-prefix-variable`
    
    <aside>
    ⚠️ Note: The key difference here is that you did not need to have `airflow-variables-`as the prefix to your variable name.
    
    </aside>
    
    ```python
    from airflow.models import Variable
    
    def print_var():
        # Print a variable from Azure Key Vault:
        my_var = Variable.get("variable-no-prefix")
        print(f'My variable is: {my_var}')
    
    ....
    # Printed logs:
    {logging_mixin.py:109} INFO - My variable is: This-is-my-no-prefix-variable
    ```
    
    - **Connection Example** - similar to the no-prefix Variable example above, in Key Vault, create a variable named `postgresdbnoprefix` with a value containing the connection string. In this example, the localhost postgres connection string is `postgres://postgres:postgres@postgres:5432/postgres`
    
    ```python
    # Example 1:
    postgres_hook = PostgresHook(postgres_conn_id='postgresdbnoprefix')
    
    # Example 2:
    t1 = PostgresOperator(
            task_id='postgres_query',
            postgres_conn_id='postgresdbnoprefix',
            sql="""select * from dag""")
    ```

### Additional Resources
- If you have an existing connection created in the Airflow UI and would like to generate the connection URI, see example [methods available here](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#generating-a-connection-uri).
- [Apache Airflow Secrets Backend docs](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html)
- [Astronomer - Secrets Management in Airflow 2.0](https://www.astronomer.io/blog/secrets-management-airflow-2)