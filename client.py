import socket
import threading
import sys
import os
import traceback

serverAddress = ('127.0.0.1',4466)
SIZE = 1024
FORMAT = "utf-8"
DATAPORT = '127,0,0,1,17,116'
DATA_PORT = 4468
ADDR = ('127.0.0.1',4468)


def main():
    print("client initialised")
    conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    conn.connect(serverAddress)
    data = conn.recv(SIZE).decode(FORMAT)
    print(data)
    user = input("Enter username: ")
    msg = "USER "+ user
    conn.send(msg.encode(FORMAT))
    data = conn.recv(SIZE).decode(FORMAT)
    print(data)
    password = input("Enter password: ")
    msg = "PASS "+ password
    conn.send(msg.encode(FORMAT))
    data = conn.recv(SIZE).decode(FORMAT)
    print(data)
    while True:
        cmd = input("> ")
        #format the input
        command  = cmd.split(' ', 1)
        ftpCommand  = (command[0].rstrip()).lower()
        ftpData		= command[-1].rstrip()

        if ftpCommand == "ls":
            #create an active connection with server, a seperate data connection
            msg = f"PORT {DATAPORT}"
            conn.send(msg.encode(FORMAT))
            datacon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            datacon.bind(ADDR)
            datacon.listen()
            dataconn, addr = datacon.accept()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            #send a command to list the files in the server directory
            msg = "LIST"
            conn.send(msg.encode(FORMAT))
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            bytesToSave = dataconn.recv(SIZE)
            #receive the files and print on screen
            print('Receiving files')
            while bytesToSave:
                print(bytesToSave.decode(FORMAT))
                bytesToSave = dataconn.recv(SIZE)
            dataconn.close()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)

        if ftpCommand == "get":
            #create an active connection with server, a seperate data connection
            msg = f"PORT {DATAPORT}"
            conn.send(msg.encode(FORMAT))
            datacon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            datacon.bind(ADDR)
            datacon.listen()
            dataconn, addr = datacon.accept()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            #send a command to RETR a file from the server to the local computer
            msg = f"RETR {ftpData}"
            print(msg)
            conn.send(msg.encode(FORMAT))
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            HomeDirectory=os.getcwd() + "\\client"
            file = HomeDirectory + "\\" + ftpData
            bytesToSave = dataconn.recv(SIZE)
            theFile = open(file, 'w')
            print('Writing to file...')
            #retrieve the file in chucks and write it to a local file
            while bytesToSave:
                theFile.write(bytesToSave.decode(FORMAT))
                bytesToSave = dataconn.recv(SIZE)
            theFile.close()
            dataconn.close()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)

        if ftpCommand == "put":
            #create an active connection with server, a seperate data connection
            msg = f"PORT {DATAPORT}"
            conn.send(msg.encode(FORMAT))
            datacon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            datacon.bind(ADDR)
            datacon.listen()
            dataconn, addr = datacon.accept()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            #send a command to STOR a file from the local computer to the server
            msg = f"STOR {ftpData}"
            print(msg)
            conn.send(msg.encode(FORMAT))
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)
            HomeDirectory=os.getcwd() + "\\client"
            file = HomeDirectory + "\\" + ftpData
            #set the default type to ascii files
            mode='r'
            print("Opening the file")
            #send the file in chuncks
            with open(file, mode) as theFile:
                bytesToSend = theFile.read(SIZE)
                dataconn.send(bytesToSend.encode(FORMAT))
                while bytesToSend:
                    prevBytes   = bytesToSend
                    bytesToSend = theFile.read(SIZE)
                    dataconn.send(bytesToSend.encode(FORMAT))
                    if not bytesToSend:
                        break
            print("Server Done uploding")
            theFile.close()
            datacon.close()
            data = conn.recv(SIZE).decode(FORMAT)
            print(data)

            if ftpCommand == "quit":
                conn.close()


if __name__ == "__main__":
    main()