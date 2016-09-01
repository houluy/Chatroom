import socket
import threading
import socketserver
import time
from modules.log import set_logger

max_conn = 100
max_byte = 1024

request_dic = {}

relation_dic = {}

online_list = []
group_list = []

message_dic = {
    'Success':'successful',
    'Fail':'failed'
}

group_dic = {}

command_dic = {'OL?':'Online_list', 'GP?':'Group_list'}

logger = set_logger('server')

def respond(sock, message='Success', src_name='', target=''):
    if (message in message_dic):
        logger.info('Response from server: request is {}'.format(message_dic[message]))
    elif (src_name == 'server'):
        #log out specific message--FIXME
        logger.info('Server command responding')
    else:
        logger.info('{} says to {}: {}'.format(src_name, target, message))
    sock.sendall(message.encode())

def query_func(query_obj, client_name):
    if (query_obj == 'Online_list'):
        query_str = 'online'
        article = 'An'
        result = ':'.join(online_list)
    elif (query_obj == 'Group_list'):
        query_str = 'group'
        article = 'A'
        result = ':'.join(group_list)
    logger.info('{} {} list query request from {} is received'.format(article, query_str, client_name))
    return query_str.capitalize() + ':' + result

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(max_byte)
            data_slice = self.data.decode().split(':')
            logger.info('Original data:"{}"'.format(self.data.decode())) 
            if (data_slice[0] == 'setname'):
                self.name = data_slice[1]
                #Check duplication of name
                cur_thread = threading.current_thread()
                logger.info('Set name with {}'.format(self.name))
                request_dic[self.name] = self.request
                online_list.append(self.name)
                respond(self.request)
            elif (data_slice[0] == 'OL?' or data_slice[0] == 'GP?'):
                self.request.sendall(query_func(command_dic[data_slice[0]], self.name).encode())
            elif (data_slice[0] == ""):
                logger.info('{} disconnects with server.'.format(self.name))
                online_list.pop(self.name)
            elif (data_slice[0] == "DATA"):
                src_name = self.name
                dst_name = data_slice[1]
                message = '{}:{}'.format(src_name, ':'.join(data_slice[2:]))
                if (dst_name in online_list):
                    dst_request = request_dic[dst_name]
                    respond(dst_request, message, src_name, dst_name)
                elif (dst_name in group_list):
                    for dst_temp in group_dic[dst_name]:
                        if (dst_temp == self.name):
                            continue
                        dst_request = request_dic[dst_temp]
                        respond(dst_request, message, src_name, group_name) 
                else:
                #Error group name--FIXME
                    pass
                #logger.info('{} says to {}: {}'.format(self.name, self.target, self.data.decode()))
                #request_dic[self.target].sendall(''.join([self.name, ':', self.data.decode()]).encode())
                #self.request.sendall(response)
            elif (data_slice[0] == "cgroup"):#create group
                group_name = data_slice[1]
                #Check duplication of group name--FIXME
                group_list.append(group_name)
                group_dic[group_name] = []
                group_dic[group_name].append(self.name)
                message = 'command:Group {} has been created successfully'.format(group_name)
                respond(self.request, message, 'server', self.name)
            elif (data_slice[0] == 'egroup'):#enter group
                group_name = data_slice[1]
                if (group_name not in group_list):
                    message = 'command:Group {} has not been created yet'.format(group_name)
                    respond(self.request, message, 'server', self.name)
                else:
                    group_dic[group_name].append(self.name)
                    message = 'command:You have successfully entered group {}'.format(group_name)#Also respond with group info--FIXME
                    respond(self.request, message, 'server', self.name)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer(('localhost', 11234), TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.damon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread)
    #server.shutdown()
    #server.server_close()
