import parse as ps
import codecs


p=ps.parser()
result='hostname,tld,port,path,queue,segment\n'

with codecs.open('../data/result.txt',mode='r',encoding='utf-8') as f:
    data=f.read()
data_arr=data.split(',')
data_arr=data_arr[:2000000]
hostnames={}

num=0
for line in data_arr:
    line_result=''
    line=line[10:-2]
    _, hostname, tld, port, path, queue, segment=p.parse(line)
    parts_arr=[hostname, tld, port, path, queue, segment]
    if not hostname:
        continue
    if hostname in hostnames:
        if hostnames[hostname]>50:
            continue
        else:
            hostnames[hostname]+=1
    else:
        hostnames[hostname]=1

    if num>100000:
        break
    num+=1
    for part in parts_arr:
        if part:
            line_result+=part+','
        else:
            line_result+=','
    line_result=line_result[:-1]+'\n'
    result+=line_result

with codecs.open('good.csv', mode='w',encoding='utf-8') as f:
    f.write(result)
