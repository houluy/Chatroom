import socket
import threading

max_byte = 1024
ALL = 'all' #Broadcast

class Client():
    def __init__(self, name):
        #super(threading.Thread, self).__init__()
        self.name = name
        self.enable = False

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

    def talk(self):
        self.connect_peer()
        while True:
            data = input("Say:")
            #Save the history
            if (data == 'quit'):
                self.disconnect_peer()
            else:
                self.s.sendall(bytes(data, encoding='utf8'))

    def receive(self):
        while True:
            data = self.s.recv(max_byte).decode()
            if (data):
                peer_name = data.split(':')[0]
                words = ':'.join(data.split(':')[1:])
                print("{} says: {}".format(peer_name, words))
            else:
                print("Empty content received")
                continue

    def __del__(self):
        self.s.close()

if __name__ == '__main__':
    your_name = input('Pleas input your name:')
    client = Client(your_name)
    client.connect()
    threads = []
    thread_talk = threading.Thread(target=client.talk)
    thread_receive = threading.Thread(target=client.receive)
    threads.append(thread_talk)
    threads.append(thread_receive)

    for th in threads:
        th.setDaemon(True)
        th.start()
    for th in threads:
        th.join()

