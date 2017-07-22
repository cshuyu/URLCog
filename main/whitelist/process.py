import codecs
from random import shuffle


top_dic={}
with open('top-domain/alexa-top-1m.csv') as f:
    arr=f.read().split('\n')
for line in arr:
    try:
        url=line.split(',')[1]
        top_dic[url]=1
    except Exception:
        print(line)

def process(gorb):
    result_dic={}
    with codecs.open('../domain/'+gorb+'_domain.txt',encoding='utf-8') as f:
        arr=f.read().split('\n')
        del(arr[-1])
        for line in arr:
            line_arr=line.split(':')
            url=line_arr[0]
            indexes=line_arr[1].split(',')
            if url in top_dic.keys():
                for ind in indexes:
                    result_dic[ind]=1
            else:
                for ind in indexes:
                    result_dic[ind]=0
    result_arr=[]
    result='is_top_1m,num_ip,reg_time,country,registrar,tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
    with codecs.open('../host+lexical/host+lexical_'+gorb+'.csv', encoding='utf-8') as f:
        arr=f.read().split('\n')
        del(arr[-1])
    for i,line in enumerate(arr):
        if i==0:
            continue
        line_result=str(result_dic[str(i)])+','+line
        result+=line_result+'\n'
        result_arr.append(line_result)

    with codecs.open('host+lexical+whitelist_'+gorb+'.csv','w',encoding='utf-8') as f:
        f.write(result)
    return result_arr

bad_arr=process('bad')
good_arr=process('good')
total_arr=bad_arr+good_arr
shuffle(total_arr)
result='is_top_1m,num_ip,reg_time,country,registrar,tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
result+='\n'.join(total_arr)
with codecs.open('host+lexical+whitelist_training.csv', 'w', encoding='utf-8') as f:
    f.write(result)