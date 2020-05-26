'use strict';

const express = require('express');
const app = new express();
const bodyParser = require('body-parser');

// register JSON parser middleware
app.use(bodyParser.json());

require('./routes/api')(app);

app.listen(3000, '0.0.0.0', () => {
    console.log('Server is up & running!');
});
