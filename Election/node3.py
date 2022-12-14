import socket
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
to_port = 7777
s.connect((host, to_port))
cur_process_id = "3"
s.send(cur_process_id.encode('utf-8'))
leader="-1"

def initiate_election(s):
    time.sleep(1)
    s.send(cur_process_id.encode('utf-8'))
    print("token sent: " + cur_process_id)
    print("Election initiated")

def Ring_Election_Algorithm(s):

    while True:
        global leader
        try:
            s.settimeout(15)
            received = s.recv(1024)
            s.settimeout(None)
            received_token_list = received.decode('utf-8')
        #here the timeout exceptiion catches and iniate election
        except socket.timeout:
            leader = "0"
            initiate_election(s)
            continue

        print("token list is: "+received_token_list)
        if cur_process_id in received_token_list and "Coordinator: " not in received_token_list and "id_rec" not in received_token_list:
            leader = max(received_token_list)
            forwarding_leader = "Coordinator: " + leader
            time.sleep(1)
            s.send(forwarding_leader.encode('utf-8'))

        elif cur_process_id not in received_token_list and "Coordinator: " not in received_token_list and "id_rec" not in received_token_list :

            print("rec tok: " + received_token_list)
            leader = "0"
            received_token_list = received_token_list + " " + cur_process_id
            time.sleep(1)
            s.send(received_token_list.encode('utf-8'))
            print("adding token: " + received_token_list)

        elif ("id_rec" in received_token_list or "Coordinator: " in received_token_list )and leader=="-1"  :
                leader="0"
                initiate_election(s)

        elif "Coordinator: " in received_token_list and leader not in received_token_list :
            print(received_token_list)
            le=received_token_list.split()
            leader=le[1]
            time.sleep(1)
            s.send(received_token_list.encode('utf-8'))

        else :
            if leader=="-1" or leader=="0":
                continue
            else :
                #print("coordinator mm :" + leader)
                print(received_token_list)
                communicate = "id_rec" + cur_process_id
                time.sleep(1)
                s.send(communicate.encode('utf-8'))
                continue

recv_thread = threading.Thread(target=Ring_Election_Algorithm, args=(s,))
recv_thread.start()
recv_thread.join()
s.close()