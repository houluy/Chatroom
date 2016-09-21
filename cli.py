from modules.client import Client, threads
import threading
import logging

object_host = 'localhost'
object_port = 12344

your_name = input('Pleas input your name:')
client = Client(your_name)
client.connect(object_host, object_port)
client.send()
client.receive()

for th in threads:
    th.setDaemon(True)
    th.start()
for th in threads:
    th.join()

