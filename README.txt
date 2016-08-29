# Chatroom
A free chatroom for CLI by Python

This is a chatroom software that can run in CLI in Linux. Users can firstly run chat_server.py. Then, multi-clients can be started and chat
with each other. 

This commit is the first one that only simple chatting function is supported. Coming soon...

[Interaction process]
1. Connect to server
2. Client.py start two threads, one for sending and the other for receiving
3. Set client name, command: 'setname:<name>', server return 'Success' or 'Failure'
4. Choose the target to talk with, command: 'target:<name>', then send thread waits
5. Server sends request to the target client, command: 'name:<name>', and wait for confirmation
6. The target client accept the request, command: 'accept:<name>:Y', or decline, command: 'decline:<name>:N', <name> stands for the name of request client
7. Server sends the acceptance message to the request client, command: 'accept:<name>:Y', or decline, command: 'decline:<name>:N', <name> stands for the target name
8. If accept, they can chat with each other by add the peer name, e.g., 'Mary:hello'
