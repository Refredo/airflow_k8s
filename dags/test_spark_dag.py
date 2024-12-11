from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
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
        application='/scripts/process_weather_data.py',
        name='process_weather_data_job',
        verbose=True,
        conf={'spark.executor.memory': '2g', 'spark.executor.cores': '1'},  # Optional configurations
        # application_args=['arg1', 'arg2'],
        executor_cores=2,
        executor_memory='4g',
        driver_memory='4g',
    )