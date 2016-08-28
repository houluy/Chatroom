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

message_dic = {
    'Success':'successful',
    'Fail':'failed'
}

def respond(sock, message='Success'):
    logger.info('Response from server: request is {}'.format(message_dic[message]))
    sock.sendall(message.encode())

class TCPHandler(socketserver.BaseRequestHandler):
    #def __init__(self):
    #    #super(socketserver.BaseRequestHandler, self).__init__()
    #    self.name = ''

    def handle(self):
        while True:
            self.data = self.request.recv(max_byte)
            data_slice = self.data.decode().split(':')
            if (data_slice[0] == 'setname'):
                self.name = data_slice[1]
                cur_thread = threading.current_thread()
                logger.info('Set name with {}'.format(self.name))
                request_dic[self.name] = self.request
                respond(self.request)
            elif (data_slice[0] == 'target'):
                self.target = data_slice[1]
                if self.target in list(request_dic.keys()):
                    self.target = data_slice[1]
                    logger.info('{} wants to talk with {}'.format(self.name, self.target))
                    respond(self.request)
                else:
                    respond(self.request, 'Fail')
            else:
                logger.info('{} says to {}: {}'.format(self.name, self.target, self.data.decode()))
                request_dic[self.target].sendall(''.join([self.name, ':', self.data.decode()]).encode())
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
