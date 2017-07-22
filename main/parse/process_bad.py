import parse as ps
import codecs


p=ps.parser()
result='hostname,tld,port,path,queue,segment\n'

with codecs.open('../data/url-data.csv', encoding='utf-8') as f:
    data=f.read()
data_arr=data.split('\n')
del(data_arr[0])

for line in data_arr:
    line_result=''
    line_arr=line.split(',')
    if len(line_arr)>1 and line_arr[1]=='bad':
        _, hostname, tld, port, path, queue, segment=p.parse(line_arr[0])
        if not hostname:
            continue
        parts_arr=[hostname, tld, port, path, queue, segment]
        for part in parts_arr:
            if part:
                line_result+=part+','
            else:
                line_result+=','
        line_result=line_result[:-1]+'\n'
        result+=line_result
         
with codecs.open('../data/url-data2.csv', encoding='utf-8') as f:
    data=f.read()
data_arr=data.split('\n')
del(data_arr[0])

for line in data_arr:
    line_result=''
    line_arr=line.split(',')
    if len(line_arr)>1 and line_arr[1]=='bad':
        _, hostname, tld, port, path, queue, segment=p.parse(line_arr[0])
        if not hostname:
            continue
        parts_arr=[hostname, tld, port, path, queue, segment]
        for part in parts_arr:
            if part:
                line_result+=part+','
            else:
                line_result+=',' 
        line_result=line_result[:-1]+'\n'
        result+=line_result
    
with codecs.open('bad.csv', encoding='utf-8', mode='w') as f:
    f.write(result)
