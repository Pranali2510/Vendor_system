import logging
import os

def add_log(pagename, methodname, exception, level, errorType = None):
    file_path = os.path.join(os.getcwd()+"/media/", "error_Log"+".log")
    logging.basicConfig(filename=file_path,format='%(asctime)s %(message)s',filemode='w')
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.error('This is an error message in pageName: '+str(pagename)+' ,Method: '+str(methodname) +' Exception: '+str(exception)+' and Type of error: '+str(errorType), exc_info=True)