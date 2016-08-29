import socket
import threading

max_byte = 1024
ALL = 'all' #Broadcast
con = threading.Condition()

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

    def send(self):
        global con
        con.acquire()
        self.connect_peer()
        con.wait()
        while True:
            data = input()
            #Save the history
            if (data == 'quit'):
                self.disconnect_peer()
            else:
                self.s.sendall(bytes(data, encoding='utf8'))
        con.release()

    def receive(self):
        global con
        con.acquire()
        while True:
            data = self.s.recv(max_byte).decode()
            if (data):
                data_slice = data.split(':')
                if (data_slice[0] == 'name'):
                    peer_name = data.split(':')[1]
                    accept = input("{} wants to talk with you, accept? Y/N".format(peer_name))
                    if (accept == 'Y') or (accept == 'y'):
                        self.connection[peer_name] = 0
                        try:
                            self.s.sendall('accept:{}:Y'.format(peer_name).encode())
                        except:
                            print('Send error in receive function')
                    else:
                        pass
                elif (data_slice[0] == 'accept'):
                    peer_name = data.split(':')[1]
                    self.connection[peer_name] = 1
                    con.release()
                else:
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
    thread_talk = threading.Thread(target=client.send)
    thread_receive = threading.Thread(target=client.receive)
    threads.append(thread_talk)
    threads.append(thread_receive)

    for th in threads:
        th.setDaemon(True)
        th.start()
    for th in threads:
        th.join()

