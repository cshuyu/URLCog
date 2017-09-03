/* UrlUtil Module: Generate URL's feature set for URLCog. 
 * This module replies on compPubSuffixArr, alexaBloomFilter and URI object.
 */
var UrlUtil= (function() {
  if ((typeof compPubSuffixArr === "undefined") || !compPubSuffixArr) {
    console.log("error: compPubSuffixArr is undefined.");
    return null;
  } 
  if ((typeof URI === "undefined") || !URI) {
    console.log("error: URI is undefined.");
    return null;
  }
  if ((typeof alexaBloomFilter === "undefined") || !alexaBloomFilter) {
    console.log("error: alexaBloomFilter is undefined.");
    return null;
  }
  /* Private: returns the URL's domain 
   * Param: (URI) url */
  var getDomain_ = function(url){
    var hostname = url.hostname();
    hostname = hostname.toLocaleLowerCase().trim();
    // compPubSuffixArr is an array with those TLDs
    // that contain more than one parts (e.g., com.cn),
    // sorted by the number of parts desc.
    for (var idx in compPubSuffixArr) {
      var tld = compPubSuffixArr[idx];
      if (hostname.endsWith(tld)) {
        var parts = hostname.substr(0, hostname.length-tld.length).split(".");
        return parts[parts.length-1] + tld;
      }
    }
    var parts = hostname.split(".");
    if (parts.length >= 2) {
      return parts[parts.length-2]+"."+parts[parts.length-1];
    } else {
      return null;
    }
  }
  
  /* Private: returns an array of tokens extracted from a string. 
   * Param: (string) url */
  var getTokens_ = function(str) {
    var tokens = str.split(/[-,_.?'"=/]/);
    var rs = [];
    for (var i in tokens) {
      if(tokens[i].trim().length > 0)
        rs.push(tokens[i].trim());
    }
    return rs;
  }

  /* Private: returns the feature object for target URL. 
   * Param: (string) url */
  var getURLFeatures_ = function(url) {
    var urlObj = URI(url);
    var rs = {};
    if( !urlObj ) {
      console.log("error: failed to create urlObj. "+url);
      return null;
    }
    var domain = getDomain_(urlObj);
    if((typeof domain === "undefined") || !domain) {
      console.log("error: failed to extract domain. "+url);
      return null;
    }
    var dotsInHostname = urlObj.hostname().split(".").length - 1;
    var hostNameTokens = getTokens_(urlObj.hostname());
    var hostNameTokenSum = 0, hostNameTokenMax = 0, hostNameTokenAvg = 0;
    for (var i in hostNameTokens) {
      hostNameTokenSum += hostNameTokens[i].length;
      if (hostNameTokenMax < hostNameTokens[i].length) {
        hostNameTokenMax = hostNameTokens[i].length;
      }
    }
    hostNameTokenAvg = parseInt(hostNameTokenSum / hostNameTokens.length);

    var pathTokens = getTokens_(urlObj.path());
    var isAlexaTopSites = alexaBloomFilter.test(domain);
    // console.log("domain        : "+domain);
    // console.log("dotsInHostname: "+dotsInHostname);
    // console.log("hostnametokenavg: "+ hostNameTokenAvg);
    // console.log("hostnametokenmax: "+ hostNameTokenMax);
    // console.log("pathTokenCount: "+ pathTokens.length);
    // console.log("hostnameTokenCount: "+ hostNameTokens.length);
    // console.log("domainInAlexaOneMillionSite: "+ isAlexaTopSites);
    
    return {
      domain : domain,
      dotsInHostname : dotsInHostname,
      hostNameTokenAvg : hostNameTokenAvg,
      hostNameTokenMax : hostNameTokenMax,
      pathTokenCount : pathTokens.length,
      hostnameTokenCount : hostNameTokens.length,
      domainInAlexaOneMillionSite : isAlexaTopSites
    }
  };
  
  /* Public: gets the feature array used for DT model. 
   * Param: (string) url */
  var extractURLFeatures = function (url) {
    var featureObj = getURLFeatures_(url);
    if(featureObj == null) {
      return null;
    }
    //TODO: add feature preprocessing.
    var features = [];
    features.push(featureObj['domain']);
    features.push(featureObj['dotsInHostname']);
    features.push(featureObj['hostNameTokenAvg']);
    features.push(featureObj['hostNameTokenMax']);
    features.push(featureObj['pathTokenCount']);
    features.push(featureObj['hostnameTokenCount']);
    features.push(featureObj['domainInAlexaOneMillionSite']);
    return features;
  }
  
  /* Public: builds the training set used to train DT model. 
   * Param: (array) [[url1,label1],[url2,label2],...] */
  var buildTrainingSet = function (rawData) {
    var rs = { data:[], label:[]};
    for (var i in rawData) {
      var item = rawData[i];
      var url = item[0].trim();
      var label = item[1]. trim();
      var features = extractURLFeatures(url);
      if(features == null) {
        continue;
      }
      rs.data.push(features);
      rs.label.push(label);
      // console.log(features);
    }
    console.log(rs.data.length+" "+rs.label.length)
    return rs;
  }

  return {
    buildTrainingSet : buildTrainingSet,
    extractURLFeatures : extractURLFeatures
  };
}());