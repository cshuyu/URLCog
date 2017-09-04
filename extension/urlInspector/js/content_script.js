// content_script.js

// Global variable.
var clickableLinks = new Object();
var LOW_CONFIDENCE_SCORE_THRESHOLD = 120;
var observer = null;
var idCnt = 0;
var idNodeMap = {};
// Listen commands from background JS.
chrome.runtime.onMessage.addListener(
  // scan all available urls
  function(request, sender, sendResponse) {
    if( request.cmd === "enable_inspector" ) {
      scanAndDetectAllClickableLinks();
      registerDOMMonitor();
    } else if (request.cmd === "disable_inspector") {
      if(observer) {
        observer.disconnect();
      }
    } else if (request.cmd === "detection_result") {
      try{
        var node = idNodeMap[request.id];
        //console.log("received detection_result:", request, node);
        if(node) {
          if(request.result === "M") {
            node.style.color = 'red';
          }
        }
      } catch (e) {
        console.log("error: receive detection request: ",e);
      }
    }
  }
);

/**
 * Scan all the clickable links.
 */
var scanAndDetectAllClickableLinks = function() {
  if ((typeof dtModel === "undefined") || !dtModel) {
    console.log("error: dtModel is not ready.");
    return ;
  }
  var links = document.links;
  var rs = new Array();
  
  for (var idx in links) {
    var node = links[idx];
    if(! node.href) continue;
    //TODO: filter out those scanned URLs using BloomFilter?
    processNode(node);
  }
  console.log("done detecting "+links.length+" urls.");
}

var processNode = function(node) {
  var url = getFullURL(node.href);
  if(url && detectNode(node)) {
    node.style.color = 'red';
  }
}

var getFullURL = function(url){
  if (typeof(url) !== 'string' && url instanceof String)
    return null;
  var url = url.toLocaleLowerCase();
  if (url.indexOf('http://')!==0 && url.indexOf('https://')!==0) {
    var base = document.baseURI();
    if(base && 
        (base.indexOf('http://')===0 || base.indexOf('https://')===0)) {
      url = base + url;
    }
    else 
      return null;
  }
  return url;
}

/**
 * Scan the target node with href attribute.
 *
 * @param {Node} node - the target node to be inspected.
 */
var detectNode = function(node){
  var url = node.href
  var rs = dtModel.classify(url);
  //console.log("detect result: ",rs,url);
  if (rs.score<LOW_CONFIDENCE_SCORE_THRESHOLD) {
    //TODO: Ajax sends to backend server for processing.
    var id = genUniqueID();
    idNodeMap[id] = node;
    requestRemoteDetection({url:url, id:id});
  }

  if(!rs.isMalicious || rs.score<LOW_CONFIDENCE_SCORE_THRESHOLD) {
    return false; //not malicious
  } else {
    return true;
  }
}

/**
 * Register DOM tree change to detect newly added urls.
 */
var registerDOMMonitor = function() { 
  observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      // console.log("mutation nodeName:", mutation.target.nodeName);
      // console.log("mutation addedNodes:", mutation.addedNodes);
      // console.log("mutation :", mutation);
      for (var i=0; i<mutation.addedNodes.length; i++) {
        var node = mutation.addedNodes[i];
        // console.log("AddedNode: ",node);
        // console.log("Href: ",node.href);
        if(node.href) {
          processNode(node);
        }
      }
    });
  });
  observer.observe(document, { childList:true, subtree: true, attributes:true });

  // var a = document.createElement("a");
  // a.href = "http://www.google.com";
  // a.innerText ="abd";
  // document.getElementsByTagName('body')[0].appendChild(a);
};
/*
 * Sends the url to backend, where it will sends to server for
 * deeper detection.
 * Param (object) {url: url, id:id}
 */
var requestRemoteDetection = function(obj){
  chrome.runtime.sendMessage({
      cmd:"deep-detection", 
      url: obj.url, 
      id:obj.id}, 
    function(response){
      if(response && response.status) {
        //console.log("["+response.status+"] done sending "+obj.url+" for remote detection.");
      } else {
        console.log("request emoteDetection failed. ");
      }
    });
};

var genUniqueID = function(){
  return idCnt++;
};
