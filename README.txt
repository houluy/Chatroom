# Chatroom
A free chatroom for CLI by Python

This is a chatroom software that can run in CLI in Linux. Users can firstly run chat_server.py. Then, multi-clients can be started and chat
with each other. 

This is a preliminary version that only simple chatting function is supported. Coming soon...

[Sept. 01. 2016] Add group function
[Sept. 03. 2016] Change all data format into JSON

[Interaction process]

1. Connect to server
2. Client.py start two threads, one for sending and the other for receiving
3. Set client name, command: 'setname:<name>', server return 'Success' or 'Failure'
4. Client can get an online list from server by command: 'OL?'
5. Server returns an online list which shows all the current users, format: 'Online:<name1>:<name2>...'
6. Client can send messages to any user they want, format: '<name>:<msg>', e.g., 'Mary: hello'

[Group talk]

1. Any client can create a non-existing group by typing: 'CG:<name>'
2. By command 'GP?' clients can check the existing group, format: 'Group:<group1>:<group2>...'
3. 'EG:<name>' enables a client to enter the group with <name>
4. Client can send messages to a group just as to common users: '<group>:<msg>', all clients that have entered the group can receive the msg. 

JSON Structure:

Client:

{
    Command: <command>,
    Value: <val>,
    Message: <msg>,
    Dest: <name>,
}

Command includes:
OL?         : Get current online list
GP?         : Get current chatting group
CG:<name>   : Create a new group
EG:<name>   : Enter a group

Server:
{
    Response: <command>,
    Value: <val>,
    Message: <msg>,
    Source: <name>,
}

Command includes:
Online      : Online list
Group       : Group list
Conf        : State of configuration (Success or Failure)
Data        : Chatting data
