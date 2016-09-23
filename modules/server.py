import socket
import threading
import socketserver
import time
import json
from modules.log import set_logger

max_conn = 100
max_byte = 1024

request_dic = {}

object_dic = {}

relation_dic = {}

online_list = []
group_list = []

message_dic = {
    'Success':'successful',
    'Failure':'failed'
}

group_dic = {}

query_dic = {'OL?':'Online', 'GP?':'Group', 'BL?':'Black'}

logger = set_logger('server')

def respond(sock, command='Resp', message='Success', src_name='server', target=''):
    msg = dict(Command=command)
    if (command == 'Resp'):
        #Command type response
        logger.info(message)#: request is '{}'.format(message_dic[message]))
        msg.update(Value=message)
    elif command in query_dic.values():
        #Query type response
        #log out specific message--FIXME
        logger.info(message)
        msg.update(Value=message)
    sock.sendall(json.dumps(msg).encode())

def check_dup_name(name, name_list):
    if name in name_list:
        logger.info('Name: {} already exists'.format(name))
        return True 
    else:
        return False

class TCPHandler(socketserver.BaseRequestHandler):
    def handle_command(self, msg):
        command = msg.get('Command')
        value = msg.get('Value')
        message = ''
        com = 'Resp'
        if (command == 'SN'):#Set name
            if check_dup_name(value, online_list):
                message='Name {} already exists'.format(value)
            else:
                self.name = value
                logger.info('Set name with {}'.format(self.name))
                request_dic[self.name] = self.request
                object_dic[self.name] = self
                online_list.append(self.name)
                message='Success'
        elif command in query_dic.keys():
            com = query_dic.get(command)
            message=self.query_func(query_dic[command], self.name)
        elif (command == "CG"):#create group
            if check_dup_name(value, group_list):
                message='Group name \'{}\' already exists'.format(value)
            else:
                group_name = value
                group_list.append(group_name)
                group_dic[group_name] = []
                group_dic[group_name].append(self.name)
                message = 'Group {} has been created successfully'.format(group_name)
        elif (command == 'EG'):#enter group
            group_name = value
            if (group_name not in group_list):
                message = 'Group {} has not been created yet'.format(group_name)
            else:
                group_dic[group_name].append(self.name)
                message = 'You have successfully entered group {}'.format(group_name)#Also respond with group info--TODO
        elif (command == 'CN'):#change name
            new_name = value
            online_list.remove(self.name)
            online_list.append(new_name)
            request_dic[new_name] = request_dic.pop(self.name)
            self.name = new_name
            message = 'Your name has been changed to {} successfully'.format(self.name) 
        elif (command == 'CP'):#change group name
            old_name = value.split(':')[0]
            if old_name not in group_list:
                message = 'There is no group with name {}'.format(old_name)
            else:
                new_name = value.split(':')[1]
                group_list.remove(old_name)
                group_list.append(new_name)
                group_dic[new_name] = group_dic.pop(old_name)
                message = 'Group name has been changed to {} successfull'.format(new_name)
                #Inform all the clients in this group--FIXME
                #msg['Dest'] = new_name
                #msg['Message'] = 'Group name {} has been changed to {} by {}.'.format(old_name, new_name, self.name)
                #self.distribute_msg(msg)
        elif (command == 'QG'):#quit group
            group_name = value
            if group_name not in group_list:
                message = 'No such group exists'
            elif self.name not in group_dic[group_name]:
                message = "You haven't entered group {}".format(group_name)
            else:
                group_dic[group_name].remove(self.name)
                message = "You have successfully leave the group {}".format(group_name)
        elif (command == 'BL'):#black list
            self.black_list += value.split(':')    
            message = "You have moved {} to the blacklist, you will no longer hear from he/she".format(value)
        elif (command == ""):
            pass
        respond(self.request, command=com, message=message, target=self.name)

    def query_func(self, query_obj, client_name):
        if (query_obj == 'Online'):
            query_str = 'online'
            article = 'An'
            result = ':'.join(online_list)
        elif (query_obj == 'Group'):
            query_str = 'group'
            article = 'A'
            result = ':'.join(group_list)
        elif (query_obj == 'Black'):
            query_str = 'black'
            article = 'A'
            result = ':'.join(self.black_list)
        logger.info('{} {} list query request from {} is received'.format(article, query_str, client_name))
        return result

    def distribute_msg(self, message):
        src_name = self.name
        dst_name = message.get('dst')
        file_type = message.get('flt')
        data = message.get('msg')
        timestamp = message.get('tim')
        reply_msg = dict(src=src_name, dst=dst_name, flt=file_type, msg=data, tim=timestamp)
        reply_pac = dict(Command='MG', Value=reply_msg)
        reply = json.dumps(reply_pac).encode()
        if (dst_name in online_list):
            #Check black list
            if src_name not in object_dic[dst_name].black_list:
                dst_request = request_dic[dst_name]
                dst_request.sendall(reply)
            else:
                message = 'You are in the target\'s black list!'
                respond(self.request, message=message, target=dst_name)
        elif (dst_name in group_list):
            for dst_temp in group_dic[dst_name]:
                if (dst_temp == self.name):
                    continue
                dst_request = request_dic[dst_temp]
                dst_request.sendall(reply)
        else:
            message = 'Target user or group does not exist!'
            respond(self.request, message=message, target=self.name)

    def handle(self):
        self.black_list = []
        while True:
            data = self.request.recv(max_byte)
            msg = json.loads(data.decode())
            logger.info('Original data:"{}"'.format(msg)) 
            command = msg.get('Command')
            if (command != 'MG'):
                self.handle_command(msg)
            elif (command == 'MG'):
                self.distribute_msg(msg.get('Value'))
                                
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    ThreadedTCPServer.allow_reuse_address = True
    server = ThreadedTCPServer(('localhost', 11234), TCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.damon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread)
