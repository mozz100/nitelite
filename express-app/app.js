var express    = require('express');
var bodyParser = require('body-parser');
var app        = express();
var net        = require('net');
var sockfile   = '/tmp/communicate.sock';

// Inter-process communications with the python process
var client = net.connect( { path: sockfile });
client.on('connect', function () {
    console.log('client connected');
    client.write('hello');
});
client.on('data', function (data) {
    console.log('data', data.toString());
});
client.on('error', function (err) {
    console.error('error', err);
});
client.on('end', function () {
    console.log('client disconnected');
    // reconnect
    client = net.connect( { path: sockfile });
});

// Define Express app
app.use('/',                 express.static('pages'));
app.use('/bower_components', express.static('bower_components'));
app.use('/css',              express.static('css'));
app.use(bodyParser.urlencoded());
app.post('/state', function(req, res) {
    client.write(req.body.state);
    res.redirect('/');
});

// Start up the server
var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('nitelite js app listening at http://%s:%s', host, port);
});