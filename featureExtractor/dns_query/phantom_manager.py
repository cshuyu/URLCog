import argparse,Queue,os,time,sys
import psutil, uuid
import traceback
import urlparse
import threading, subprocess
from multiprocessing import Process
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from process_manager import killProcR
import project_logger as pl

loggers = pl.loggers
projName = "URLCog"
logger = loggers.getLogger(projName)

''' Randomly select a proxy from proxy list '''
def getRandomHTTPSProxy():
    #TODO: the candiadte list should be larger than 300
    return "104.236.166.203:3128"

''' Web retrieval task class '''
class Task:
    def __init__(self, url, time, proxy=None):
        self.url = url
        self.times = time
        self.proxy = proxy

''' Manager class to launch/stop web retrieval tasks'''
class Manager(threading.Thread):
    def __init__(self, task_queue, worker_count,
        timeout, user_agent, log_dir, worker_script_path):
        threading.Thread.__init__(self)
        self.__task_queue = task_queue
        self.__worker_count = worker_count
        self.__timeout = timeout
        self.__user_agent = user_agent
        self.__workers = []
        self.__log_dir = log_dir
        self.__total_worker_instances = 1
        self.__worker_script_path = worker_script_path
        logger.info("Manager get started")

    def __launch_worker(self, task):
        token = str(uuid.uuid4())
        try:
            # prepare log path
            o = urlparse.urlparse(task.url)
            host = o.netloc
            path_name = host + '_' + token
            full_path_name = os.path.join(self.__log_dir,path_name)
            if not os.path.exists(full_path_name):
                os.makedirs(full_path_name)
            
            # prepar args
            # note that phantomjs should be in your classpath.
            proxy_url = "--proxy="+getRandomHTTPSProxy()
            proxy_type = "--proxy-type=http"
            args = ['phantomjs']
            args[1:1] = [proxy_url, proxy_type, self.__worker_script_path, \
                task.url, str(task.times)]
            logger.info("Start worker for "+task.url+ " with proxy "+proxy_url)        
    
            # start worker process 
            worker = subprocess.Popen(
                args, 
                stdout=open(os.path.join(full_path_name,
                    'stdout.txt'), 'w'),
                stderr=open(os.path.join(full_path_name,
                    'stderr.txt'), 'w'))

            # [starting_time, url, times, popen-obj]
            worker_info = (int(time.time()),task.url, task.times, worker)
            time.sleep(1)

            # update worker info
            self.__total_worker_instances += 1
            self.__workers.append(worker_info)
            logger.info("[MAIN] successfully run " + worker_info[1] +
                " withpid:"+str(worker.pid)+
                ", full_path:" + full_path_name)
        except Exception as e:
            logger.error("failed to launch worker "+str(e))

    # Manager stays in this loop
    def run(self):
        while True:
            try:
                # check and kill dead process
                now = int(time.time())
                while len(self.__workers) > 0:
                    index = 0
                    for worker in self.__workers:
                        starting_time = worker[0]
                        proc = worker[3]
                        if now - starting_time > self.__timeout:
                            logger.info("[MAIN] TIMEOUT worker for %s with pid %d, kill it." 
                                % (worker[1], worker[3].pid) )
                            killProcR(worker[3].pid)
                            break
                        else:
                            code = proc.poll()
                            if code != None:
                                logger.info("[MAIN] worker for %s with pid[%s] exit[%s]" 
                                    % (worker[1], str(worker[3].pid), str(code)))
                                break
                            else:
                                logger.info("[MAIN] process %d is still running" % worker[3].pid)
                        index += 1
                    if index >= len(self.__workers):
                        logger.info("[MAIN] %d workers are in processing"
                            % len(self.__workers))
                        break
                    else:
                        # remove the structure of stopped/killed worker
                        del self.__workers[index] 

                # start task if there is any
                while len(self.__workers) < self.__worker_count:
                    try:
                        if len(self.__workers) > 0:
                            # Block when working instances
                            # used for reduce loop times.
                            task = self.__task_queue.get(True, 10)         
                            self.__launch_worker(task)
                        else:
                            task = self.__task_queue.get()
                            self.__launch_worker(task)
                    except Queue.Empty as e:
                        logger.debug("[MAIN] no other tasks to be allocated for now.")
                        break
                time.sleep(5)

            except Exception as e:
                traceback.print_exc()
                logger.error(
                    "[MAIN] error: "+str(e))   
                time.sleep(2) 

''' Task server running forever to receive new tasks '''
class MyHTTPServer(HTTPServer):
    def serve_forever(self, queue):
        self.RequestHandlerClass.task_queue = queue 
        HTTPServer.serve_forever(self)

class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type','text-html')
            self.end_headers()
            
            o = urlparse.urlparse(self.path)
            task = urlparse.parse_qs(o.query)
            logger.info("receive path: "+self.path);
            logger.info("receive task:" + str(task) )
            url = task['url'][0]
            times = int(task['times'][0])
            
            self.wfile.write("task received: %s for %d times\r\n" 
                %(url, times) );

            self.task_queue.put(Task(url,times))
            return
        except Exception as e:
            self.send_error(400, 'error'+str(e))

def main():
    queue = Queue.Queue()
    # testing cases
    queue.put(Task("https://www.google.com",3))
    queue.put(Task("http://whatismyipaddress.com/",3))
    queue.put(Task("https://mxtoolbox.com/SuperTool.aspx?action=a%3agoogle.com",3))
    
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0"
    if len(sys.argv) != 3:
        print "usage: python phantom_manager.py log_dir phanton_worker.js_path"
        return
    log_dir = sys.argv[1]
    worker_script_path = sys.argv[2]
    # args: queue, worker_count, timeout, user_agent, log_dir, worker_script_path
    manager = Manager(queue, 10, 120, user_agent,log_dir,worker_script_path)
    manager.start()
    time.sleep(10)
    server_address = ('127.0.0.1', 8082)
    
    httpd = MyHTTPServer(server_address, KodeFunHTTPRequestHandler)
    logger.info('http server is running...')
    httpd.serve_forever(queue)


if __name__ == "__main__":
	main()


