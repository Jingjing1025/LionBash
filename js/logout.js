var apigClient = apigClientFactory.newClient({
    accessKey: '',
    secretKey: ''
});

//var messages = "";
//AWS.config.region = 'us-east-1'
function Response() {

  var params = {};
  var additionalParams = {};
  var body = {
       "ip":document.getElementById("gfg").textContent
    };
    console.log(body)
    apigClient.logoutPost(params, body, additionalParams)
      .then(function(result){
      
      var returnMessage = result['data']['body']
      
      if(returnMessage== "Success"){
         popUpWindow("You have successfully logged out!");
      }
      else if(returnMessage=="Fail"){
        popUpWindow("You must sign in first!");
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