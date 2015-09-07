import socket
import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
host = ''
#port = input('ENTER PORT: ')
port = 900
storedValue = 'Alright mate'

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print ('Bind complete')
    return s

def setupConnection():
    s.listen(1) #Allows one connection at a time.
    conn, address = s.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    return conn


def dataTransfer(conn):
    # A big loop that sends/receices data until told not to
    global killswitch
    killswitch = 0
    while True:
        # Recieve data
        data = conn.recv(1024) #Recieve the data
        data = data.decode('utf-8')
        # split the data to seperate the command from the rest of the data
        dataMessage = data.split(':', 1)
        command = dataMessage[0]

        statusFile = open('status.txt', 'r')
        locked = statusFile.readline()
        statusFile.close()
        statusFile2 = open('status2.txt', 'r')
        openTrigSwitch = statusFile2.readline()
        statusFile2.close()


        lockedreply = 'Unable to complete request, door is locked.'

        if command == 'open' and locked == '0' or command == 'o' and locked == '0':
            GPIO.setup(17, GPIO.OUT)
            reply = 'Open'
            openTrigSwitch = '1'
        elif command == 'open' and locked == '1' or command == 'o' and locked == '1':
            reply = lockedreply

        elif command == 'close' or command == 'c':
            GPIO.setup(17, GPIO.IN)
            reply = 'Closed'
            openTrigSwitch = '0'

        elif command == 'SWITCHCODE' and locked == '0':
            if openTrigSwitch == '0':
                GPIO.setup(17, GPIO.OUT)
                reply = 'Open'
                openTrigSwitch = '1'
            elif openTrigSwitch == '1':
                GPIO.setup(17, GPIO.IN)
                reply = 'Closed'
                openTrigSwitch = '0'
            else:
                reply = 'There has been a fuck up on openTrigSwitch'
                print(openTrigSwitch)
        elif command == 'SWITCHCODE' and locked == '1':
                reply = lockedreply


        elif command == 'temp' and locked == '0' or command == 't' and locked == '0':
            print('Open for ' + dataMessage[1])
            GPIO.setup(17, GPIO.OUT)
            time.sleep(int(dataMessage[1]))
            GPIO.setup(17, GPIO.IN)
            reply = 'Door was open for ' + str(dataMessage[1]) + ' seconds.'
            openTrigSwitch = '0'
        elif command == 'temp' and locked == '1' or command == 't' and locked == '1':
            reply = lockedreply


        elif command == 'lock' or command == 'l':
            fh = open('status.txt', 'w')
            fh.write('1')
            fh.close()
            reply = 'Locked to file'
            GPIO.setup(17, GPIO.IN)
            openTrigStwich = '0'
        elif command == '1553':
            fh = open('status.txt', 'w')
            fh.write('0')
            fh.close()
            reply = 'Unlocked to file'

        elif command == 'EXIT':
            print ('Client has left')
            killswitch = 0
            break
        elif command =='KILL':
            print ('Server is kill')
            killswitch = 1
            s.close
            break
        elif command =='SYS':
            print ('SYS_MESSAGE')
            os.system(dataMessage[1])
            reply = 'Executed'
        elif command =='This is Bowie to Bowie, do you read me out there man?':
            reply = 'This is Bowie back to Bowie, I read you loud and clear man!'
        else:
            reply = 'Unknown Command'

        #Save openTrigSwitch status
#        fh1 = open('status2.txt', 'w')
#        if openTrigSwitch == '0':
#            fh1.write('0')
#        elif openTrigSwitch == '1':
#            fh1.write('1')
#        fh1.close()

        #send reply back to client
        conn.sendall(str.encode(reply))
        print ('Data has been sent')

        tf = open('status2.txt', 'w')
        tf.write(openTrigSwitch)
        tf.close()
    conn.close()


s = setupServer()
while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        global killswitch
        if killswitch == 1:
            break
        else:
            s.close
    if killswitch == 1:
        break





