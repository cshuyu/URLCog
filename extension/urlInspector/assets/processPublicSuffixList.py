import operator
complexSuffixDict = {};
with open('public_suffix_list.dat','r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0: continue
    if line.startswith('//'): continue
    parts = line.split('.')
    if len(parts) < 2: continue
    complexSuffixDict[line.lower()] = len(parts)

complexSuffixSortedList = sorted(
  complexSuffixDict.items(), key=operator.itemgetter(1),reverse=True)

with open('complex_suffix_list.js','w') as f:
  f.write("var compPubSuffixArr = [ \n")
  useComma = False
  for item in complexSuffixSortedList:
    if useComma: 
      f.write(",\n")
    else: 
      useComma = True
    f.write("'."+item[0]+"'")
  f.write("];");