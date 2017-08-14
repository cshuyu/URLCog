// content_script.js

// Global variable.
var clickableLinks = new Object();

// Listen commands from background JS.
chrome.runtime.onMessage.addListener(
  // scan all available urls
  function(request, sender, sendResponse) {
    if( request.cmd === "enable_inspector" ) {
      var rs = scanAllClickableLinks();
      console.log("URLCog: found "+rs.length+" nodes.");
      rs.forEach( function(node){
        var url = getFullURL(node.href);
        if(url && detectURL(url)) {
          node.style.color = 'red';
        }
      });
      //TODO: monitor DOM tree to monitor the rest.
      registerDOMMonitor();
    }
  }
);

/**
 * Scan all the clickable links.
 */
var scanAllClickableLinks = function() {
  var links = document.links;
  var rs = new Array();
  //TODO: filter out those scanned URLs.
  for (var idx in links) {
    var node = links[idx];
    if(! node.href) continue;
    // var path = node.href.toLocaleLowerCase();
    // if (path.indexOf('http://')!==0 && path.indexOf('https://')!==0) {
    //   var base = document.baseURI();
    //   if(base && 
    //       (base.indexOf('http://')===0 || base.indexOf('https://')===0)) {
    //     path = base + path;
    //   }
    //   else continue;
    // }
    rs.push(node);
  }
  return rs;
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
var detectURL = function(node){
  //TODO: bogus function.
  var ms = new Date().getTime();
  if (ms%2 === 0)
    return true;
  else
    return false;
}

/**
 * Register DOM tree change to detect newly added urls.
 */
var registerDOMMonitor = function() {
  //TODO:
}

