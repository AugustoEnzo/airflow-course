from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f"Hello World! my name is {first_name + last_name} and my age is {age}.")


def get_name(ti):
    ti.xcom_push(key='first_name', value='August')
    ti.xcom_push(key='last_name', value='Enzo')


with DAG(
        default_args=default_args,
        dag_id='dag_with_python_operator_v05',
        description='Our first dag using python operator',
        start_date=datetime(2022, 8, 29),
        schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 21}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task2 >> task1
