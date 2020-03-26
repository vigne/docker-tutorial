//source https://nodejs.org/de/docs/guides/nodejs-docker-webapp/

'use strict';

const express = require('express');
var cors = require('cors');

// Constants
const PORT = 8000;
const HOST = '0.0.0.0';

// App
const app = express();
app.use(cors());

app.get('/helloworld', (req, res) => {
  res.json({'message': "Hello World, from your REST-Api. Please implement me!"});
});

app.listen(PORT, HOST);