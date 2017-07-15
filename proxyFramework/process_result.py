import codecs


def missing():

    with codecs.open('result.log',encoding='utf-8') as f:
        string=f.read()
        arr=string.split('\n')

    all={}
    for line in arr:
        ind=line.split(':')[0]
        all[ind]=True

    missing = []
    for i in range(30000):
        if str(i).zfill(5) not in all.keys():
            missing.append(i)
            #print(i)
    return missing