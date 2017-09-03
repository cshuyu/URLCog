
var dtModel = (function(){
  if ((typeof modelTreeStr === "undefined") || !modelTreeStr) {
    console.log("error: modelTreeStr is undefined.");
    return null;
  }
  if ((typeof UrlUtil === "undefined") || !UrlUtil) {
    console.log("error: UrlUtil is undefined.");
    return null;
  }

  var dt_ = new ml.DecisionTree({
    data : [], result : [] });
  // console.log("length of model: "+modelTreeStr.length);
  dt_.tree = JSON.parse(modelTreeStr);
  
  var classify = function(url) {
    var feature_arr = UrlUtil.extractURLFeatures(url);
    if(feature_arr == null) {
      console.log("error: failed to classify because of feature_arr error.");
      return {isMalicious: false, score: 0};
    }
    
    var rs = dt_.classify(feature_arr);
    // console.log("start to classify: ",feature_arr," ",rs);
    if (Number.isInteger(rs['B'])) {
      return {isMalicious: false, score: rs['B']};
    } else {
      return {isMalicious: true, score: rs['M']};
    }
  };

  return {
    classify : classify
  };
  // var rs1 = dt.classify(f1);
  // console.log("classify sina: ",rs1['B'],+" "+rs1['M']);
  // var rs2 = dt2.classify(f2);
  // console.log("classify github: ",rs2['B'],+" "+rs2['M']);
})();

// console.log("sina: "+dtModel.classify("http://www.sina.com.cn/book"));
// console.log("git2: "+dtModel.classify("https://git2hub.com/medialize/URI.js/"));
// console.log("git2: "+dtModel.classify("https://google.com"));
console.log("dtModel is ready.")