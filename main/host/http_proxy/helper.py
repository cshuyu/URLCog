import codecs
import logging
import random

def import_url(path,lo,hi):
    with codecs.open(path,encoding='utf-8') as f:
        string = f.read()
    arr = string.split('\n')
    if not lo:
        lo=0
    if not hi:
        hi=len(arr)
    arr=arr[lo:hi]
    url_arr = []
    want = range(lo,hi)
    # returns url and its number
    for i,line in enumerate(arr):
        if i+lo in want:
            url = line.split(':')[0]
            num = str(i+lo).zfill(5)
            url_arr.append((num,url))
    return url_arr


def import_proxy(path,mode):
    with open(path) as f:
        string = f.read()
    arr = string.split('\n')
    del(arr[-1])
    proxy_arr = []
    for line in arr:
        if mode=='comma':
            line_arr=line.split(',')
            addr=line_arr[0]
            port=line_arr[1]
            line=addr+':'+port
        dic = {}
        dic['http'] = 'http://' + line
        dic['https'] = 'https://' + line
        proxy_arr.append(dic)
    random.shuffle(proxy_arr)
    return proxy_arr


def setLogger(path):
    console_logger = logging.getLogger('consoleLogger')
    hdlr = logging.FileHandler('./console.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    console_logger.addHandler(hdlr)
    console_logger.addHandler(consoleHandler)
    console_logger.setLevel(logging.DEBUG)

    result_logger = logging.getLogger('resultLogger')
    hdlr2 = logging.FileHandler('./'+path,encoding='utf-8')
    formatter2 = logging.Formatter('%(message)s')
    hdlr2.setFormatter(formatter2)
    result_logger.addHandler(hdlr2)
    result_logger.setLevel(logging.DEBUG)

    return console_logger, result_logger
