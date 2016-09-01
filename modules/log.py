import logging

def set_logger(user):
    logger = logging.getLogger('MainLogger')
    if (user == 'server'):
        log_format = '[%(asctime)-s %(levelname)s]: %(relativeCreated)5d %(lineno)d %(threadName)s \n%(message)s'
    elif (user == 'client'):
        log_format = '[%(asctime)-s %(levelname)s]: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    return logger

