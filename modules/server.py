import socket
import threading
import socketserver
import time
import json
from modules.log import set_logger

max_conn = 100
max_byte = 1024

request_dic = {}

relation_dic = {}

online_list = []
group_list = []

message_dic = {
    'Success':'successful',
    'Failure':'failed'
}

group_dic = {}

command_dic = {'OL?':'Online', 'GP?':'Group'}

logger = set_logger('server')

def respond(sock, command='Conf', message='Success', src_name='', target=''):
    msg = {}
    if (command == 'Conf'):
        logger.info('Response from server')#: request is {}'.format(message_dic[message]))
        msg['Response'] = command
        msg['Value'] = message
    elif (command == 'Online' or command == 'Group'):
        #log out specific message--FIXME
        logger.info('Server command responding')
        msg['Response'] = command
        msg['Value'] = message
    elif (command == 'Data'):
        logger.info('{} says to {}: {}'.format(src_name, target, message))
        msg['Message'] = message
        msg['Source'] = src_name
    sock.sendall(json.dumps(msg).encode())

def query_func(query_obj, client_name):
    if (query_obj == 'Online'):
        query_str = 'online'
        article = 'An'
        result = ':'.join(online_list)
    elif (query_obj == 'Group'):
        query_str = 'group'
        article = 'A'
        result = ':'.join(group_list)
    logger.info('{} {} list query request from {} is received'.format(article, query_str, client_name))
    return result


class TCPHandler(socketserver.BaseRequestHandler):
    def handle_command(self, msg, command):
        if (command == 'SN'):
            #Set name
            self.name = msg.get('Value')
            #Check duplication of name
            logger.info('Set name with {}'.format(self.name))
            request_dic[self.name] = self.request
            online_list.append(self.name)
            respond(self.request)
        elif (command == 'OL?' or command == 'GP?'):
            respond(self.request, command_dic[command], query_func(command_dic[command], self.name), 'server', self.name)
        elif (command == "CG"):#create group
            group_name = msg.get('Value')
            #Check duplication of group name--FIXME
            group_list.append(group_name)
            group_dic[group_name] = []
            group_dic[group_name].append(self.name)
            message = 'Group {} has been created successfully'.format(group_name)
            respond(self.request, 'Conf', message, 'server', self.name)
        elif (command == 'EG'):#enter group
            group_name = msg.get('Value')
            if (group_name not in group_list):
                message = 'Group {} has not been created yet'.format(group_name)
                respond(self.request, 'Conf', message, 'server', self.name)
            else:
                group_dic[group_name].append(self.name)
                message = 'You have successfully entered group {}'.format(group_name)#Also respond with group info--FIXME
                respond(self.request, 'Conf', message, 'server', self.name)
        elif (command == ""):
            pass
            #logger.info('{} disconnects with server.'.format(self.name))
            #online_list.pop(self.name)

    def distribute_msg(self, msg, src):
        src_name = self.name
        dst_name = msg.get('Dest')
        message = msg.get('Message')
        if (dst_name in online_list):
            dst_request = request_dic[dst_name]
            respond(dst_request, 'Data', message, src_name, dst_name)
        elif (dst_name in group_list):
            for dst_temp in group_dic[dst_name]:
                if (dst_temp == self.name):
                    continue
                dst_request = request_dic[dst_temp]
                respond(dst_request, 'Data', message, src_name, dst_name) 
        else:
        #Error group name--FIXME
            pass

    def handle(self):
        while True:
            data = self.request.recv(max_byte)
            msg = json.loads(data.decode())
            logger.info('Original data:"{}"'.format(msg)) 
            command = msg.get('Command')
            if (command):
                self.handle_command(msg, command)
            elif (command == None):
                self.distribute_msg(msg, self.name)
                                
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    ThreadedTCPServer.allow_reuse_address = True
    server = ThreadedTCPServer(('localhost', 11234), TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.damon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread)
    #server.shutdown()
    #server.server_close()
