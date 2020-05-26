import os
import uuid
import time
import json
import logging

from multiprocessing import Process

from kafka import KafkaConsumer, TopicPartition
from simulation import start_trip_simulation


logger = logging.getLogger('event_simulator_web')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


class TripSimulatorWorker(object):

    def __init__(self, group_id, partition):
        self.group_id = group_id
        self.partition = partition

        def initialize():
            self.broker = os.environ.get('BROKER_URL')
            self.queue = os.environ.get('QUEUE')
            self.topic = self.queue
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.broker,
                value_deserializer=json.loads,
            )
            self.consumer.assign([TopicPartition(self.topic, partition)])

        while True:
            try:
                initialize()
                break
            except Exception as e:
                self.log('Worker init error: {}'.format(str(e)))
                self.log('Retries in 2 seconds...')
                time.sleep(2)

    def run(self):
        self.log('Broker: %s' % self.broker)
        self.log('Queue: %s' % self.queue)
        self.log('Group Id: %s' % self.group_id)
        self.log('Partition: %s' % self.partition)

        while True:
            try:
                msg = next(self.consumer)
                self.log(
                    'Recevied task from topic|partition: {}|{}'.format(
                        msg.topic, msg.partition
                    )
                )
                start_trip_simulation(msg.value, self.log)
            except Exception as e:
                self.log('Worker consume error: {}'.format(str(e)))
                self.log('Retries in 2 seconds...')
                time.sleep(2)

    def log(self, msg):
        logger.info('worker: {}  | {}'.format(self.partition, msg))


def main(group_id, partition):
    worker = TripSimulatorWorker(group_id, partition)
    worker.run()


if __name__ == '__main__':
    concurrency = int(os.environ.get('CONCURRENCY'))
    group_id = str(uuid.uuid4())
    for partition in range(concurrency):
        Process(target=main, args=(group_id, partition)).start()
