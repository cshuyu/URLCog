with open('lexical.csv') as f:
    string=f.read()
arr=string.split('\n')
arr=arr[:10000]
result='\n'.join(arr)
with open('sub.csv','w') as f:
    f.write(result)