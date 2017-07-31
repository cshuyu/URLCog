import logging

class Logger:
    def __init__(self):
        self.loggers = {}
    
    ''' Logger setup method.  
        param log_filename     : the log's name. A logger file with
                               : the same name will be created in this
                               : directory.
        param output_to_console: if output to console is enabled.
                               : Its default value is True.
        ret type: logging.Logger
    '''
    def getLogger(self, log_name, output_to_console=True):
        if log_name in self.loggers:
            return self.loggers[log_name]
        logger = logging.getLogger(log_name)
        hdlr = logging.FileHandler('./'+log_name+'.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.addHandler(consoleHandler)
        logger.setLevel(logging.DEBUG)
        self.loggers[log_name] = logger
        return logger

''' export loggers '''
loggers = Logger()