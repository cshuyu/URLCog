import codecs
import logging
import random


def import_url(path,lo,hi):
    with codecs.open(path,encoding='utf-8') as f:
        string = f.read()
    arr = string.split('\n')
    arr=arr[lo:hi]
    url_arr = []
    want = range(lo,hi)
    #want=[254,610,1695,1698,2324,2403,2793,2997,3295,3641,3922,4258,4565,4701,4784,4924,4925]
    # returns url and its number
    for i,line in enumerate(arr):
        if i+lo in want:
            url = "https://who.is/whois/"+ line
            num = str(i+lo).zfill(5)
            url_arr.append((num,url))
    return url_arr


def import_proxy(path):
    with open(path) as f:
        string = f.read()
    arr = string.split('\n')
    proxy_arr = []
    for line in arr:
        line = line.split(' ')[0]
        dic = {}
        dic['http'] = 'http://' + line
        dic['https'] = 'https://' + line
        proxy_arr.append(dic)
    random.shuffle(proxy_arr)
    return proxy_arr


def setLogger():
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
    hdlr2 = logging.FileHandler('./result.log',encoding='utf-8')
    formatter2 = logging.Formatter('%(message)s')
    hdlr2.setFormatter(formatter2)
    result_logger.addHandler(hdlr2)
    result_logger.setLevel(logging.DEBUG)

    return console_logger, result_logger
