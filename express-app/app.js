var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var net = require('net');
var sockfile = '/tmp/communicate.sock';

var client = net.connect( { path: sockfile });

app.use('/',                 express.static('pages'));
app.use('/bower_components', express.static('bower_components'));
app.use('/css',              express.static('css'));
app.use(bodyParser.urlencoded());
app.post('/state', function(req, res) {
    client.write('state change');
    console.log(req.body);
    client.write(req.body.state);
    res.redirect('/');
});

client
  .on('connect', function () {
    console.log('client connected');
    client.write('hello server');
  })
  .on('data', function (data) {
    console.log('Data: %s', data.toString());
    client.end();
  })
  .on('error', function (err) {
    log.error('client', err);
  })
  .on('end', function () {
    console.log('client disconnected');
  })
  ;

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});