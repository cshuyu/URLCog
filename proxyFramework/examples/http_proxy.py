import requests
import Queue
import threading
import logging

#use mitmproxy
local_proxies = {
  "http": "http://localhost:8080",
  "https": "https://localhost:8080",
}

#get from https://free-proxy-list.net/
#TODO: replace with a dynamic list.
outside_proxies = {
  "http": "http://200.141.34.246:53281",
  "https": "https://200.141.34.246:53281",
}

def setLogger():
    logger = logging.getLogger('WhoisLogger')
    hdlr = logging.FileHandler('./whois.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)
    return logger


class WhoisWorker(threading.Thread):
    def __init__(self, queue, logger):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.conn_timeout = 3  #connection timeout
        self.read_timeout = 5  #response read timeout
        #A lot of website use user-agent to 
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101 Firefox/53.0'}
    
    def run(self):
        while True:
            url = self.queue.get()
            self.logger.debug("start "+url)
            try:
                #read http://docs.python-requests.org/en/master/
                #read http://docs.python-requests.org/zh_CN/latest/user/advanced.html
                response = requests.get(url, verify=False, headers=self.headers,
                    timeout=(self.conn_timeout, self.read_timeout),
                    proxies=outside_proxies)
                texts = response.text # load contents in blocking mode
                self.logger.debug("done loading %s with status code %s. "%(
                    url,response.status_code) )
                self.logger.debug("  fetched %d data"%len(texts))
                self.logger.debug(texts)
            except Exception as e:
                self.logger.error("failed to load %s because of %s." %(url, str(e)))
            self.queue.task_done()

def main():
    logger = setLogger()
    queue = Queue.Queue()
    
    #Note that mxtoolbox.com requires JS execution. 
    # use phantomjs instead.
    #urls = ["https://mxtoolbox.com/SuperTool.aspx?action=whois%3agoogle.com&run=toolpage"]
    
    urls = ["https://who.is/whois/sina.com.cn", "https://www.whatismyip.com/"]
    #urls = ["https://www.iplocation.net/find-ip-address"]
    # start worker threads
    for i in range(5):
        worker = WhoisWorker(queue, logger)
        worker.setDaemon(True)
        worker.start()
    
    for url in urls:
        queue.put(url)
    
    #wait on the queue until all have been processed
    queue.join()

if __name__ == "__main__":
    main()
    
    
            
