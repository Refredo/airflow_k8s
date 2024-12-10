from ariflow.operators.python import PythonOperator
from airflow import DAG

from datetime import timedelta, datetime

from scripts.script_producer import start_streaming

default_args = {
    'owner': 'artem',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

with DAG(
    dag_id='kafka_producer_dag',
    description='test DAG for interaction with Kafka',
    default_args=default_args,
    start_date=datetime(2024, 11, 18, 0, 0), 
    schedule_interval='*/1 * * * *',  
    catchup=False,
) as dag:
    
    produce_data = PythonOperator(
        task_id='produce_data',
        pythoncallable=start_streaming
    )
    
    produce_data
    
