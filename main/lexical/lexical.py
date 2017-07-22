import re


class lexical(object):

    '''Lexical Features:
	Top Level domain (str)
	Number of dots in hostname (int)
	Average token length of hostname (float)
	Max token length of hostname (int)
	Average token length of path (float)
	Max token length of path (int)
    '''

    def __init__(self):
        pass

    def lexical(self,hostname,path):
        dot_num=self.dots(hostname)
        arr_host=self.split(hostname)
        arr_path=self.split(path)
        avg_host=self.avg(arr_host)
        max_host=self.max(arr_host)
        avg_path=self.avg(arr_path)
        max_path=self.max(arr_path)

        return dot_num,avg_host,max_host,avg_path,max_path

    def dots(self,hostname):
        # returns number of dots
        return hostname.count('.')

    def split(self,string):
        # returns a list split by ‘/’,  ‘?’,  ‘.’,  ‘=’,  ‘-’  and ‘_’
        return re.split('/|\?|\.|=|-|_', string)

    def avg(self,arr):
        # returns average token length
        return sum(len(token) for token in arr)/len(arr)

    def max(self,arr):
        # returns max token length
        return max(len(token) for token in arr)