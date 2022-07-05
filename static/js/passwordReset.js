function message_load() {
	var loginmsg = document.getElementById('login_message').innerHTML;
	if(loginmsg == ''){
		document.getElementById('login_message').style.display = "none"
	}
	else if(loginmsg == 'Invalid Email.'){
		document.getElementById('login_message').style.display = "inline"
	}
	else{
		document.getElementById('login_message').style.display = "none"
	}
}