from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def greet(name, age):
    print(f"Hello World! my name is {name} and my age is {age}.")


with DAG(
        default_args=default_args,
        dag_id='dag_with_python_operator_v02',
        description='Our first dag using python operator',
        start_date=datetime(2022, 8, 29),
        schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'August', 'age': 21}
    )
