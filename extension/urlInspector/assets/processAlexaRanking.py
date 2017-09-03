import json

rs = {}
with open('alexa_top_1m.csv','r') as f:
  with open('alexa_ranking.js','w') as fw:
    fw.write("var alexaRanking = [")
    useComma = False
    for line in f:
      line = line.strip()
      elems = line.split(",")
      if useComma: 
        fw.write(",\n")
      else: 
        useComma = True
      fw.write("'"+elems[1]+"'")
    fw.write("];");

#with open('alexa_ranking.js','w') as f:
#  f.write("var alexaRanking = "+json.dumps(rs))