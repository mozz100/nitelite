var express    = require('express');
var bodyParser = require('body-parser');
var app        = express();
var net        = require('net');
var sockfile   = '/tmp/communicate.sock';
var faye       = require('faye');
var bayeux     = new faye.NodeAdapter({mount: '/faye', timeout: 45});
var fayeClient = bayeux.getClient();

// Inter-process communications with the python process
var client = net.connect( { path: sockfile });
client.on('connect', function () {
    console.log('client connected');
    client.write('hello');
});
client.on('data', function (data) {
    newState = data.toString();
    console.log('data', newState);
    fayeClient.publish('/state', { state: newState });
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
app.use('/js',               express.static('js'));
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
bayeux.attach(server);