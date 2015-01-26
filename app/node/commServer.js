/* 
* This work has been done by Phillip Ochola Makanyengo
* Email: its2uraps@gmail.com
*
* This work uses open source code and libraries and 
* can therefore be replicated unless certain portions
* are stated otherwise. 
*
* Please refer to the author when using the code.
*
*/

//Nodejs server implementation for the Ihub my energy project

/* 
This cloud app implements zeromq for cross device communication,
mongodb for data storage, will consider other technologies and 
modules for data analysis. This server handles interactivity with
the device, such as sending commands to control switches and recieving 
status updates from the device. The app is designed to be non-Blocking.
*/

//Importing all the modules
var express = require('express'),
    path = require('path'),
    httpPort = 8080,
	wsPort = 5678,
//	mysql = require('mysql'),
//	squel = require('squel'),
    zmq = require("zmq"),
	conn = zmq.socket('req'),
	wsServer = require('ws').Server,
	app = express();
	
//Declare variables and the environment
var ZMQ_REQ_ADDR = "tcp://*:9992";

//This sets up the express environment, public is the folder containing the files
express.static.mime.default_type = "text/html";
app.use(express.static(path.join(__dirname, 'public')));

/*
*	The request reply socket only passes messages from the webpage to the rpi
*	No processing happens on the nodejs server, this is to minimize cpu
*	consumption
*	Request and recieve replies
*/
conn.identity = 'server' + process.pid;

conn.bind(ZMQ_REQ_ADDR,function(err){
	if (err) throw err;
	console.log("ZMQ-Request server started\n");
});

var wss = new wsServer({
        port: wsPort
    });

wss.on('connection', function (ws) {
	console.log("WS Server: ws://localhost:"+ wsPort);
    ws.on('message', function (message) {
		console.log(message);
		conn.send(message);
    });
	conn.on('message', function(data){
		for (var i in wss.clients){
       		wss.clients[i].send(data);
		}
	});
});

// start http server
app.listen(httpPort, function () {
    console.log('HTTP Server: http://localhost:' + httpPort);
});