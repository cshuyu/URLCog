import codecs
import time
# bad 27548, good 16615

def create_info_dic(path):

    with codecs.open(path,encoding='utf-8') as f:
        arr=f.read().split('\n')
        del(arr[0])
        del(arr[-1])
    dic={}
    registrar_dic={}
    for line in arr:
        line_arr=line.split(':')
        line_arr1=line_arr[0].split(',')
        url=line_arr1[1]
        line_arr2=line_arr[1].split(',')
        num_ip=line_arr2[0]
        reg_time=line_arr2[1]
        country=line_arr2[2]
        registrar=line_arr2[3]
        # process time
        try:
            time_arr = time.strptime(reg_time, "%Y-%m-%d")
            timeStamp = str(int(time.mktime(time_arr)))
        except Exception:
            timeStamp = ''
        dic[url]=str(num_ip)+','+timeStamp+','+country+','
        if registrar in registrar_dic.keys():
            registrar_dic[registrar]+=1
        else:
            registrar_dic[registrar]=1
    for line in arr:
        url=line.split(':')[0].split(',')[1]
        registrar=line.split(':')[1].split(',')[3]
        if registrar_dic[registrar]>=10:
            dic[url]+=registrar
    return dic

def create_index_dic(path):
    with codecs.open(path,encoding='utf-8') as f:
        arr=f.read().split('\n')
    index_dic={}
    for line in arr:
        line_arr=line.split(':')
        url=line_arr[0]
        indexes_arr=line_arr[1].split(',')
        for ind in indexes_arr:
            index_dic[ind]=url
    return index_dic

def process(lexical_path,save_path,info_dic,index_dic):
    with codecs.open(lexical_path,encoding='utf-8') as f:
        arr=f.read().split('\n')
        del(arr[0])
    result='num_ip,reg_time,country,registrar,tld,dot_num,avg_host,max_host,avg_path,max_path,class\n'
    for i,line in enumerate(arr):
        try:
            url = index_dic[str(i)]
            info=info_dic[url]
            info=info.replace('\r','')
            result+=info+','+line+'\n'
        except Exception:
            result+=',,,,'+line+'\n'
    result=result.replace('\'','')
    result=result.replace('"','')
    with codecs.open(save_path,'w',encoding='utf-8') as f:
        f.write(result)

def process_easy(gorb):
    info_dic = create_info_dic('../host/http_proxy/'+gorb+'.log')
    index_dic = create_index_dic('../domain/'+gorb+'_domain.txt')
    process('../lexical/lexical_'+gorb+'.csv', 'host+lexical_'+gorb+'.csv', info_dic, index_dic)

process_easy('good')
process_easy('bad')