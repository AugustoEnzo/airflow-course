from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
        dag_id='first_dag',
        default_args=default_args,
        description='This is my test airflow first DAG',
        start_date=datetime(2022, 8, 29),
        schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is the first task!"
    )

    task1
