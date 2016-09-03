from modules.server import ThreadedTCPServer, TCPHandler
import threading
from modules.log import set_logger

host = 'localhost'
port = 12344

logger = set_logger('server')

ThreadedTCPServer.allow_reuse_address = True
server = ThreadedTCPServer((host, port), TCPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.damon = True
server_thread.start()
logger.info('Chat server is running at {}:{}'.format(host, port))

