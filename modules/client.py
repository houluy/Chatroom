import socket
import threading
from modules.log import set_logger
import json

max_byte = 1024
ALL = 'all' #Broadcast
logger = set_logger('client')
command_list = ['CG', 'EG', 'CN', 'CP', 'QG']

class Client():
    def __init__(self, name):
        self.name = name
        self.enable = False
        self.connection = {}

    def connect(self, host='localhost', port=12344):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            logger.error('Socket established error!')
            self.s.close()
            return
        try:
            self.s.connect((host, port))
            logger.info('Connecting to server...')
        except:
            logger.error('Server error!')
            self.s.close()
            return
        msg = {}
        msg['Command'] = 'SN'
        msg['Value'] = self.name
        name_str = json.dumps(msg)
        try:
            self.s.sendall(name_str.encode())
        except Exception as e:
            logger.error('Initialization error!')
            self.s.close()
            return
        res_bytes = self.s.recv(max_byte)
        res = json.loads(res_bytes.decode())
        if (res.get('Value') == 'Success'):
            logger.info('Connection is established, your name is {}'.format(self.name))
        else:
            logger.error('Error receive from servers!')
            print(res)
            return
                
    def _analyze_input(self, input_str):
        #Save the history--FIXME
        msg = {}
        input_slice = input_str.split(':')
        command = input_slice[0].upper()
        if (command == 'QUIT'):
            pass
            #self.disconnect_peer()
        elif (command == 'OL?' or command == 'GP?'):
            msg['Command'] = input_str
        elif command in command_list:
            msg['Command'] = command
            msg['Value'] = ':'.join(input_slice[1:])
        else:
            msg['Message'] = input_slice[1]
            msg['Dest'] = input_slice[0]
        return json.dumps(msg)

    def _analyze_receive(self, data_dic):
        if (data_dic.get('Response') == 'Online' or data_dic.get('Response') == 'Group'): 
            print('List: ' + str(data_dic.get('Value')).replace(':', ', ')) 
        elif (data_dic.get('Response') == 'Conf'):
            print(data_dic.get('Value'))
        else:
            msg = data_dic.get('Message')
            src_name = data_dic.get('Source')
            print('{} says: {}'.format(src_name, msg))

    def send(self):
        while True:
            input_str = input()
            data = self._analyze_input(input_str)
            self.s.sendall(data.encode())
            
    def receive(self):
        while True:
            data = self.s.recv(max_byte)
            data_dic = json.loads(data.decode())
            self._analyze_receive(data_dic)
            
    def __del__(self):
        self.s.close()

if __name__ == '__main__':
    your_name = input('Pleas input your name: ')
    client = Client(your_name)
    client.connect()
    #client.get_online_list()
    threads = []
    thread_send = threading.Thread(target=client.send)
    thread_receive = threading.Thread(target=client.receive)
    threads.append(thread_send)
    threads.append(thread_receive)

    for th in threads:
        th.setDaemon(True)
        th.start()
    for th in threads:
        th.join()

