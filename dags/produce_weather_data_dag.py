from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import timedelta, datetime

from scripts.get_weather_data import put_weather_info

default_args = {
    'owner': 'artem',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


with DAG(
    dag_id='produce_weather_data',
    description='upload weather data in Kafka topic',
    default_args=default_args,
    start_date=datetime(2024, 12, 11, 10, 0, 0),
    schedule_interval='*/1 * * * *',
    catchup=False
) as dag:
    
    produce_data = PythonOperator(
        task_id='produce_data',
        python_callable=put_weather_info
    )
    
    produce_data