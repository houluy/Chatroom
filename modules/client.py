import socket
import threading
from log import set_logger

max_byte = 1024
ALL = 'all' #Broadcast
data_prefix = 'DATA:'
logger = set_logger('client')

class Client():
    def __init__(self, name):
        self.name = name
        self.enable = False
        self.connection = {}

    def connect(self, host='localhost', port=12344):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print('Socket established error!')
            print(e)
            self.s.close()
            return
        try:
            self.s.connect((host, port))
            logger.info('Connecting to server...')
        except:
            print('Server error!')
            self.s.close()
            return
        name_str = ''.join(['setname:', self.name])
        try:
            self.s.sendall(bytes(name_str, encoding='utf8'))
        except Exception as e:
            print('Initialization error!')
            self.s.close()
            return
        res = self.s.recv(max_byte)
        if (res.decode() == 'Success'):
            logger.info('Connection is established, your name is {}'.format(self.name))
            print()
            #print('Please type in "OL?" to get the online list first: ', end='')
        else:
            print('Error receive from servers!')
            print(res)
            return
                
    def _send_command(self, command):
        self.s.sendall(bytes(target_str, encoding='utf8'))
        res = self.s.recv(max_byte)
        if (res == 'Success'):
            logger.info('{} successfully'.format(command))
        else:
            print('Error command return')

    def _analyze(self):
        pass

    #Merge the following two functions--FIXME
    def get_list(self, lst_name):
        self.s.sendall(lst_name.encode())

    #def create_group(self):
    #    group_name = input("Please input the group name: ")
    #    self.s.sendall('cgroup:' + group_name)

    def connect_peer(self):
        self.target = input("Target name:")
        target_str = ''.join(['target:', self.target])
        try:
            self.s.sendall(bytes(target_str, encoding='utf8'))
            #res = self.s.recv(max_byte)
        except:
            print('Error connecting to peer')
            return
        
    def disconnect_peer(self):
        disconnect_str = ''.join(['disconnect:', self.target])
        self.s.sendall(bytes(disconnect_str, encoding='utf8'))
        res = self.s.recv(max_byte)

    def send(self):
        while True:
            input_str = input()
            #Save the history--FIXME
            if (input_str == 'quit'):
                self.disconnect_peer()
            elif (input_str == 'OL?' or input_str == 'GP?'):
                self.get_list(input_str)
            else:
            #Talk
                input_slice = input_str.split(':')
                if (input_slice[0] == 'cgroup' or input_slice[0] == 'egroup'):
                    self.s.sendall(bytes(input_str, encoding='utf8'))
                else:
                    self.s.sendall(bytes('DATA:' + input_str, encoding='utf8'))

    def receive(self):
        while True:
            self.data = self.s.recv(max_byte)
            data_slice = self.data.decode().split(':')
            if (data_slice[0] == 'Online' or data_slice[0] == 'Group'): 
                print(data_slice[0] + ' list: ' + str(data_slice[1:])) 
            elif (data_slice[0] == 'command'):
                print(':'.join(data_slice[1:]))
            else:
                src_name = data_slice[0]
                src_data = data_slice[1:]
                print('{} says: {}'.format(src_name, ':'.join(src_data)))

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

