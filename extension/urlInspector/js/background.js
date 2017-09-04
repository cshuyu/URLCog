var reqCache = [];

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.cmd == "deep-detection"){
    console.log("receive deep detection request: ",sender," "+request.url);
    if(request.url && request.id){
      //sendURLForRemoteDetection(request.url, request.id, sender.tab.id);
      reqCache.push({url:request.url, id:request.id, senderId:sender.tab.id});
      sendResponse({status:"submitted"});
    } else {
      sendResponse({status:"request error"});
    }
  }
});

var processCachedRequests = function(){
  console.log("start processing cached requests.");
  if(reqCache.length > 0){
    sendURLForRemoteDetection(reqCache);
    console.log("sending "+reqCache.length+" requests.");
    reqCache = [];
  }
  //TODO: check results from server.
  fetchDetectionRequests();
  
  setTimeout(processCachedRequests,10000);
};

var sendURLForRemoteDetection = function(reqArr) {
  $.ajax
  (
      {
          type: "POST",
          //TODO: write the url into a configuration file.
          url: "http://localhost:3000/remote-detection/",
          dataType:"application/json",
          data: 
          {               
              cmd: 'remote-detection',
              payload : JSON.stringify(reqArr)
          },
          success: function(msg)
          {
            if(msg.status === "succ") {
              console.log("succeeded: sendURLForRemoteDetection send ",msg);
              // chrome.tabs.sendMessage(senderId, 
              //   {"cmd": "detection_result", id:id});
            } else {
              console.log("failed: sendURLForRemoteDetection ",msg);
            }
          },
          error: function(msg) 
          {
             console.log("failed: sendURLForRemoteDetection (server) ",msg);
          }
      }
  );//End ajax 

};

var fetchDetectionRequests = function() {
  $.ajax
  (
      {
          type: "GET",
          //TODO: write the url into a configuration file.
          url: "http://localhost:3000/fetch-results/",
          success: function(msg)
          { 
            var resp = JSON.parse(msg);
            if(resp.status==="succ" && resp.data.length>0) {
              console.log("succeeded: fetchDetectionRequests get "+resp.data.length+" responses.");
              for(var i in resp.data){
                var obj = resp.data[i];
                chrome.tabs.sendMessage(obj.senderId, 
                  {"cmd": "detection_result", id:obj.id, result:obj.result});
              } 
            } else {
              console.log("failed: fetchDetectionRequests ",resp.status);
            }
          },
          error: function(msg) 
          {
             console.log("failed: fetchDetectionRequests (server) ",msg);
          }
      }
  );//End ajax 

};

//check
processCachedRequests();