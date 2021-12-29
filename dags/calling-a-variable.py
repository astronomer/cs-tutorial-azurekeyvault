from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


def print_var():
    # Example - Get and print your variable named 'test' from the Secrets Backend:
    my_var = Variable.get("test")
    print(f"My variable is: {my_var}")


with DAG(
    "variables-using-backend",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    get_print_variable = PythonOperator(
        task_id="get_print_variable",
        python_callable=print_var
    )
