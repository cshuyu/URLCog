# see https://github.com/cshuyu/URLCog/ contributer Xiang Pan, cshuyu
import WhoisWorker as wh
import queue as qu
import helper
import warnings
warnings.filterwarnings("ignore")

# Use mitmproxy to observe or monitor.
# Enter mitmproxy's interactive mode:
#   mitmproxy -i ~q 
'''local_proxies = {
  "http": "http://localhost:8080",
  "https": "https://localhost:8080",
}'''

# Example: mxtoolbox.com requires JS execution.
#  use phantomjs instead.
#  url: ["https://mxtoolbox.com/SuperTool.aspx?action=whois%3agoogle.com&run=toolpage"]

# Example: www.whatismyip.com checks the user-agent.
#  provide headers in each request.
#  url: https://www.whatismyip.com/

# Example: whois.icann.org requires captcha.
#  url: https://whois.icann.org/en/lookup?name=google.com

# The entrance of the program.

def main():
    thread_num = 10
    queue = qu.Queue()
    proxys = helper.import_proxy('proxy.csv','comma')
    #proxys = helper.import_proxy('pr
    # oxy.csv')
    #proxys=None
    console_logger, result_logger = helper.setLogger('good.log')
    urls = helper.import_url('../../domain/good_domain.txt',None,None)
    #result_logger.debug(u'num,url:num_ip,reg_time,country,registrar')
    # start worker threads
    for i in range(thread_num):
        proxy_arr=[]
        if proxys:
            proxy_arr = proxys[int(i*len(proxys)/thread_num):int((i+1)*len(proxys)/thread_num)]
        conn_timeout=7
        read_timeout=10
        max_attempt=5
        worker = wh.WhoisWorker(i, queue, proxy_arr,console_logger, result_logger,conn_timeout,read_timeout,max_attempt)
        worker.setDaemon(True)
        worker.start()
    
    for i,url in urls:
        queue.put((i,url))
    
    # Wait on the queue until all have been processed

    queue.join()

if __name__ == "__main__":
    main()
