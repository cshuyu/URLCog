function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  init();
});

 /**
  * Init has to be called after the popup html DOM is ready.
  */
var init = function(){
  document.getElementById('togBtn').addEventListener(
    'click', enableOrDisableInspector);
  enableOrDisableInspector();
}

var enableOrDisableInspector = function(event){
  var enabled = document.getElementById('togBtn').checked;
  if (enabled) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var activeTab = tabs[0];
      chrome.tabs.sendMessage(activeTab.id, 
        {"cmd": "enable_inspector"});
      renderStatus("enabled!");
    });
  }
  else {
    renderStatus("disabled!");
  }
}
