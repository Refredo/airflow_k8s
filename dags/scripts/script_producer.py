from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import requests
import json


def get_API_data():
    response = requests.get('https://randomuser.me/api/')
    
    if response.status_code == 200:
        result = response.json()['results'][0]
        return result


def transform_data(data) -> dict:
    dct = {}
    dct['full_name'] = data['name']['title'] + ' ' + data['name']['first'] + ' ' + data['name']['last']
    dct['gender'] = data['gender']
    dct['location'] = data['location']['street']['name'] + ' ' + str(data['location']['street']['number'])
    dct['city'] = data['location']['city']
    dct['country'] = data['location']['country']
    dct['postcode'] = data['location']['postcode']
    dct['latitude'] = float(data['location']['coordinates']['latitude'])
    dct['longitude'] = float(data['location']['coordinates']['longitude'])
    dct['email'] = data['email']

    return dct

def get_kafka_producer():
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
        sasl_plain_username="user1",        
        sasl_plain_password="zXN0F7Mmr5"       
        )

    if producer.bootstrap_connected():
        print("KafkaProducer connected successfully.")
    else:
        print("Failed to connect to KafkaProducer.")
    return producer


def start_streaming():
    
    data = transform_data(get_API_data())
    print(data)
    
    producer = get_kafka_producer()

    future = producer.send('random_namess', value=data, key='key')
    
    producer.flush()

    try:
        record_metadata = future.get(timeout=100)

        print("Message sent successfully to topic:", record_metadata.topic)
        print("Message sent to partition:", record_metadata.partition)
        print("Message offset:", record_metadata.offset)
    except KafkaError as e:
        print("Failed to send message:", str(e))
    
    producer.close()


if __name__ == '__main__':
    
    start_streaming()
    
    # consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])
    
    # print(topics)
     
     