import json,sys

rs = []
#training_set.txt     
with open(sys.argv[1]) as f:    
  for line in f:
    elems = line.split(",")
    url = elems[0].strip().lower()
    label = elems[1].strip()
    rs.append([url, label])


with open('training_set.js', 'w') as outfile:
    outfile.write("var trainingRawData = '")
    outfile.write(json.dumps(rs))
    outfile.write("';")

