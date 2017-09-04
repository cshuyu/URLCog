var express = require('express');
//var fs = require('fs');
var bodyParser = require('body-parser');
var app = express();
var completedTasks = [];

app.use(bodyParser.urlencoded({ extended: false, limit: '5mb' }));
app.use(bodyParser.json({limit: '5mb'}));

app.get('/', function (req, res) {
  console.log(JSON.stringify(req.headers));
  res.send('Hello World!');
});

app.post('/remote-detection', function (req, res) {
  try{
    //console.log(req.body);
    var data = JSON.parse(req.body.payload);
    console.log(data);

    //console.log("received "+data.length+" requests.");
    processRequest(data);
    res.send(JSON.stringify({
      size : data.length, 
      status:"succ"}));
  } catch(e) {
    console.error(e);
    res.send(JSON.stringify({status:"fail"}));
  }
});

app.get('/fetch-results', function (req, res) {
  //fetch-results
  try{
    console.log("fetch requests: "+completedTasks.length);
    res.send(JSON.stringify({
      size : completedTasks.length, 
      data : completedTasks,
      status:"succ"}));
    completedTasks = [];
  } catch(e) {
    res.send(JSON.stringify({status:"fail"}));
  }
});


//Start listening 3000
app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
  console.log('dir:'+__dirname);
});

var processRequest = function(data) {
  //Bogus function.
  //TODO: send those data for deep detection.
  for(var i=0; i<data.length; i++) {
    completedTasks.push({url:data[i].url, id:data[i].id, senderId:data[i].senderId, result:'B'});
  }
}
