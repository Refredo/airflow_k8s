from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
from airflow import DAG, Dataset

from datetime import timedelta, datetime


default_args = {
    'owner': 'artem',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


with DAG(
    dag_id='test_bash_operator',
    description='DAG with test bash operator',
    default_args=default_args,
    start_date=datetime(2024, 11, 18, 0, 0), 
    schedule_interval='*/1 * * * *',  
    catchup=False,  
) as dag:
    
    test_bash_command = BashOperator(
        task_id='test_bash_operator',
        bash_command='echo hello from K8s Airflow'
    )
    
    test_bash_command
    
    # wait_for_file_appear = S3KeySensor(
    #     task_id='wait_for_file_appear',
    #     bucket_name='data',
    #     bucket_key='tiktok_google_play_reviews.csv',
    #     aws_conn_id='minio_connection',
    #     verify=False,
    #     timeout=3600,
    #     poke_interval=5,
    #     mode='poke'
    # )
    
    # check_is_empty_file = BranchPythonOperator(
    #     task_id='check_is_empty_file',
    #     python_callable=check_if_file_empty
    # )
    
    # log_file_empty = BashOperator(
    #     task_id='log_file_empty',
    #     bash_command='echo file in bucket is empty, no need to process'
    # )
     
    # with TaskGroup('process_file') as process_file_task_group:
         
    #     remove_nulls = PythonOperator(
    #         task_id='remove_nulls',
    #         python_callable=remove_nulls_task
    #     )
        
    #     sort_by_date = PythonOperator(
    #         task_id='sort_by_date',
    #         python_callable=sort_by_created_date
    #     )
        
    #     clear_content = PythonOperator(
    #         task_id='clear_content',
    #         python_callable=clear_content_column,
    #         outlets=[Dataset('http://minio:9000/data/tiktok_google_play_reviews.csv')]
    #     )
        
    #     remove_nulls >> sort_by_date >> clear_content
    
    # wait_for_file_appear >> check_is_empty_file >> [log_file_empty, process_file_task_group]
        
