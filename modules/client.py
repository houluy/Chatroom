import socket
import threading
from .utils import *
import json
import time
import collections
from .chessboard.game import Game

max_byte = 1024
ALL = 'all' #Broadcast
logger = set_logger('client')
command_list = ['CG', 'EG', 'CN', 'CP', 'QG', 'BL']
query_list = ['OL?', 'GP?', 'BL?', 'GM?', 'Online', 'Group', 'Black', 'Game']
game_list = ['FOURINAROW', 'GOMOKU', 'TICTACTOE']

class Client():
    def __init__(self, name):
        self.name = name
        self.game = collections.defaultdict(dict)

    def _print_msg(self, src, dst, msg, timestamp):
        time_str = time.asctime(time.localtime(timestamp))
        if (dst == self.name):
            print('[{}] {} says to you: {}'.format(time_str, src, msg))
        else:
            print('[{}] {} says in group <{}>: {}'.format(time_str, src, dst, msg))

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
        #Change to a register process--TODO
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
        #Save the history--TODO
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
            command = 'MG'
            msg['Command'] = command
            dest = input_slice[0]
            message = dict(dst=dest)
            subcom = input_slice[1]
            if (subcom.upper() == 'FILE'):
                #Send file
                #Check file path--TODO
                #Transferred meaning of FILE--TODO
                filename = input_slice[2]
                file_type = get_suffix(filename)
                file_dat = read_file(filename)
                message.update(flt=file_type, msg=file_dat, tim=time.time())
            elif (subcom.upper() == 'PLAY'):
                gamename = input_slice[2]
                message.update(gme=gamename)
                new_game = Game(game=gamename)
                self.game[dest][gamename] = [new_game, 1]
            elif (subcom.upper() in game_list):
                move = input_slice[2]
                result = self.game[dest][subcom][0].place(move)
                if (result):
                    self._print_game_res(self.game[dest][subcom][1], result)
                message.update(msg=':'.join(input_slice[1:]))
            else:
                message.update(msg=':'.join(input_slice[1:]))
            msg.update(Value=message)
        return msg

    def _analyze_receive(self, data_dic):
        logger.info('Original data: {}'.format(str(data_dic)))
        command = data_dic.get('Command')
        message = data_dic.get('Value')
        if command in query_list:
            print('{} List: '.format(command) + str(message).replace(':', ', ')) 
        elif (command == 'Resp'):
            print(message)
        else:
            src_name = message.get('src')
            dst_name = message.get('dst')
            file_type = message.get('flt')
            data = message.get('msg')
            gamename = message.get('gme')
            timestamp = message.get('tim')
            if file_type:
                print('{} sends a {} file to you, check at default directory'.format(src_name, file_type))
                print(data)
            elif gamename:
                print('{} wants to play {} with you'.format(src_name, gamename))
                new_game = Game(game=gamename)
                self.game[src_name][gamename] = [new_game, 2]
                new_game.print_pos()
            else:
                data_slice = data.split(':')
                if (data_slice[0].upper() in game_list):
                    move = data_slice[1]
                    gamename = data_slice[0]
                    result = self.game[src_name][gamename][0].place(move)
                    if (result):
                        self._print_game_res(self.game[src_name][gamename][1], result)
                else:
                    self._print_msg(src_name, dst_name, data, timestamp)
    
    @threaded
    def send(self):
        while True:
            input_str = input()
            msg = self._analyze_input(input_str)
            if (msg == -1):
                break
            else:
                self.s.sendall(json.dumps(msg).encode())
    
    @threaded
    def receive(self):
        while True:
            data = self.s.recv(max_byte)
            data_dic = json.loads(data.decode())
            self._analyze_receive(data_dic)
            
    def __del__(self):
        self.s.close()

    def _print_game_res(self, seq, result):
        if (result == seq):
            print('You win!')
        elif (result != seq):
            print('You lose!')

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

