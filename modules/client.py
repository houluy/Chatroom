import socket
import threading
from modules.log import set_logger
import json

max_byte = 1024
ALL = 'all' #Broadcast
logger = set_logger('client')
command_list = ['CG', 'EG', 'CN', 'CP', 'QG', 'BL']
query_list = ['OL?', 'GP?', 'BL?', 'Online', 'Group', 'Black']

threads = []

def threaded(fn):
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=fn, args=args, kwargs=kwargs)
        threads.append(th)
    return wrapper

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

    def disconnect(self):
        logger.info('Disconnecting...')
        self.s.close()
        logger.info('Bye Bye')
                
    def _analyze_input(self, input_str):
        #Save the history--FIXME
        msg = {}
        input_slice = input_str.split(':')
        command = input_slice[0].upper()
        if (command == 'QUIT'):
            self.disconnect()
            return -1
        elif command in query_list:
            msg['Command'] = input_str
        elif command in command_list:
            msg['Command'] = command
            msg['Value'] = ':'.join(input_slice[1:])
        else:
            msg['Dest'] = input_slice[0]
            if (input_slice[1].upper() == 'FILE'):
                #Send file
                #Check file path--FIXME
                msg['Message'] = ':'.join('FILE', self._read_file(input_slice[2]))
            else:
                msg['Message'] = input_slice[1]
        self.s.sendall(json.dumps(msg).encode())
        return 0

    def _analyze_receive(self, data_dic):
        if data_dic.get('Response') in query_list:
            print('{} List: '.format(data_dic.get('Response')) + str(data_dic.get('Value')).replace(':', ', ')) 
        elif (data_dic.get('Response') == 'Conf'):
            print(data_dic.get('Value'))
        else:
            msg = data_dic.get('Message')
            msg_slice = msg.split(':')
            #if (msg_slice[0].upper() == 'FILE'):
            src_name = data_dic.get('Source')
            dst_name = data_dic.get('Dest')
            if (dst_name == self.name):
                print('{} says to you: {}'.format(src_name, msg))
            else:
                print('{} says in group <{}>: {}'.format(src_name, dst_name, msg))

    def _read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    @threaded
    def send(self):
        while True:
            input_str = input()
            data = self._analyze_input(input_str)
            if (data == -1):
                break
    
    @threaded
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
    client.send()
    client.receive()
    
    for th in threads:
        th.setDaemon(True)
        th.start()
    for th in threads:
        th.join()

