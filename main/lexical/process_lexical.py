import lexical as lx
import codecs
from random import shuffle


l=lx.lexical()
result='tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
result_arr1=[]

with codecs.open('../parse/good.csv',encoding='utf-8') as f:
    string=f.read()
arr=string.split('\n')
del(arr[0])
del(arr[-1])
for line in arr:
    comp=line.split(',')
    hostname=comp[0]
    tld=comp[1]
    path=comp[3]
    dot_num, avg_host, max_host, avg_path, max_path=l.lexical(hostname,path)
    result_arr1.append(tld+','+str(dot_num)+','+str(avg_host)+','+str(max_host)+','+str(avg_path)+','+str(max_path)+',good')

result='tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
result+='\n'.join(result_arr1)
with codecs.open('lexical_good.csv',mode='w',encoding='utf-8') as f:
    f.write(result)

result_arr2=[]
with codecs.open('../parse/bad.csv',encoding='utf-8') as f:
    string=f.read()
arr=string.split('\n')
del(arr[0])
del(arr[-1])
for line in arr:
    comp=line.split(',')
    hostname=comp[0]
    tld=comp[1]
    path=comp[3]
    dot_num, avg_host, max_host, avg_path, max_path=l.lexical(hostname,path)
    result_arr2.append(tld+','+str(dot_num)+','+str(avg_host)+','+str(max_host)+','+str(avg_path)+','+str(max_path)+',bad')

result='tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
result+='\n'.join(result_arr2)
with codecs.open('lexical_bad.csv',mode='w',encoding='utf-8') as f:
    f.write(result)
