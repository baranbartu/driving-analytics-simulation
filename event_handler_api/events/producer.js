'use strict';

const KAFKA_URL = process.env.KAFKA_URL;
var kafka = require('kafka-node'),
  client = new kafka.KafkaClient({kafkaHost: KAFKA_URL}),
  kafkaProducer = new kafka.Producer(client);


const producer = {
  send: function (data, topic) {
    const payloads = [
        { topic: topic, messages: JSON.stringify(data)},
    ];
    kafkaProducer.send(payloads, function (err, data) {
    });
  }
}
module.exports = producer;
