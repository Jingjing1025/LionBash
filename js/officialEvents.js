var apigClient = apigClientFactory.newClient({
    accessKey: '',
    secretKey: ''
});


function detectIP(){

  var IP = document.getElementById("gfg").textContent;

    if (IP.length == 0){
      location.reload();
    }
console.log("im here")

returnQuery()

}

function returnQuery() {

  var params = {};
  var additionalParams = {};
  var body = {
    "EventCategory" : "official"
    };

    apigClient.createEventsPost(params, body, additionalParams)
      .then(function(result){

        var res = JSON.parse(result['data']['body']);
        console.log(res)

        var counter = 0;

        for (var key in res) {
            obj = res[key];
            console.log(obj);

            counter = counter + 1;

            EventName1 = obj['Name'];
            EventDetails1 = obj['Detail'];
            EventLocation1 = obj['Location'];
            EventDate1 = obj['Date'];
            EventPhoto1 = obj['Photo'];

            console.log("event name is " + String(EventName1));

            var photo_data1 = "https://b2homework3.s3.amazonaws.com/"+EventPhoto1;
            console.log(photo_data1);
            var img1 = new Image();
            img1.src = photo_data1;
            img1.setAttribute("class", "banner-img");
            img1.setAttribute("alt", "effy");

            console.log("Start creating blocks");

            var div0 = document.createElement('div');
            div0.className = "col-lg-4";
            var div1 = document.createElement('div');
            div1.className = "tm-bg-black-transparent tm-about-box";

            console.log(div0.className);
            
            var div2 = document.createElement('div');
            div2.className = "tm-about-number-container";
            var divtext = "0." + String(counter);
            var seq1 = document.createTextNode(divtext);
            div2.appendChild(seq1);

            var h3 = document.createElement('h3');
            var name = "EventName" + String(counter);
            h3.id = name;
            h3.className = "tm-about-name";
            var nbsp = document.createTextNode("&nbsp;");
            h3.appendChild(nbsp);

            console.log(h3);

            var div3 = document.createElement('div');
            div3.className = "banner-section";
            var contname = "img-container" + String(counter);
            div3.id = contname;

            var p1 = document.createElement('p');
            var location = "EventLocation" + String(counter);
            p1.id = location;
            p1.className = "tm-about-description";
            p1.appendChild(nbsp);

            var p2 = document.createElement('p');
            var date = "EventDate" + String(counter);
            p2.id = date;
            p2.className = "tm-about-description";
            p2.appendChild(nbsp); 

            var p3 = document.createElement('p');
            var detail = "EventDetails" + String(counter);
            p3.id = detail;
            p3.className = "tm-about-description";
            p3.appendChild(nbsp);

            var div4 = document.createElement('div');
            div4.className = "text-center";
            var addbtn = document.createElement('button');
            addbtn.type = "button";
            addbtn.value = counter;
            addbtn.className = "btn btn-tertiary tm-btn-app-feature";
            addbtn.setAttribute("onclick", addEvent);
            addbtn.onclick = addEvent;
            var addtext = document.createTextNode("ADD");
            addbtn.appendChild(addtext);
            div4.appendChild(addbtn);

            console.log(div4);

            div1.appendChild(div2);
            div1.appendChild(h3);
            div1.appendChild(div3);
            div1.appendChild(p1);
            div1.appendChild(p2);
            div1.appendChild(p3);
            div1.appendChild(div4);

            div0.appendChild(div1);

            var currentSec = document.getElementById("tmAbout");
            currentSec.appendChild(div0);

            console.log("all divs created");

            document.getElementById(contname).appendChild(img1);
            document.getElementById(contname).style.display = "block";

            document.getElementById(name).innerHTML = EventName1;
            document.getElementById(detail).innerHTML = 'Details : ' + EventDetails1;
            document.getElementById(location).innerHTML = 'Location : ' + EventLocation1;
            document.getElementById(date).innerHTML = 'Date : ' + EventDate1;


        };


      }).catch( function(result){
        	console.log("Inside Catch Function");
      });

}



function addEvent(event) {
    console.log(this.value);
    console.log("im adding events1");

    var count = this.value;
    var name = "EventName" + String(count);
    console.log(name);

    var eventname = document.getElementById(name).textContent;
    console.log(eventname);

    var params = {};
    var additionalParams = {};
    var body = {
    "EventIP" : document.getElementById("gfg").textContent,
    "EventName" : eventname
    };

    console.log(body)

    apigClient.createEventsPost(params, body, additionalParams)
      .then(function(result){
        console.log("inside post1")
      }).catch( function(result){
            console.log("Inside Catch Function");
      });
}
