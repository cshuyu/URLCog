import codecs
import socket
import geoip
import time

def import_domain(path,lo=None,hi=None):
    with codecs.open(path,encoding='utf-8') as f:
        arr = f.read().split('\n')
    for i in range(len(arr)):
        arr[i] = arr[i].split(':')[0]
    return arr[lo:hi]

def get_info(domain):
    ip = socket.gethostbyname(domain)
    country = geoip.get_country(ip)
    asn = geoip.get_asn(ip)
    ptr = geoip.ptr(ip)
    return country,asn,ptr

arr = import_domain('good_domain.txt')
for i,domain in enumerate(arr):
    try:
        country,asn,ptr = get_info(domain)
        result = domain + ':' + country + ',' + str(asn) + ',' + str(ptr) + '\n'
    except Exception as e:
        print(str(e))
        result = domain + ':\n'
    print(result[:-1])
    with codecs.open('result.txt','a',encoding='utf-8') as f:
        f.write(result)
    if i%100==99:
        time.sleep(10)
    time.sleep(0.1)
