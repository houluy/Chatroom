import logging
import threading

def set_logger(user):
    logger = logging.getLogger('MainLogger')
    if (user == 'server'):
        log_format = '[%(asctime)-s %(levelname)s]: %(relativeCreated)5d %(lineno)d %(threadName)s \n%(message)s'
    elif (user == 'client'):
        log_format = '[%(asctime)-s %(levelname)s]: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    return logger

threads = []
def threaded(fn):
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=fn, args=args, kwargs=kwargs)
        threads.append(th)
    return wrapper

def get_suffix(filename):
    file_slice = filename.split('.')
    if (len(file_slice) == 1):
        #No suffix
        return ''
    else:
        return file_slice[-1]

def read_file(filename):
    try:
        f = open(filename, 'r')
        data = f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError
    else:
        f.close()
    return data

