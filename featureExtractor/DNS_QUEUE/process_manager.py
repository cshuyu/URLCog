import psutil, subprocess
import project_logger as pl

def killProc(pid, log_name="ProcMgr"):
    try:
        logger = pl.loggers.getLogger(log_name)
        cmd = ['kill','-9','']
        cmd[2] = str(pid)
        subprocess.Popen(cmd)
    except Exception as e:
        logger.error("killProc exception %s" % str(e))
        return

def killProcR(parent_pid, log_name="ProcMgr"):
    try:
        logger = pl.loggers.getLogger(log_name)
        p = psutil.Process(parent_pid)
        child_pid = p.get_children(recursive=True)
        for pid in child_pid:
            killProcR(pid.pid)
        killProc(parent_pid)
    except Exception as e:
        logger.error("killProcR exception %s" % str(e))
        return