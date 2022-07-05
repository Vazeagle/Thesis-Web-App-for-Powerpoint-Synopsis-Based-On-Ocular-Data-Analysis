var checker = document.getElementById('checkterms');
var sendbtn = document.getElementById('signupbtn');

var hover = 'button:hover {box-shadow: 0px 0px 15px 0px rgb(0 0 0 / 90%);}';
var style = document.createElement("style");

var username_flag = false; //not empty flag
var password_flag = false; //not empty flag
var email_flag = false;    //not empty flag
var password_ver_flag = false;
var email_ver_flag = false;
var checkbox_flag = false;


// when checker is unchecked or checked, run the function

checker.onchange = function(){
   
   if(this.checked){
      checkbox_flag = true;
      if(username_flag && password_flag && password_ver_flag && email_flag && email_ver_flag)
      {
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
         //var hover = 'button:hover {box-shadow: 0px 0px 15px 0px rgb(0 0 0 / 90%);}';
         //var style = document.createElement("style");
         style.appendChild(document.createTextNode(""));
         document.head.appendChild(style);
         style.sheet.insertRule(hover);
      }
   }
   else {
      checkbox_flag=false;
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default';
      style.sheet.removeRule(0);
   }

}

//Validate username based on regular expression
var validate_usr = function()
{
   var username = document.getElementById('username').value;
   var regex = /^[0-9a-zA-Z]{7,}$/
   if(regex.test(username))
   {
      document.getElementById('username_message').innerHTML = '';
      username_flag = true;
      if(checkbox_flag && password_flag && password_ver_flag && email_flag && email_ver_flag)
      {
         //re-enable button
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
      }
      
   }
   else
   {
      document.getElementById('username_message').style.color = 'red';
      document.getElementById('username_message').innerHTML = 'The username must contain at least have 7 characters'
      username_flag = false
      //disable button
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default';
      style.sheet.removeRule(0);
   }
}


//Validate password based on regular expression
var validate_password = function()
{
   var regex =  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/
   var password = document.getElementById('password').value;
   if(regex.test(password))
   {
      document.getElementById('password_message').innerHTML = '';
      password_flag = true;
      if(checkbox_flag && username_flag && password_ver_flag && email_flag && email_ver_flag)
      {
         //re-enable button
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
      }
   }
   else
   {
      document.getElementById('password_message').style.color = 'red';
      document.getElementById('password_message').innerHTML = 'The password must contain at least 8 characters,at least one number, at least one upper case and one lower case character!,';
      password_flag = false
      //disable button
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default';
      style.sheet.removeRule(0);
   }
   confirm_password();//We call again this function because the user could, after having the script confirm the equality of the values, change the initial value and the button would still be visible so we call the function again to recheck. One other way is if we could put in the element alert "onkeyup" the two scripts which isn't do-able
}


var confirm_password = function()
{
   //password confirmation check
   if (document.getElementById('password').value == document.getElementById('verify-password').value)
   {
      document.getElementById('password_ver_message').innerHTML = '';
      password_ver_flag = true;

      if(checkbox_flag && username_flag && password_flag && email_flag && email_ver_flag)
      {
         //re-enable button
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
      }
   }
   else {
      document.getElementById('password_ver_message').style.color = 'red';
      document.getElementById('password_ver_message').innerHTML = 'Password not matching';
      password_ver_flag = false;
      //disable button
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default';
      style.sheet.removeRule(0);
   }
}

//Validate email based on regular expression
var validate_email = function()  {
   var email = document.getElementById('email').value; 
   var regex = /^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/
   if(regex.test(email))
   {
      document.getElementById('email_message').innerHTML = '';
      email_flag = true;
      if(checkbox_flag && username_flag && password_flag && password_ver_flag && email_ver_flag)
      {
         //re-enable button
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
      }
   }
   else
   {
      document.getElementById('email_message').style.color = 'red';
      document.getElementById('email_message').innerHTML = 'Invalid mail';
      email_flag = false
      //disable button
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default'
      style.sheet.removeRule(0);
   }
   confirm_email(); //We call again this function because the user could, after having the script confirm the equality of the values, change the initial value and the button would still be visible so we call the function again to recheck. One other way is if we could put in the element alert "onkeyup" the two scripts which isn't do-able
}

var confirm_email = function()
{
   //password confirmation check
   if (document.getElementById('email').value == document.getElementById('verify-email').value)
   {
      document.getElementById('email_ver_message').innerHTML = '';
      email_ver_flag = true;

      if(checkbox_flag && username_flag && password_flag && password_ver_flag && email_flag)
      {
         //re-enable button
         sendbtn.disabled = false;
         sendbtn.style.background='#3A5FBB';
         sendbtn.style.cursor='pointer';
      }
   }
   else {
      document.getElementById('email_ver_message').style.color = 'red';
      document.getElementById('email_ver_message').innerHTML = 'Email not matching';
      email_ver_flag = false;
      //disable button
      sendbtn.disabled = true;
      sendbtn.style.background='#A9A9A9';
      sendbtn.style.boxShadow=null
      sendbtn.style.cursor='default';
      style.sheet.removeRule(0);
   }
}

function message_load() {
	var signupmsg = document.getElementById('signup_message').innerHTML;
	if(signupmsg == ''){
		document.getElementById('signup_message').style.display = "none"
	}
	else if(signupmsg == 'Email already used!'){
		document.getElementById('signup_message').style.display = "inline"
	}
   else if(signupmsg == 'Username already taken!'){
		document.getElementById('signup_message').style.display = "inline"
	}
   else if(signupmsg == 'Email already used and username already taken!'){
		document.getElementById('signup_message').style.display = "inline"
	}
   else if(signupmsg == 'You have successfully signed-up!'){
      document.getElementById('signup_message').style.borderColor  = "green"
      document.getElementById('signup_message').style.backgroundColor = "rgba(0, 128, 0, 0.247)"
		document.getElementById('signup_message').style.display = "inline"
	}
	else{
		document.getElementById('signup_message').style.display = "none"
	}
}