
import os
import socket
from stat import filemode
import threading
from typing import ForwardRef
import csv

outIP = '105.245.40.223'

IP = '127.0.0.1'
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
#DATA_PORT = 4467
filemode='r'
mode = 'w'
type = ''
DATAPORT = (127,0,0,1,17,116)
DATA_PORT = 4468
dataconn = ''


def user_find(ftpdata,conn,addr):
    founduser = False
    #search the file for the username given
    with open("user.txt", "r") as file:
        file_reader = csv.reader(file)
        
        for row in file:
            row  = row.split(',', 1)
            if row[0] ==ftpdata:
                msg="331 user name okay, need password \r\n"
                conn.send(msg.encode(FORMAT))
                file.close()
                founduser = True
                break

        if founduser==False:
            err="530 could not find user \n"
            conn.send(err.encode(FORMAT))
            #conn.close()
            print(f"[NEW CONNECTION] {addr} is failed to connect")
            file.close()

def PORT(data):
    #formatting the received input
    listT = data.split(',')
    upper = int(listT[4])
    lower = int(listT[5])
    clientIp = '.'.join(listT[:4])
    clientIp = '127.0.0.1'
    clientPort = 256*upper + lower
    adr=(clientIp, clientPort)
    print(adr)
    #active connection, try and connect to the port specified by the client
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(adr)
        
    except:
        print("data port not connected")
        pass
    message = "200 Entering Active Connection...\r\n"
    return clientSocket,message

def ftp_LIST(directory):
    print("in list")
    valid = os.path.isdir(directory)
    if valid:
        items = os.listdir(directory)
        response = []
        print(items)
        return items
			
def ftp_MakeDir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)	
		response = "200 Okay Directory created.\r\n"
	else:
		response = "550 Directory NOT created.\r\n"
	#endIf
	return response

def ftp_PASV(passDataSocket):
	print("Handling Passive Request")
	try:
		passDataSocket.listen()
	except:
		pass
		
	deviceIPaddr = socket.gethostbyname(socket.gethostname())
	deviceIPaddr = deviceIPaddr.replace('.',',')
	
	#deviceIPaddr = '127,0,0,1'
	
	port  = passDataSocket.getsockname()[1]
	port  = "{0:b}".format(port).zfill(16)
	upper = int(port[:8],2)
	lower = int(port[8:],2)
	
	#upper = 0
	#lower = 20
	
	address = deviceIPaddr+','+str(upper)+','+str(lower)
	response = '227 Entering Passive Mode ('+address+')\r\n'
	return response

def upload(filename,dataconn):
    print(filename)
    #only allow ascii files
    mode='r'
    print("Opening the file")
    #read the file in chucks and send to the client
    with open(filename, mode) as theFile:
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



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} is trying to connect")
    conn.send("220 Welcome to server \r\n".encode(FORMAT))
    user = []
    HomeDirectory=os.getcwd()

    while True:

        data = conn.recv(SIZE).decode(FORMAT)
        print(data)
        command  = data.split(' ', 1)
        ftpCommand  = (command[0].rstrip()).upper()
        ftpData		= command[-1].rstrip()


        if ftpCommand == "USER":
            print(ftpData)
            user = ftpData
            user_find(ftpData,conn,addr)

        if ftpCommand == "SYST":
            conn.send("215 Windows_NT \r\n".encode(FORMAT))

        if ftpCommand == "FEAT":
            conn.send("211 System Status \r\n".encode(FORMAT))

        if ftpCommand == "PWD":
            ftp_MakeDir(os.path.join(os.getcwd(),user) )
            HomeDirectory 	 = os.path.join(os.getcwd(),user) 
            msg = f'257 {HomeDirectory} created \r\n'
            conn.send(msg.encode(FORMAT))
            print("sent path")

        if ftpCommand == "TYPE":
            type = ftpData
            conn.send("200 Command okay \r\n".encode(FORMAT))

        if ftpCommand == "PASV":
            msg = f'227 Entering Passive Mode {DATAPORT} \r\n'
            conn.send(msg.encode(FORMAT))
    
        if ftpCommand == "PORT":
            dataconn,m = PORT(ftpData)
            conn.send(m.encode(FORMAT))

        if ftpCommand == "LIST":
            message = '200 List being send to Dataconnection.\n'
            conn.send(message.encode())
            print(HomeDirectory)
            items = ftp_LIST(HomeDirectory)
            if items!=None:
                for item in items:
                    dataconn.sendall((item+'\r\n').encode(FORMAT))
            message = '200 Listing completed.\r\n'
            conn.send(message.encode())
            dataconn.close()
            print("Listing completed...")

        if ftpCommand == "CWD":
                ftp_MakeDir(os.path.join(os.getcwd(),user) )
                HomeDirectory 	 = os.path.join(os.getcwd(),user) 
                message = "200 CWD changed \r\n"
                conn.send(message.encode(FORMAT))

        if ftpCommand == "RETR":
            message = '200 File being sent to Dataconnection.\r\n'
            conn.send(message.encode(FORMAT))
            home = os.path.join(os.getcwd(),user)
            file = home+"\\"+ftpData
            upload(file,dataconn)
            dataconn.close()
            message = "226 Transfer completed Closing data connection.\r\n"
            conn.send(message.encode(FORMAT))

        if ftpCommand == "STOR":
            message = '200 List being received to Dataconnection.\r\n'
            conn.send(message.encode(FORMAT))
            file = HomeDirectory + "\\" + user + "\\" + ftpData
            bytesToSave = dataconn.recv(SIZE)
            theFile = open(file, 'w')
            while bytesToSave:
                theFile.write(bytesToSave.decode(FORMAT))
                bytesToSave = dataconn.recv(SIZE)
            theFile.close()
            dataconn.close()
            message = "226 Transfer completed Closing data connection.\r\n"
            conn.send(message.encode(FORMAT))
            print("Download complete")

        if ftpCommand == "PASS":
            print(user)
            print(ftpData)
            with open("user.txt", "r") as file:
                file_reader = csv.reader(file)
                for row in file:
                    row  = row.split(',', 1)
                    if row[0] ==user:
                        if row[1]==ftpData:
                            msg="230 user logged in \r\n"
                            conn.send(msg.encode(FORMAT))
                            file.close()
                            break
                        else:
                            msg="530 wrong password \r\n"
                            conn.send(msg.encode(FORMAT))


            
            
            

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] sERVER IS LISTENING")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()