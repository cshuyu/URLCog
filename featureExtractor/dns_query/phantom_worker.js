var queue = require('./Queue'),
  system = require('system'),
  taskWorker,
  /* parameters */
  address, times, index,
  /* settings */
  defaultUserAgent, userAgent, defaultTimeout, timeout,
  /* utilities */
  b64EncodeUnicode, displayObject;

/* Settings */
defaultUserAgent = 
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0";
defaultTimeout = 5000;

/* Utilities */
b64EncodeUnicode = function(str) {
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
        return String.fromCharCode('0x' + p1);
    }));
}
displayObject = function (obj) {
  var item;
  for (item in obj) {
    if (obj.hasOwnProperty(item)) {
        console.log("KEY: "+ item+" VAL:"+obj[item]);
    }
  }
};

/* Task Worker */
/*
 * taskWorker = {
 *    configure : function(setting){},
 *    post_task : function(task){},
 *    open_url_callback : function(result){},
 *    send_contents : function(url, contents, landing_url){},
 *    start_tasks :  function(){},
 *    open_url  : function(url){},
 *    get_remaining_task_count : function(){},
 *    get_fin_task_count  :  function(){},
 *    get_error_tag  : function(){},
 *}
 */
taskWorker = (function (){
  var user_agent, timeout, remaining_times, current_url,
    task_queue = new queue(), page = null,
    fin_task_count = 0, err_task_count = 0,
    error_tag = false,
    configure, post_task, start_tasks, 
    open_url, open_url_callback,
    get_remaining_task_count, get_fin_task_count, get_error_tag;

  configure = function(settings) {
    user_agent = settings.user_agent;
    timeout = settings.timeout;
    remaining_times = settings.remaining_times;
  };

  post_task = function (task) {
    task_queue.enqueue(task);
    console.log("[ADD_TASK] adding a browsing task: " + 
      task_queue.getLength());
  };

  open_url_callback = function (result) {
    try{
      if (result.status !== 'success') {
        console.log('[FAIL] load the url:'+result.url+", "+result.status);
        if(--remaining_times > 0){
          console.log('[INFO]  try again.'+ remaining_times+" times remain");
          open_url(current_url);
          return ;
        }
        else{
          console.log('[INFO]  Give up this URL.');
        }
      }
      else {
        console.log("[SUCC] to load the address: " + result.url +
          ", contnet-size:"+result.content.length+
          ", requested objects:"+result.request_count+
          ", failed objects:"+ result.failed_obj_count);
        remaining_times = 0;
        //console.log(result.content);
        //Parse contents
        send_contents(current_url, result.content)
      }
    }
    catch (err) {
      console.log("[ERROR] error in open_url_callback "+err);
    }
    
    start_tasks();
  };

  send_contents = function (url, contents) {
    //TODO: this method will send results to database to store.
    //      right now, let's just write it to standard output.
    console.log("[RESULT]\n"+contents);
    return ;

    var db_listener = "http://localhost:4040/api/web-contents/contents-store",
      sender, error = null, 
      json_header, encoded_contents, data;
    sender = require('webpage').create();
    sender.onResourceTimeout = function (e) {
      error = "timeout";
    };
    console.log("[INFO] sending contents to Database: "+contents.length);
    encoded_contents = b64EncodeUnicode(contents);
    data = '{"url":"' + encodeURIComponent(url) 
          '","contents":"'+encoded_contents+'"}';
    json_header = { "Content-Type": "application/json" };
    try{
      sender.open(db_listener, 'post', data, json_header,
       function (status) {
        sender.close();
        sender = null;
        
        if (status !== 'success')
          console.log("[FAIL] failed to send contents to DB.");
        else if (error) 
          console.log("[FAIL] failed to send contents to DB."+error);
        else 
          console.log("[SUCCEED] sent contents ["+data.length+"] to db");
      });
    }
    catch (err) {
      console.log("[PHANTOM_ERR] error sending contents to db "+err);
      sender.close();
      page = null;
      error_tag = true;
    }
    finally {
      fin_task_count++;
    } 
  };

  start_tasks = function () {
    var task;
    if (task_queue.getLength()>0 && page === null) {
        task = task_queue.dequeue();
        current_url = task.url;
        console.log("[INFO] start next task, "+task_queue.getLength()+" tasks left");
        open_url(task.url);
    }
    else if(task_queue.getLength() === 0){
      console.log("[INFO] no other tasks ");
    }
    else{
       console.log("[INFO] cannot start next task because page is in use. ");
    }
  };

  get_remaining_task_count = function () {
    return task_queue.getLength();
  };

  get_fin_task_count = function() {
    return fin_task_count;
  };

  get_error_tag = function () {
    return error_tag;
  }
  
  //this method creates and closes the page instance
  open_url = function (url) {
    var landing_page = url, content, timeout_count = 0,
      request_count = 0, response_count = 0;
    error_tag = false;
    if (page !== null) {
      console.log("[ERROR] last instance hasn't finished!!!");
      return ;
    }
    page = require('webpage').create();
    page.settings.resourceTimeout = 5000;
    page.settings.userAgent = user_agent;    

    page.onConsoleMessage = function (msg) { console.log(msg); };
    
    /** rewrite eval functions **/
    // page.onInitialized = function() {
    //   console.log("[DEBUG] onInitialized");
    //   page.injectJs('hook.js');
    // };
    /****************************/

    page.onResourceRequested = function (req) {
      request_count++;
    };

    page.onResourceReceived = function (res) {
      response_count++;
    };

    page.onResourceTimeout = function (e) {
      timeout_count++;
    };

    console.log("[INFO] start browsing: "+url);
    try{
      page.open(url, function (status) {
        console.log("[INFO] done opening: "+url+" "+status);
        content = page.content.slice(0);
           
        page.close();
        page = null;
        
        open_url_callback({
          status : status,
          url : url,
          request_count : request_count,
          response_count : response_count,
          failed_obj_count : timeout_count,
          content : content
        });
      });
    }
    catch (err) {
      console.log("[WORKER] error in open "+url+" error:"+err);
      page.close();
      page = null;
      error_tag = true;
    }
    finally { } 
  };

  wait_for_task_finish = function() {
    if (!taskWorker.get_error_tag() &&
      (task_queue.getLength()>0 || page!==null) ) {
        console.log("[INFO] finished "+task_queue.getLength() +
          " tasks left, check 2s later");
      setTimeout(
        function(){ wait_for_task_finish() },
        2000);
    }
    else {
      console.log("[INFO] exit. finished "+
        taskWorker.get_fin_task_count()+" tasks");
      phantom.exit();
    }
  };
  
  return {
    configure : configure,
    post_task : post_task,
    start_tasks : start_tasks,
    get_remaining_task_count : get_remaining_task_count,
    get_fin_task_count : get_fin_task_count,
    get_error_tag : get_error_tag,
    wait_for_task_finish : wait_for_task_finish
  };

})();

/* main */
if (system.args.length < 3) {
  console.log(
    "usage: phantom-worker.js url times timeout-for-one-req userAgent");
}
else {
  address = system.args[0];
  times = parseInt(system.args[1]);
  if (system.args.length >3 ){
    timeout = parseInt(system.args[3]);
  }
  else {
    timeout = defaultTimeout;
  }
  if (system.args.length > 4){
    userAgent = system.args[4];
  }
  else {
    userAgent = defaultUserAgent;
  }
  console.log("[MAIN] browsing "+address+" for "+times);
  taskWorker.configure({
    timeout : timeout,
    user_agent : userAgent,
    remaining_times : times });
  taskWorker.post_task({url : address});
  taskWorker.start_tasks();
  taskWorker.wait_for_task_finish();
}


