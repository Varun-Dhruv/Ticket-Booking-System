# Python3 program imitating a client process

from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket
import time


# client thread function used to send time at client side
def startSendingTime(slave_client):

    while True:
        # provide server with clock time at the client
        if slave_client._closed:
            break
        try:
            slave_client.send(str(datetime.datetime.now()).encode())
            print("Recent time sent successfully",end="\n\n")
            time.sleep(25)
        except:
            break


# client thread function used to receive synchronized time
def startReceivingTime(slave_client):

    while True:
        if slave_client._closed:
            break
        # receive data from the server
        try:
            Synchronized_time = parser.parse(slave_client.recv(1024).decode())
            print("Synchronized time at the client is: " + str(Synchronized_time), end="\n\n")
        except:
            break


# function used to Synchronize client process time
def initiateSlaveClient(port=8080):

    slave_client = socket.socket()

    # connect to the clock server on local computer
    slave_client.connect(('127.0.0.1', port))

    # start sending time to server
    print("Starting to receive time from server\n")
    send_time_thread = threading.Thread(
        target=startSendingTime,
        args=(slave_client, ))
    send_time_thread.start()

    # start receiving synchronized from server
    print("Starting to receiving " +
          "synchronized time from server\n")
    receive_time_thread = threading.Thread(
        target=startReceivingTime,
        args=(slave_client, ))
    receive_time_thread.start()
    return slave_client



