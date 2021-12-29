from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator


def get_dags():
    # Example 1: using your 'postgresdb' conn_id in a hook:
    postgres_hook = PostgresHook(postgres_conn_id="postgresdb")
    # To prove the connection worked, print records from a metadata table. View output in task log:
    records = postgres_hook.get_records(sql="select * from dag")
    print("Here is a list of your DAGs:")
    for row in records:
        print(row)


with DAG(
    "connections-using-backend",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Example 2: Using your 'postgres' conn_id in a PostgresOperator:
    t1 = PostgresOperator(
        task_id="postgres_query",
        postgres_conn_id="postgresdb",
        sql="""select * from dag""",
    )

    t2 = PythonOperator(
        task_id="get_dags",
        python_callable=get_dags,
    )

    t1 >> t2
