import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step 1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="database-server_postgres")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE date >= %s and date < %s",
                   (ds_nodash, next_ds_nodash))
    # with open(f"dags/get_orders_{ds_nodash}.txt", "w") as temp_file:
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as temp_file:
        csv_writer = csv.writer(temp_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        temp_file.flush()
        cursor.close()
        conn.close()
        logging.info(f"Saved orders data in text file: dags/get_orders_{ds_nodash}.txt")
    # Step 2: upload text file into S3
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename=temp_file.name,
            key=f"orders/{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True
        )
        logging.info("Orders file %s has been pushed to S3!", temp_file.name)


with DAG(
    dag_id="hook_postgres_dag_v04",
    default_args=default_args,
    start_date=datetime(2022, 8, 29),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )
    task1
