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
        # application='/scripts/process_weather_data.py',
        application='/opt/airflow/dags/repo/dags/scripts/process_weather_data.py',
        name='process_weather_data_job',
        conn_id='spark_conn',
        # conf={
        #     "spark.kubernetes.container.image": "bitnami/spark:latest",  # Образ Spark
        #     "spark.kubernetes.namespace": "default",  # Namespace для Spark
        # },
        verbose=True,
        # conf={
        #     'spark.executor.memory': '2g',
        #     'spark.executor.cores': '1',
        #     'spark.hadoop.fs.s3a.access.key': 'uchBfIlUp1I8QUa8erMz',
        #     'spark.hadoop.fs.s3a.secret.key': 'RQF7k9yXj9GIKVVN2ew3NmoDG0PTiJGUVDdfjlfd',
        #     'spark.hadoop.fs.s3a.endpoint': 'minio-service:9000',
        #     'spark.hadoop.fs.s3a.path.style.access': 'true'
        #     },

        env_vars={
        "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk",
        "PATH": "/usr/lib/jvm/java-11-openjdk/bin:$PATH"
        },
        # application_args=['arg1', 'arg2'],
        # executor_cores=2,
        # executor_memory='1g',
        # driver_memory='1g',
    )
    
    process_weather_data