from modules.client import Client
import threading
import logging

object_host = 'localhost'
object_port = 12344

your_name = input('Pleas input your name:')
client = Client(your_name)
client.connect(object_host, object_port)
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

