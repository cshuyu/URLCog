import codecs

with codecs.open('bad.csv', encoding='utf-8') as f:
    data = f.read()
arr = data.split('\n')
del(arr[0])
del(arr[-1])
all={} #[]
result='hostname,tld,port,path,queue,segment\n'

'''for line in arr:
    if line in all:
        print(line)
    else:
        all.append(line)'''

for line in arr:
    if line in all.keys():
        continue
    else:
        all[line]=1
        result += line + '\n'

with codecs.open('bad.csv',mode='w',encoding='utf-8') as f:
    f.write(result)
