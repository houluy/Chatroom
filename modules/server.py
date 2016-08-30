import socket
import threading
import socketserver
import logging
import time

max_conn = 100
max_byte = 1024

logger = logging.getLogger('MainLogger')
log_format = '[%(levelname)s] %(asctime)-s %(relativeCreated)5d %(lineno)d %(threadName)s \n%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

request_dic = {}

relation_dic = {}

online_list = []

message_dic = {
    'Success':'successful',
    'Fail':'failed'
}

def respond(sock, message='Success', src_name='', target=''):
    if (message in message_dic):
        logger.info('Response from server: request is {}'.format(message_dic[message]))
    elif (src_name == 'server'):
        logger.info('Server command responding')
    else:
        logger.info('{} says to {}: {}'.format(src_name, target, message))
    sock.sendall(message.encode())

class TCPHandler(socketserver.BaseRequestHandler):
    #def __init__(self):
    #    #super(socketserver.BaseRequestHandler, self).__init__()
    #    self.name = ''

    def handle(self):
        while True:
            self.data = self.request.recv(max_byte)
            data_slice = self.data.decode().split(':')
            logger.info('Original data:"{}"'.format(self.data.decode())) 
            if (data_slice[0] == 'setname'):
                self.name = data_slice[1]
                cur_thread = threading.current_thread()
                logger.info('Set name with {}'.format(self.name))
                request_dic[self.name] = self.request
                online_list.append(self.name)
                respond(self.request)
            elif (data_slice[0] == 'Online_list'):
                logger.info('An online list request by {} is received'.format(self.name))
                online_list_str = 'Online:' + ':'.join(online_list)
                self.request.sendall(online_list_str.encode())
            elif (data_slice[0] == ""):
                logger.info('{} disconnects with server.'.format(self.name))
                online_list.pop(self.name)
            elif (data_slice[0] == "DATA"):
                src_name = self.name
                dst_name = data_slice[1]
                dst_request = request_dic[dst_name]
                message = '{}:{}'.format(src_name, ':'.join(data_slice[2:]))
                respond(dst_request, message, src_name, dst_name)
                #logger.info('{} says to {}: {}'.format(self.name, self.target, self.data.decode()))
                #request_dic[self.target].sendall(''.join([self.name, ':', self.data.decode()]).encode())
                #self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer((host, port), TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.damon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread)
    #server.shutdown()
    #server.server_close()
