import os
import json

from producer.kafka import get_producer


TRIP_SIMULATION_TOPIC = os.environ.get('TRIP_SIMULATION_TOPIC')
NUM_OF_PARTITIONS = int(os.environ.get('NUM_OF_PARTITIONS'))
NUM_OF_RECORDS = 0


def fire_trip_simulation_event(operator_name, shuttle_identifier, polyline):
    global NUM_OF_RECORDS

    producer = get_producer()
    if producer:
        data = {
            'operator_name': operator_name,
            'shuttle_identifier': shuttle_identifier,
            'polyline': polyline,
        }
        partition = NUM_OF_RECORDS % NUM_OF_PARTITIONS
        producer.send(
            TRIP_SIMULATION_TOPIC,
            json.dumps(data).encode(),
            partition=partition
        )
        NUM_OF_RECORDS += 1
        return True
    return False
