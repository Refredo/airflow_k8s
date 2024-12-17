from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator
from airflow import DAG

from datetime import timedelta, datetime


default_args = {
    'owner': 'artem',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


with DAG(
    dag_id='test_spark_dag',
    description='test spark dag to execute Spark job',
    default_args=default_args,
    start_date=datetime(2024, 12, 11, 10, 0, 0),
    schedule_interval='@hourly',
    catchup=False
) as dag:
    
    
    process_weather_data = SparkSubmitOperator(
        task_id='process_weather_data',
        application='/opt/airflow/dags/repo/dags/scripts/process_weather_data.py',
        name='process_weather_data_job',
        conn_id='spark_conn',
        verbose=True,
    )
    
    process_weather_data
    