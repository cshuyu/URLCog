import requests
import threading
import WhoisParser

# Multithreads programming.
# This class is a worker thread that will be started by main thread.
class WhoisWorker(threading.Thread):
    def __init__(self, thread_ID, queue, proxy_arr, console_logger, result_logger, conn_timeout=3, read_timeout=5, max_attempt=5):
        threading.Thread.__init__(self)
        self.thread_id = thread_ID
        self.queue = queue
        self.parser=WhoisParser.WhoisParser()
        self.console_logger = console_logger
        self.result_logger = result_logger
        self.proxy_arr = proxy_arr
        self.conn_timeout = conn_timeout  # connection timeout
        self.read_timeout = read_timeout  # response read timeout
        self.max_attempt = max_attempt
        self.whois_site = 'https://who.is/whois/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101 Firefox/53.0'}


    def step(self, i, url, proxy_index):
        try:
            # read http://docs.python-requests.org/en/master/
            # read http://docs.python-requests.org/zh_CN/latest/user/advanced.html
            proxy=None
            if self.proxy_arr:
                proxy=self.proxy_arr[proxy_index]
            response = requests.get(self.whois_site + url, verify=False, headers=self.headers,
                                    timeout=(self.conn_timeout, self.read_timeout),
                                    proxies=proxy)
            if response.status_code >= 400:
                self.console_logger.error('   Get bad request %s' % i)
                return False
            else:
                texts = response.text  # load contents in blocking mode
                info = self.parser.to_string(texts)
                self.result_logger.debug(u'%s,%s:%s'%(i,url,info))
                self.console_logger.debug(
                    'Success loading %s, thread %d proxy index %d' % (i, self.thread_id, proxy_index))
                return True
        except Exception as e:
            self.console_logger.error('      Error loading %s, thread %d, proxy index %d' % (i, self.thread_id, proxy_index))
            self.console_logger.error('         %s'%str(e))
            return False

    def run(self):
        proxy_index = 0
        while True:
            i,url = self.queue.get()
            attempt = 0
            #self.logger.debug("start " + url)
            while not self.step(i, url, proxy_index):
                if self.proxy_arr:
                    proxy_index=(proxy_index+1) % len(self.proxy_arr)
                if attempt>=self.max_attempt:
                    # put the task into the queue again
                    #self.queue.put((i, url))
                    break
                attempt += 1
            # Send signal to the queue that the worker thread
            #  has finished one task.
            self.queue.task_done()
        return


