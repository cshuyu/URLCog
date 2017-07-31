import codecs


class parser(object):

    def __init__(self):
        with codecs.open('tld.txt', mode='r', encoding='utf-16') as f:
            tld_list=f.read()
            self.tld_arr=tld_list.split()
        with codecs.open('country.txt', mode='r', encoding='utf-16') as g:
            country_list=g.read()
            self.country_arr=country_list.split()

    def parse_protocol(self,url):
        # return a tuple of protocol, and the rest
        arr=url.split('://')
        if len(arr)==1:
            return None, url
        elif len(arr)==2:
            return arr[0], arr[1]
        else:
            return None, None

    def parse_host_n_port(self,rest):
        # return a tuple of host, port, and the rest
        if not rest:
            return None, None, None
        arr=rest.split('/')
        if len(arr)==1:
            host_n_port=rest
            rest=None
        else:
            host_n_port=arr[0]
            del(arr[0])
            rest='/'.join(arr)
            
        arr2=host_n_port.split(':')
        if len(arr2)==1:
            return host_n_port, None, rest
        elif len(arr2)==2:
            return arr2[0], arr2[1], rest
        else:
            return None, None, None

    def parse_tld(self,host):
        # returns hostname (with www), tld
        if not host:
            return None, None
        arr=host.split('.')
        if arr[-1] in self.country_arr:
            if len(arr)>1 and arr[-2] in self.tld_arr:
                tld=arr[-2]+'.'+arr[-1]
                del(arr[-2])
                del(arr[-1])
                hostname='.'.join(arr)
                return hostname, tld

            tld = arr[-1]
            del (arr[-1])
            hostname = '.'.join(arr)
            return hostname, tld

        if arr[-1] in self.tld_arr:
            tld=arr[-1]
            del(arr[-1])
            hostname='.'.join(arr)
            return hostname, tld

        return None, None

    def parse_path_n_queue(self,rest):
        # returns path, queue, and segment
        if not rest:
            return None, None, None
        arr=rest.split('?')
        if len(arr)==1:
            path, segment=self.parse_segment(rest)
            return path, None, segment
        elif len(arr)==2:
            path=arr[0]
            queue, segment=self.parse_segment(arr[1])
            return path, queue, segment
        else:
            return None, None, None

    def parse_segment(self,string):
        # returns previous (path or queue) and segment
        if not string:
            return None, None
        arr=string.split('#')
        if len(arr)==1:
            return string, None
        elif len(arr)==2:
            return arr[0], arr[1]
        else:
            return None, None
        
    def parse(self,url):
        url1=url.lower()
        protocol,rest=self.parse_protocol(url1)
        host,port,rest=self.parse_host_n_port(rest)
        hostname,tld=self.parse_tld(host)
        path,queue,segment=self.parse_path_n_queue(rest)
        return protocol, hostname, tld, port, path, queue, segment