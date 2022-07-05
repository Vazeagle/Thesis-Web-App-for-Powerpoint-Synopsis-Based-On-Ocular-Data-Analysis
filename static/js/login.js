//$(".options-02 a").click(function () {
//	$("form").animate(
//	  {
//		height: "toggle",
//		opacity: "toggle"
//	  },
//	  "slow"
//	);
//  });
//

// This function will be called every time the html body will be loaded
//This fynction makes invisible the login message if there is none and visible if it is
//the message is being given by flask in /login route to a div's inner html {{msg}}
function message_load() {
	var loginmsg = document.getElementById('login_message').innerHTML;
	const myArray = loginmsg.split(" ");
	if(loginmsg == ''){
		document.getElementById('login_message').style.display = "none"
	}
	else if(loginmsg == 'Invalid Email OR Password !'){
		document.getElementById('login_message').style.display = "inline"
	}
	else if(myArray[1]== 'successfully' && myArray[2]== 'logged'&& myArray[3]== 'out!'){
		document.getElementById('login_message').style.borderColor  = "green"
		document.getElementById('login_message').style.backgroundColor = "rgba(0, 128, 0, 0.247)"
		document.getElementById('login_message').style.display = "inline"
	}
	else {
		document.getElementById('login_message').style.display = "none"
	}
}
