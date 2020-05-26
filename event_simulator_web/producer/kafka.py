import os
from kafka import KafkaProducer

KAFKA_URL = os.environ.get('KAFKA_URL')

PRODUCER = None

def get_producer():
    global PRODUCER

    if not PRODUCER:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_URL)
            PRODUCER = producer
        except:
            producer = None

    return PRODUCER
