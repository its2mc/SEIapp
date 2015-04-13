/* 
* This work has been done by Phillip Ochola Mak'Anyengo
* as part of the Smart Energy Integrator Project together
* with Frankline Mogoi.
* 
* Email: its2uraps@gmail.com
*
* This work uses open source code and open use libraries
* but the application itself is neither open source or 
* allowed for open use. 
* 
* Users who wish to use parts of this
* work MUST contact the authors before use, failure to which
* the user can be prosecuted.
*
*/


$().ready(function(){
//Declared variables here
	var msg = {
		command:""
	};
	
//Here is where I will put all global my functions.
	
	//This function will check the inputs to make sure that the configuratiosn are within the limits
	function saveConfig(){
		/* THIS IS TEST CODE I HOPE WILL WORK*/
		//this is the supposed circuit configuration file
		var conf = {
				app:"SEI",
				user: "admin",
				technician: "adminTech",
				lastDateSet : "01/01/2015",
				circuits: {
					1:"circuit1",
					2:"circuit2",
					3:"circuit3"
				},
				sources: {
					1:"source1",
					2:"source2",
					3:"source3"
				},
				matches: {
				}
		};
		//This loop will clean the inputs, check if values are null and out of range
		var tempCircuit;
		var tempSource;
		var valCircuit=0; //holds the value of the circuit to make match
		var valSource; //holds value of source to make match
		var tempMatch ="0:matches";
		
		for(var i=1;i<4;i++){
			//This if statements check if the values are empty
			if( $("#"+conf.circuits[i]).val() == '' ){
				alert('Please Input Value between 0 and 300');
				$("#"+conf.circuits[i]).focus();
				return "Err";
			}
			if( $("#"+conf.sources[i]).val() == ''){
				alert('Please Input Value between 0 and 1000');
				$("#"+conf.sources[i]).focus();
				return "Err";
			}
			
			//This code gets integers from the input fields
			tempCircuit = parseInt($("#"+conf.circuits[i]).val())+0;
			tempSource = parseInt($("#"+conf.sources[i]).val())+0;
			
			//This if nest checks if the circuit values are integers between 0 and 300
			if(Number.isInteger(tempCircuit) && tempCircuit>0 && tempCircuit<300){
				valCircuit += tempCircuit;
			}
			//If not give alert and focus on wrong circuit value
			else{
				alert ("Power value should be between 0 and 300.");
				$("#"+conf.circuits[i]).focus();
				return "Err";
			}

			//Does the same but for sources
			if(Number.isInteger(tempSource) && tempSource>0 && tempSource<1000);
			//If not then alert and focus
			else{
				alert ("Power value should be between 0 and 1000.");
				$("#"+conf.sources[i]).focus();
				return "Err";
			}
			//This code here does the matching, it adds the current values for the circuits,
			//until it exceeds the supply source then goes to the next source
			var count=1;
			if(tempSource > valCircuit){
				tempMatch += "," + i + ":"+count;
			}
			else {
				count++;
				tempMatch += "," + i + ":"+count;
				valCircuit = 0;
			}
		}
		count=0;
		alert(tempMatch);
		conf.matches = '{'+tempMatch+'}';
		alert(conf.matches);
		return JSON.stringify(conf);
	}
	
	$("#accountName").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#accountPassword").focus();
	    }
	});
	
	$("#accountPassword").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#login").click();
	    }
	});
	
	$("#login").click(function(){
		var name = $("#accountName").val();
		var pass = $("#accountPassword").val();
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/login",
			data: "name="+name+"&pass="+pass,
			dataType: "text",
			success: function(res){
				if(res =="accepted"){
					$.ajax({
						type : "GET",
						url : "conf.json",
						dataType: "text",
						success: function(temp){
							alert("Welcome Home");
							window.location.replace("./pages/statistics.html");
						},
						error: function(xhr,status){
							alert("Device Not yet configured!");
							window.location.replace("./pages/config.html");
						}
					});
				}
				else
					alert("Password or Username wrong!");
			},
			error: function(xhr,status){
				alert("Cannot access Server" + JSON.stringify(xhr));
			}
		});
	});
	
/*	$("#switchBtn").click(function(){
		alert($("#circuitNo").val());
		alert($("#sourceNo").val());
		msg.command="switchCircuit";
		msg.circuitNo = $("#circuitNo").val();
		msg.sourceNo = $("#sourceNo").val();
		websocket.send(JSON.stringify(msg));
	});
	*/
	$("#sensorDataBtn").click(function(){
		var htmlObj = "";
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/sensorData",
			dataType: "json",
			success: function(temp){
				$("#title").html("Sensor Data");
				$("#body").html(JSON.stringify(temp));
			},
			error: function(xhr,status){
				$("#title").html("Sensor Data Error");
				$("#body").html(JSON.stringify(xhr));
			}
		});
	});
	
	$("#deviceLogBtn").click(function(){
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/deviceLog",
			dataType: "text",
			success: function(temp){
				$("#title").html("Device Log");
				$("#body").html(JSON.stringify(temp));
			},
			error: function(xhr,status){
				$("#title").html("Device Log Error");
				$("#body").html(JSON.stringify(xhr));
			}
		});
	});
	
	$("#serverLogBtn").click(function(){
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/serverLog",
			dataType: "text",
			success: function(temp){
				$("#title").html("Server log");
				$("#body").html(JSON.stringify(temp));
			},
			error: function(xhr,status){
				$("#title").html("Server log Error");
				$("#body").html(JSON.stringify(xhr));
			}
		});
	});
	
	$("#changeConfigBtn").click(function(){
		window.location.replace("./config.html");
	});
	
	$("#statsBtn").click(function(){
		window.location.replace("./statistics.html");
	});
	
	$("#pingBtn").click(function(){
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/ping",
			dataType: "text",
			success: function(temp){
				$("#outputPanel").html("Ping Success");
			},
			error: function(xhr,status){
				$("#outputPanel").html("Ping Failure");
			}
		});
	});
	
	$("#saveConfigBtn").click(function(){
		var configText = saveConfig();
		$.ajax({
			type : "POST",
			url : "http://localhost:8080/saveConfig",
			data: "data="+configText,
			dataType: "text",
			success: function(temp){
				if(temp=='Err') $("#outputPanel").html("Error Configuration not saved. Contact Administrator");
				else $("#outputPanel").html("Configuration Saved");
			},
			error: function(xhr,status){
				$("#outputPanel").html("Configuration Not Saved. Please Contact Administrator");
			}
		}); 
	});
	
	$("#resetBtn").click(function(){
		$.ajax({
			type : "GET",
			url : "http://localhost:8080/reset",
			dataType: "text",
			success: function(temp){
				$("#outputPanel").html("Reset Command Sent");
			},
			error: function(xhr,status){
				$("#outputPanel").html("Reset Command not Sent. Please Contact Administrator");
			}
		});
	});

});