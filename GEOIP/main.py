# see https://github.com/cshuyu/URLCog/ contributer Xiang Pan, cshuyu
import WhoisWorker as wh
import queue as qu
import helper
import warnings
warnings.filterwarnings("ignore")

# Use mitmproxy to observe or monitor.
# Enter mitmproxy's interactive mode:
#   mitmproxy -i ~q 
single_proxy = {
  "http": "http://46.36.65.10:3128",
  "https": "https://46.36.65.10:3128"
}
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
    thread_num = 5
    queue = qu.Queue()
    console_logger, result_logger = helper.setLogger('bad.log')

    urls = helper.import_url('bad_domain.txt',None,None)
    #proxys = helper.import_proxy('proxy.csv','comma')
    proxys = helper.import_proxy('proxy.csv','')
    console_logger.debug(proxys[0])
    #proxys=None
    
    #result_logger.debug(u'num,url:num_ip,reg_time,country,registrar')
    # start worker threads
    for i in range(thread_num):
        proxy_arr=[]
        if proxys:
            proxy_arr = proxys[int(i*len(proxys)/thread_num):int((i+1)*len(proxys)/thread_num)]
            #for p in proxys:
            #    print(str(p))
            #sys.exit(1)
        conn_timeout=7
        read_timeout=10
        max_attempt=2
        #print(proxy_arr)
        worker = wh.WhoisWorker(i, queue, proxy_arr,console_logger, result_logger,conn_timeout,read_timeout,max_attempt)
        worker.setDaemon(True)
        worker.start()
    
    for i,url in urls:
        queue.put((i,url))
    
    # Wait on the queue until all have been processed

    queue.join()

if __name__ == "__main__":
    main()
