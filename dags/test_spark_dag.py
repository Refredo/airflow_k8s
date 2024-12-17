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
    
    
    test_bash_task = BashOperator(
    task_id='test_bash',
    bash_command='/usr/bin/env bash --version',
    dag=dag
    )
    
    process_weather_data = SparkSubmitOperator(
        task_id='process_weather_data',
        # application='/scripts/process_weather_data.py',
        application='/opt/airflow/dags/repo/dags/scripts/process_weather_data.py',
        name='process_weather_data_job',
        conn_id='spark_conn',
        spark_binary='/opt/spark/bin/spark-submit',
        # conf={
        #     "spark.kubernetes.container.image": "bitnami/spark:latest",  # Образ Spark
        #     "spark.kubernetes.namespace": "default",  # Namespace для Spark
        # },
        verbose=True,
        env_vars={
        "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk",
        "PATH": "/usr/lib/jvm/java-11-openjdk/bin:$PATH"
        },
        # application_args=['arg1', 'arg2'],
        # executor_cores=2,
        # executor_memory='1g',
        # driver_memory='1g',
    )
    
    test_bash_task >> process_weather_data