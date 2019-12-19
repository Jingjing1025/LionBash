var apigClient = apigClientFactory.newClient({
    accessKey: '',
    secretKey: ''
});

//var messages = "";
//AWS.config.region = 'us-east-1'

function assignVariable(data){
    return data
}

function Response() {

  var params = {};
  var additionalParams = {};
//   var ip = "";
//   $.getJSON('https://json.geoiplookup.io/api?callback=?', function(data) {
//     ip = assignVariable(data["ip"]);
// });

  var body = {
       "userId": document.getElementById("uni").value,
       "password": document.getElementById("password").value,
       "ip": document.getElementById("gfg").textContent,
       "type": "login",
    };
    apigClient.signupLoginPost(params, body, additionalParams)
      .then(function(result){
      console.log("Inside response");
      var returnMessage = result['data']['body']
      console.log(returnMessage);
      if(returnMessage== "LoginTrue"){
         //window.location = "http://www.yoururl.com";
         popUpWindow("login successful!");
         window.location.href='index.html';
      }
      else if (returnMessage =="LoginFalse"){
         popUpWindow("Permission denied!");
      }
      else if (returnMessage =="NoAccount"){
         popUpWindow("No account available!");
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