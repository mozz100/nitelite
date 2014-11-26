var express      = require('express');
var bodyParser   = require('body-parser');
var app          = express();
var jf           = require('jsonfile');
var net          = require('net');
var sockfile     = '/var/nitelite/communicate.sock';
var settingsfile = '/var/nitelite/settings.json';
var faye         = require('faye');
var bayeux       = new faye.NodeAdapter({mount: '/faye', timeout: 45});
var fayeClient   = bayeux.getClient();
var state        = '';
var settings;

jf.readFile(settingsfile, function(err, obj) {
    if (err) {
        settings = {
            times: {
                nitetime: "19:00",
                litetime: "06:45",
                offtime:  "07:30"
            }
        }
    } else {
        settings = obj;
    }
});

// Inter-process communications with the python process
var client = net.connect( { path: sockfile });
client.on('connect', function () {
    console.log('client connected');
    client.write('hello');
});
client.on('data', function (data) {
    state = data.toString();
    console.log('data', state);
    fayeClient.publish('/state', { state: state });
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
app.get('/state', function(req, res) {
    res.send({state: state});
});
app.post('/times', function(req, res) {
    settings.times.nitetime = req.body.nitetime;
    settings.times.litetime = req.body.litetime;
    settings.times.offtime  = req.body.offtime;
    jf.writeFileSync(settingsfile, settings);
    fayeClient.publish('/times', settings.times);
    res.send(settings.times);
});
app.get('/times', function(req, res) {
    res.send(settings.times);
});

// Start up the server
var server = app.listen(80, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('nitelite js app listening at http://%s:%s', host, port);
});
bayeux.attach(server);
