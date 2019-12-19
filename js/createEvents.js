var apigClient = apigClientFactory.newClient({
    accessKey: '',
    secretKey: ''
});
var albumBucketName = "b2homework3";
var bucketRegion = "us-east-1";
var albumName = "myAlbum";

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: "us-east-1:684d69b7-7b27-4938-9335-97744d0f8da9"
  })
});

//var messages = "";
var lastUserMessage = "";
//AWS.config.region = 'us-east-1'

function uploadPhoto() {
  var files = document.getElementById("file_path").files;
  if (!files.length) {
    return alert("Please choose a file to upload first.");
  }
  var file = files[0];
  var fileName = file.name;
  var albumPhotosKey = encodeURIComponent(fileName);
  var photoKey = fileName;
  // Use S3 ManagedUpload class as it supports multipart uploads
  var upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: albumBucketName,
      Key: photoKey,
      Body: file,
      ACL: "public-read"
    }
  });

  var promise = upload.promise();

  promise.then(
    function(data) {
      alert("Successfully uploaded photo.");
    },
    function(err) {
      console.log(err.message)
      return alert("There was an error uploading your photo: ", err.message);
    }
  );
}


function response() {

  var creator = document.getElementById('EventCreator').value
  var name = document.getElementById('EventName').value
  var category = document.getElementById('EventCategory').value
  var date = document.getElementById('EventDate').value
  var time = document.getElementById('EventTime').value
  var location = document.getElementById('EventLocation').value
  var details = document.getElementById('EventDetails').value
  var phone = document.getElementById('EventPhone').value
  var photo = document.getElementById('EventPhoto').value

  var params = {};
  var additionalParams = {};
  var body = {
    "EventCreator": creator,
    "EventName": name,
    "EventCategory": category,
    "EventDate": date,
    "EventTime": time,
    "EventLocation": location,
    "EventDetails": details,
    "EventPhone": phone,
    "EventPhoto": photo
    };

    apigClient.createEventsPost(params, body, additionalParams)
      .then(function(result){
        console.log("Inside post");
        //alert(lastUserMessage+" response");
        //returnMessage = String(result['data']);
        var returnMessage = result['data']['body']
      if(returnMessage){
         popUpWindow("Event is created successfully!");
      }
      else if (returnMessage== "Missing"){
         popUpWindow("Parameters missing! Please double-check your entries!");
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
