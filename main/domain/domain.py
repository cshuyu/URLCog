import codecs


def process(gorb):
    with codecs.open('../parse/'+gorb+'.csv',encoding='utf-8') as f:
        arr=f.read().split('\n')
        del(arr[0])
        del(arr[-1])
    dic={}
    domain_arr=[]
    result=''
    for i,line in enumerate(arr):
        line_arr=line.split(',')
        hostname=line_arr[0]
        tld=line_arr[1]
        domain=hostname.split('.')[-1]+'.'+tld
        if domain not in dic.keys():
            domain_arr.append(domain)
        if domain in dic.keys():
            dic[domain]+=','+str(i)
        else:
            dic[domain]=str(i)
    for i in range(len(domain_arr)):
        domain_arr[i]+=':'+dic[domain_arr[i]]
    result='\n'.join(domain_arr)
    with codecs.open(gorb+'_domain.txt','w',encoding='utf-8') as f:
        f.write(result)

process('bad')
process('good')