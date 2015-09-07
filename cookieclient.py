import socket
import os
import time
os.system('cls')
host = '192.168.0.23'
#port = int(input('ENTER PORT: '))
port = 900
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
    command = input("Enter your command/> ")
    if command == 'EXIT':
        s.send(str.encode(command))
        break
    elif command == 'KILL':
        s.send(str.encode(command))
        break
    if 'temp' in command or 't' in command:
        print('Wait for response...')
    if command is '':
        command = 'SWITCHCODE'
    s.send(str.encode(command))
    reply = s.recv(1024)
    os.system('cls')
    print('Last reply: ' + reply.decode('utf-8'))
    
    
s.close()
