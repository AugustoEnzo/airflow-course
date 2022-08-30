from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_operator_v02',
    default_args=default_args,
    start_date=datetime(2022, 8, 29),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='database-server_postgres',
        sql="""
            CREATE TABLE IF NOT EXISTS dag_runs (
            dt date,
            dag_id character varying,
            primary key (dt, dag_id)
            );
        """
    )

    task2 = PostgresOperator(
        task_id='insert_into_dag',
        postgres_conn_id='database-server_postgres',
        sql="""
            INSERT INTO dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )

    task1 >> task2
