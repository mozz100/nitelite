var express = require('express');
var app = express();
var net = require('net');
var sockfile = '/tmp/communicate.sock';

var client = net.connect( { path: sockfile });

app.use('/',                 express.static('pages'));
app.use('/bower_components', express.static('bower_components'));
app.use('/css',              express.static('css'));

app.post('/lite', function(req, res) {
    client.write('lite!');
    res.redirect('/');
});
app.post('/nite', function(req, res) {
    client.write('nite!');
    res.redirect('/');
});
app.post('/off', function(req, res) {
    client.write('off!');
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