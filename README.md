# FTP-Server
The File Transfer Protocol (FTP) is a standard communication protocol used for the transfer of computer files from a server to a client on a computer network. FTP is built on a client–server model architecture. The FTP server is implemented in Python using TCP sockets and explains the basic working principles of an FTP server. 

## Features:
- Multi-threaded server(a new thread is created for each client)
- User Credential check
- Seperate Directories for Users
- Receive and Store files on the server.
- Interface with generic FTP clients(Eg. Filezilla)

## Requirements
-Python3
- os module `pip install os-sys`
- threading module `pip install threaded`
- socket module `pip install sockets`

## Running the code
It is crucial to run the server before running the client. <br/>
Running the server.<br/>
`Python3 server4.py`<br/>
Running the client.<br/>
`Python3 client.py`

## User Credentials
The usernames and passwords are stored in users.txt.



