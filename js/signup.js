var apigClient = apigClientFactory.newClient({
    accessKey: '',
    secretKey: ''
});

//var messages = "";
//AWS.config.region = 'us-east-1'
function Response1() {

  var params = {};
  var additionalParams = {};
  var body = {
       "userId": document.getElementById("uni").value,
       "password": document.getElementById("password").value,
       "phone_number": document.getElementById("phone_number").value,
       "ip": document.getElementById("gfg").textContent,
       "type": "signup"
    };
    console.log(body)
    apigClient.signupLoginPost(params, body, additionalParams)
      .then(function(result){

      var returnMessage = result['data']['body']

      if(returnMessage== "AccountExisted"){
         popUpWindow("Account with this name already exists!");
      }
      else if (returnMessage =="SignUpSuccess"){
         popUpWindow("SignUp is successful! You are now logged in!");
         window.location.href='index.html';
      }
      }).catch( function(result){
          console.log("Inside Catch Function");
      });
}

//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    //runs this function when enter is pressed
    newEntry();
  }
}

//clears the placeholder text ion the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}

function popUpWindow(responseMessage){
  alert(responseMessage)
}

function getAlert(){
   alert("message gotten!");
}
