// content_script.js

// Global variable.
var clickableLinks = new Object();
var LOW_CONFIDENCE_SCORE_THRESHOLD = 20;

// Listen commands from background JS.
chrome.runtime.onMessage.addListener(
  // scan all available urls
  function(request, sender, sendResponse) {
    if( request.cmd === "enable_inspector" ) {
      scanAndDetectAllClickableLinks();
      //console.log("URLCog: found "+rs.length+" nodes.");
      //TODO: monitor DOM tree to monitor the rest.
      registerDOMMonitor();
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
    var url = getFullURL(node.href);
    if(url && detectURL(url)) {
      node.style.color = 'red';
    }
  }
  console.log("done detecting "+links.length+" urls.");
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
 * Scan the target url.
 *
 * @param {string} url - the target url to be inspected.
 */
var detectURL = function(url){
  var rs = dtModel.classify(url);
  //console.log("detect result: ",rs,url);
  if (rs.score<LOW_CONFIDENCE_SCORE_THRESHOLD) {
    //TODO: Ajax sends to backend server for processing.
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
  //TODO:
}
