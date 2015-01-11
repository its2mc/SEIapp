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
	var msg = {
		command:""
	};
	
	$("#login").click(function(){
		var name = $("#accountName").val();
		var pass = $("#accountPassword").val();
		if(name == "admin" && pass == "adminPass")
			window.location.replace("./pages/controlPanel.html");
		else
			alert("Login Details Wrong!");
	});
	
	$("#switchBtn").click(function(){
		alert($("#circuitNo").val());
		alert($("#sourceNo").val());
		msg.command="switchCircuit";
		msg.circuitNo = $("#circuitNo").val();
		msg.sourceNo = $("#sourceNo").val();
		websocket.send(JSON.stringify(msg));
	});
});