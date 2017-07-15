import codecs

# bad.csv
with codecs.open('../parse/good.csv', mode='r', encoding='utf-8') as f:
    string = f.read()

arr = string.split('\n')
del(arr[0])
del(arr[-1])
all = []
result=''

for line in arr:
    seg = line.split(',')
    hostname = seg[0] + '.' + seg[1]
    if hostname in all:
        continue
    else:
        all.append(hostname)
        result += hostname + '\n'

# bad_hostnames.csv
with codecs.open('good_hostnames.csv',mode='w',encoding='utf-8') as f:
    f.write(result)
