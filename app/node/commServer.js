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
	fs = require('fs');
	mysql = require('mysql'),
	squel = require('squel'),
    zmq = require('zmq'),
	conn = zmq.socket('req'),
	app = express();

/*
*Here is where I setup the sql connection and the query preparations 
*/

//sql connection parameters
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  database : 'node',
  password : ''
});

connection.connect();

//Prepare statements using Squel
var query = squel.select().from("user");


//Declare variables and the environment
var ZMQ_REQ_ADDR = "tcp://*:9992";
var msg = {command:""}; //This is the template for the switch Command

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


//Eclipse Will handle http get requests here. I can make it more
//secure but that will happen laterI will push mysql data queries using the url


// This will handle whois 
app.get('/huryu', function (req, res) {
	res.send("{'id':'000001'}");
});

// This will send a reset signal to the python code, which will set all switches off
app.get('/reset', function (req, res) {
	conn.send("{'command':'reset'}");
	res.send('Sent reset command');
});

//This will access the nodejs output file to look at the device output in case of errors
app.get('/serverLog', function (req, res) {
	console.log("Accessing Server Log File");
	fs.readFile('./output_node.txt', function (err, data) {
  		if (err) throw err;
  		res.send(data.toString());
	});
});

//This will access the python log file to assess the python code health and see if the device
//is performing optimally
app.get('/deviceLog', function (req, res) {
	console.log("Accessing Device Log File");
	fs.readFile('./logs.log', function (err, data) {
  		if (err) throw err;
  		res.send(data.toString());
	});
});

//This listener will wait for the sensorData command and get sensor Data to the frontend
app.get('/sensorData', function (req, res) {
	console.log("Getting sensor Data");
	connection.query(query.toString(), function(err, rows, fields) {
  		if (err) throw err;
		res.send(rows);
	});
});

//This will run the login authentification hiding it from the frontend
app.get('/login', function (req, res) {
	console.log("Logging in User");
	var name = req.query.name;
	var pass = req.query.pass;
	if(name == "admin" && pass == "adminPass")
		res.send('accepted');
	else res.send('rejected');
});

//This is a simple ping pong function to test the server
app.get('/ping', function (req, res) {
	console.log("Recieved Pong");
	res.send('pong');
});

//This will save the configuration file and send result to restart
app.get('/saveConfig', function (req, res) {
	if(req.query.data == 'Err') {res.send('Err');return;}
	console.log("Saving Configuration");
	var conf = req.query.data;
	fs.writeFile('example.json', req.query.data, function (err) {
  		if (err) throw err;
  		console.log('Saved!');
	});
	//Start switching commands
	msg.command="switchCircuit";
	for (i in conf.matches){
		console.log(i);
		//msg.circuitNo = i.indexOf(i);
		//msg.sourceNo = i;
		//conn.send(msg);
	}
	msg.circuitNo = 1;
	msg.sourceNo = 1;
//	conn.send(msg);
	console.log(msg)
	res.send('Saved');
});


// start http server
app.listen(httpPort, function () {
    console.log('HTTP Server: http://localhost:' + httpPort);
});