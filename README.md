<font face="Corbel" size=4>
# Chatroom #  
Author: LuCima   
Email:  <houlu@lucima.cn>  

A free chatroom for CLI by Python

This is a chatroom software that can run in CLI in Linux. Users can firstly run chat\_server.py. Then, multi-clients can be started and chat with each other. 

This is a preliminary version that only simple chatting function is supported. Coming soon...

[Aug.  30. 2016] Basic functions implemented.  
[Sept. 01. 2016] Add group function  
[Sept. 03. 2016] Change all data format into JSON  
[Sept. 08. 2016] Add (1)change group name; (2)leave group; (3)change client name; (4)bug fix.  

### [Interaction process]  

1. Connect to server
2. Client.py start two threads, one for sending and the other for receiving
3. Set client name, command: 'SN:<name\>', server return 'Success' or 'Failure'
4. Client can get an online list from server by command: 'OL?'
5. Server returns an online list which shows all the current users, format: 'Online:<name1\>:<name2\>...'
6. Client can send messages to any user they want, format: '<name\>:<msg\>', e.g., 'Mary: hello'
7. Client can change their name by command: 'CN:<new\_name\>'.


### [Group talk]

1. Any client can create a non-existing group by typing: 'CG:<name\>'
2. By command 'GP?', clients can check the existing group, format: 'Group:<group1\>:<group2\>...'
3. 'EG:<name\>' enables a client to enter the group with <name>
4. Client can send messages to a group just as to common users: '<group\>:<msg\>', all clients that have entered the group can receive the msg. 
5. Group clients can change the group name by command: 'CP:<old\_name\>:<new\_name\>'.
6. Clients in a group can leave the group by command: 'QG:<group\>'.

### [Black list]

1. Client can move some one to its blacklist so that it will not hear from the one, command: 'BL:<name1\>:<name2\>...'.
2. By simply typing: 'BL?', clients can check their black lists.  

--- 

## JSON Structure:

<font face="Courier New" color="0x993399">Client:  
{  
　　Command: <command\>,  
　　Value: <val\>,  
　　Message: <msg\>,  
　　Dest: <name\>,  
}  </font>

Command includes:    
　　+	OL?                         					: Get current online list  
　　+	GP?                         					: Get current chatting group  
　　+	BL?                         					: Get black list  
　　+	CG:<name\>                  				: Create a new group  
　　+	EG:<name\>                  				: Enter a group  
　　+	CN:<name\>                  				: Change name  
　　+	QG:<group\>                  			: Quit a group  
　　+	CP:<old\_group\>:<new\_group\>  : Change group name  
　　+	BL:<name1\>:<name2\>...       		: Move name1... to the black list  

<font face="Courier New" color="0x993399">Server:  
{  
　　Response: <command\>,  
　　Value: <val\>,  
　　Message: <msg\>,  
　　Source: <name\>,  
　　Dest: <name\>,  
}</font>

Command includes:  
　　+	Online    : Online list    
　　+	Group     : Group list  
　　+	Conf        : State of configuration (Success or Failure)  
　　+	Data        : Chatting data    

</font>