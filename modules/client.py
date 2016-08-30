import socket
import threading

max_byte = 1024
ALL = 'all' #Broadcast
data_prefix = 'DATA:'

class Client():
    def __init__(self, name):
        #super(threading.Thread, self).__init__()
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
            print('Connecting to server...')
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
            print('Connection is established, your name is {}'.format(self.name))
            print('Please type in "OL?" to get the online list first: ', end='')
        else:
            print('Error receive from servers!')
            print(res)
            return
                
    def _send_command(self, command):
        self.s.sendall(bytes(target_str, encoding='utf8'))
        res = self.s.recv(max_byte)
        if (res == 'Success'):
            print('{} successfully'.format(command))
        else:
            print('Error command return')

    def _analyze(self):
        pass

    def get_online_list(self):
        self.s.sendall('Online_list'.encode())
        #self.data = self.s.recv(max_byte).decode()
        #data_slice = self.data.split(':')

    def connect_peer(self):
        self.target = input("Target name:")
        target_str = ''.join(['target:', self.target])
        try:
            self.s.sendall(bytes(target_str, encoding='utf8'))
            #res = self.s.recv(max_byte)
        except:
            print('Error connecting to peer')
            return
        
        #if (res == 'Success'):
        #    print('Connection with {} is successully established'.format(self.target))
        #else:
        #    print('Error name')
        #    return

    def disconnect_peer(self):
        disconnect_str = ''.join(['disconnect:', self.target])
        self.s.sendall(bytes(disconnect_str, encoding='utf8'))
        res = self.s.recv(max_byte)

    def send(self):
        while True:
            input_str = input()
            #Save the history
            if (input_str == 'quit'):
                self.disconnect_peer()
            elif (input_str == 'OL?'):
                self.get_online_list()
            else:
            #Talk
                input_slice = input_str.split(':')
                target_name = input_slice[0]
                #print('Says to {}: {}'.format(target_name, input_str))
                self.s.sendall(bytes(data_prefix + input_str, encoding='utf8'))

    def receive(self):
        while True:
            self.data = self.s.recv(max_byte)
            data_slice = self.data.decode().split(':')
            if (data_slice[0] == 'Online'): 
                print('Online list: ' + str(data_slice[1:])) 
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

