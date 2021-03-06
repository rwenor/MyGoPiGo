import socket
import sys
import time
import os
import threading
import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

def PTD(str):
    global PrintTimeDiffLast
    global PrintTimeCnt
    print 'PTD%4s: %6s - %s' %  (PrintTimeCnt, \
                               int((time.time() - PrintTimeDiffLast)*1000), \
                               str) 
    PrintTimeCnt += 1
    PrintTimeDiffLast = time.time()


def sm_add(fra, til, data):
    try:
        d = data.strip().split(' ')

        data = 0
        for val in d:
            data += float(val)
        data = str(data)

    except:
        data = 'ERR'

    return data

    
def sm_getCpuTemp(fra, til, data):
    try:
        res = os.popen('vcgencmd measure_temp').readline()
        data = res.replace("temp=","").replace("'C\n","")
            
    except:
        data = 'ERR'

    return data

sms_data = []

def Disp_sm(fra, til, data):

    sms_data.append(data)
    if til == 'Til.Add':
        data = sm_add(fra, til, data)
    elif til == 'Til.CpuTemp':
        data = sm_getCpuTemp(fra, til, data)
    else:
        data = 'ERR'

    return data
    
#Globals
connection = None
client_address = ''
sock = None
halt = False

def Init_srv():
    global sock
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    #server_address = ('10.0.0.130', 10000)
    server_address = ('', 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)


    
def Recv_sms():
    global connection
    global client_address
    global sock
    
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while not halt:
            data = connection.recv(200)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                l = data.strip().split('\t')
                if len(l) < 3:
                    print "Err: ", l
                    l[2] = 'NAK'
                else:
                    l[2] = Disp_sm(l[0], l[1], l[2])

                #print >>sys.stderr, 'sending data back to the client'
                data = l[1] + '\t' + l[0] + '\t' + l[2]
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()


def Run_sms_srv():
    Init_srv()
    Recv_sms()


def Run_test():
    global halt
    
    i = 0
    while not halt:
        i += 1
        logging.debug( str(i) + ': ' + str(sms_data) )
        time.sleep(1)
        if i == 10:
            sms_data.append('Fire')
        elif i == 100:
            halt = True
            sock.close()


def Chk_Fire():
    global sms_data

    if sms_data:
        sms_data = []
        return True
    else:
        return False
    


threads = []

t = threading.Thread(target=Run_sms_srv)
threads.append(t)
t.start()

t = threading.Thread(target=Run_test)
threads.append(t)
t.start()

