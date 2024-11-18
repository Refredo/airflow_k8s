from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
from airflow import DAG, Dataset

from datetime import timedelta, datetime
# from minio import Minio
from io import BytesIO

import pandas as pd



# def get_minio_client():
    
#     ACCESS_KEY = Variable.get('MINIO_ACCESS_KEY')
#     SECRET_KEY = Variable.get('MINIO_SECRET_KEY')
    
#     if not hasattr(get_minio_client, "client"):
#         get_minio_client.client = Minio(
#             "minio:9000",
#             access_key=ACCESS_KEY,
#             secret_key=SECRET_KEY,
#             secure=False
#         )
#     return get_minio_client.client


# def check_if_file_empty(**kwargs):
    
#     client = get_minio_client()
    
#     bucket_name = 'data'
#     obj_name = 'tiktok_google_play_reviews.csv'
    
#     response = None
    
#     try:
#         response = client.get_object(bucket_name, obj_name)
#         content_length = int(response.headers['Content-Length'])
#         print(f'Content-Length of file is {content_length}')

#     finally:
#         response.close()
#         response.release_conn()
        
#     if content_length == 0:
#         return 'log_file_empty'


#     ti = kwargs['ti']
#     ti.xcom_push(key='obj_name', value=obj_name)
#     ti.xcom_push(key='bucket_name', value=bucket_name)

#     return 'process_file'    

             
# def remove_nulls_task(**kwargs):
    
#     ti = kwargs['ti']
#     file_name = ti.xcom_pull(key='obj_name', task_ids='check_is_empty_file')
#     bucket_name = ti.xcom_pull(key='bucket_name', task_ids='check_is_empty_file')
    
#     print(f'file name from Xcom: {file_name}')
#     print(f'bucket_name from Xcom: {bucket_name}')
    
#     dtypes = {
#         'reviewId': str,
#         'userName': str,
#         'userImage': str,
#         'content': str,
#         'score': int,
#         'thumbsUpCount': int,
#         'reviewCreatedVersion': str,
#         'replyContent': str,
#     }
    
#     client = get_minio_client()
    
#     client.fget_object(bucket_name=bucket_name, 
#                        object_name=file_name, 
#                        file_path=file_name)
    
#     dataset = pd.read_csv(file_name, dtype=dtypes, parse_dates=['at', 'repliedAt'])
    
#     print(f'dataset before process')
#     print(dataset.head())
    
#     dataset = dataset.fillna('-')
    
#     print(f'dataset after process')    
#     print(dataset.head())
        
#     csv_buffer = BytesIO()
#     dataset.to_csv(csv_buffer, index=False)
#     csv_buffer.seek(0)
    
#     client.put_object(
#         bucket_name=bucket_name,
#         object_name=file_name,
#         data=csv_buffer,
#         length=-1,
#         part_size=10 * 1024 * 1024
#     )
    
    
# def sort_by_created_date(**kwargs):
    
#     ti = kwargs['ti']
#     file_name = ti.xcom_pull(key='obj_name', task_ids='check_is_empty_file')
#     bucket_name = ti.xcom_pull(key='bucket_name', task_ids='check_is_empty_file')
    
#     print(f'file name from Xcom: {file_name}')
#     print(f'bucket_name from Xcom: {bucket_name}')
    
#     dtypes = {
#         'reviewId': str,
#         'userName': str,
#         'userImage': str,
#         'content': str,
#         'score': int,
#         'thumbsUpCount': int,
#         'reviewCreatedVersion': str,
#         'replyContent': str,
#     }
    
#     client = get_minio_client()
        
#     client.fget_object(bucket_name=bucket_name, 
#                        object_name=file_name, 
#                        file_path=file_name)
    
#     dataset = pd.read_csv(file_name, dtype=dtypes, parse_dates=['at', 'repliedAt'])
    
#     print('dataset before sorting')
#     print(dataset.head())
    
#     dataset.sort_values('at')

#     print('dataset after sorting')
#     print(dataset.head())
    
#     csv_buffer = BytesIO()
#     dataset.to_csv(csv_buffer, index=False)
#     csv_buffer.seek(0)
    
#     client.put_object(
#         bucket_name=bucket_name,
#         object_name=file_name,
#         data=csv_buffer,
#         length=-1,
#         part_size=10 * 1024 * 1024
#     )    
    
        
# def clear_content_column(**kwargs):
    
#     ti = kwargs['ti']
#     file_name = ti.xcom_pull(key='obj_name', task_ids='check_is_empty_file')
#     bucket_name = ti.xcom_pull(key='bucket_name', task_ids='check_is_empty_file')
    
#     print(f'file name from Xcom: {file_name}')
#     print(f'bucket_name from Xcom: {bucket_name}')
    
#     dtypes = {
#         'reviewId': str,
#         'userName': str,
#         'userImage': str,
#         'content': str,
#         'score': int,
#         'thumbsUpCount': int,
#         'reviewCreatedVersion': str,
#         'replyContent': str,
#     }
    
#     client = get_minio_client()
    
#     client.fget_object(bucket_name=bucket_name, 
#                        object_name=file_name, 
#                        file_path=file_name)
       
#     dataset = pd.read_csv(file_name, dtype=dtypes, parse_dates=['at', 'repliedAt'])
    
#     print('column before clearing')
#     print(dataset['content'].head())
    
#     dataset['content'] = dataset['content'].str.replace(r"[^\p{L}\p{N}\p{P}\s]+", ' ')
    
#     print('column after clearing')
#     print(dataset['content'].head())
    
#     csv_buffer = BytesIO()
#     dataset.to_csv(csv_buffer, index=False)
#     csv_buffer.seek(0)
    
#     client.put_object(
#         bucket_name='data',
#         object_name=file_name,
#         data=csv_buffer,
#         length=-1,
#         part_size=10 * 1024 * 1024
#     )  


default_args = {
    'owner': 'artem',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


with DAG(
    dag_id='process_minio_objects',
    description='DAG that process data from Minio bucket',
    default_args=default_args,
    # startdate=datetime()
    schedule_interval='*/1 * * * *'
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
        
