var WebSocketServer = require('websocket').server;
var http = require('http');

const KAFKA_URL = process.env.KAFKA_URL;
const DRIVING_ANALYTICS_TOPIC = process.env.DRIVING_ANALYTICS_TOPIC;

var kafka = require('kafka-node');
var Consumer = kafka.Consumer,
  client = new kafka.KafkaClient({kafkaHost: KAFKA_URL}),
  drivingAnalyticsConsumer = new Consumer(
    client,
    [],
    // [{topic: DRIVING_ANALYTICS_TOPIC, partition: 0}],
    {autoCommit: false}
  );

function addTopicsToConsumer() {
  drivingAnalyticsConsumer.addTopics([
    {topic: DRIVING_ANALYTICS_TOPIC, partition: 0}
  ], () => console.log('topic added'));
};
setTimeout(addTopicsToConsumer, 10000);

var server = http.createServer(function(request, response) {
  console.log('Request recieved : ' + request.url);
  response.writeHead(404);
  response.end();
});
server.listen(8081, function() {
  console.log('Listening on port: 8081');
});

webSocketServer = new WebSocketServer({
  httpServer: server,
  autoAcceptConnections: false
});

function iSOriginAllowed(origin) {
  return true;
}

webSocketServer.on('request', function(request) {
  if (!iSOriginAllowed(request.origin)) {
    request.reject();
    console.log('Connection from : ' + request.origin + ' rejected.');
    return;
  }

  var connection = request.accept('echo-protocol', request.origin);
  console.log('Connection accepted : ' + request.origin);

  connection.on('message', function(message) {
    if (message.type === 'utf8') {
      console.log('Received Message: ' + message.utf8Data);
    }
  });

  drivingAnalyticsConsumer.on('message', function (message) {
    console.log(message);
    connection.sendUTF(message.value);
  });

  connection.on('close', function(reasonCode, description) {
    console.log('Connection ' + connection.remoteAddress + ' disconnected.');
  });
});
