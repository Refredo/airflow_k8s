from airflow.models import Variable
from kafka import KafkaProducer
from kafka.errors import KafkaError
import requests
import datetime
import json

# from dotenv import load_dotenv
# import os

# load_dotenv(verbose=True)

# API_KEY = os.getenv('API_KEY') 

def get_API_data():

    API_KEY = Variable.get('API_KEY')
    print(API_KEY)
    
    location = 'toronto'
    headers = {"accept": "application/json"}

    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={API_KEY}"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f'data was fetched successfully for {datetime.datetime.now()}')
        return result
    
    
def get_kafka_producer():
    user = Variable.get('sasl_plain_username')
    password = Variable.get('sasl_plain_password')
    
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        key_serializer=lambda x: x.encode('utf-8'),
        acks='all',
        linger_ms=1000,
        request_timeout_ms = 60000,
        api_version=(2, 6, 0),
        connections_max_idle_ms=1000000,
        security_protocol="SASL_PLAINTEXT",  
        sasl_mechanism="PLAIN",              
        sasl_plain_username=user,        
        sasl_plain_password=password
        # sasl_plain_password="zXN0F7Mmr5"       
        )
    
    if producer.bootstrap_connected():
        print('Connection to Kafka was successfull')
    else:
        print('Failed to connect to Kafka')
    return producer



def put_weather_info():
    
    print('Start')
    
    data = get_API_data()
    producer = get_kafka_producer()
    
    topic = 'weather_info'
    
    future = producer.send(topic=topic, value=data, key='key')
    
    producer.flush()
    
    try:
        record_metadata = future.get(timeout=100)
        
        print("Message sent successfully to topic:", record_metadata.topic)
        print("Message sent to partition:", record_metadata.partition)
        print("Message offset:", record_metadata.offset)
        
    except KafkaError as e:
        print("Failed to send message:", str(e))
    
    producer.close()


