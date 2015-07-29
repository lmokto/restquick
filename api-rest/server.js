var restify = require('restify');
var zmq = require('zmq');
var requester = zmq.socket('req');
var r = require('bunyan')
var q = require('q');

var l = new r({ 'name': 'test', 'level': 'info' })
l.info('test info message')

requester.connect("tcp://localhost:5555");

var srv = restify.createServer();

srv.pre(restify.pre.userAgentConnection());
srv.use(restify.queryParser());

srv.get('/', function (req, res, next) {
    res.send({hello: 'world'});
    next();
});

var resolver = function(lat, lng){
	return q.Promise(function(resolve, reject, notify){
	    requester.send(lat+"::"+lng);
		requester.on("message", function(reply) {
			resolve(JSON.parse(reply.toString()))
		})
	})
}

srv.post('/', function (req, res, next) {
	console.log(req.params);
	resolver(req.params.lat, req.params.lng)
	.done(function(result){
		res.send({Estaciones: result})
		return next();
	}, function(err){
        if(err) console.log(err)
	})
});

process.on('SIGINT', function() {
  requester.close();
});

process.setMaxListeners(100);

srv.listen(8080, function () {
    console.log('ready on %s', srv.url);
});