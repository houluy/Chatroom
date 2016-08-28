from modules.server import ThreadedTCPServer, TCPHandler
import threading
import logging

host = 'localhost'
port = 12344

logger = logging.getLogger('MainLogger')

server = ThreadedTCPServer((host, port), TCPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.damon = True
server_thread.start()
logger.info('Chat server is running at {}:{}'.format(host, port))

