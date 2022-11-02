import random
import sys
import threading
from collections import deque
from datetime import datetime
from threading import Thread
from time import sleep
from mpi4py import MPI
comm = MPI.COMM_WORLD
tid = comm.Get_rank()
N = comm.Get_size()
cs_lock = threading.Lock()
token_lock = threading.Lock()
rn_lock = threading.Lock()
release_lock = threading.Lock()
request_lock = threading.Lock()
send_lock = threading.Lock()
Q = deque()

has_token = 0
in_cs = 0
waiting_for_token = 0
RN = []
LN = []
for i in range(0, N):
    LN.append(0)
    RN.append(0)
# giving a token to start the process
if tid == 0:
    print("%s: %d I have a startup token." %
      (datetime.now().strftime('%M:%S'), tid))
    sys.stdout.flush()
    has_token = 1
RN[0] = 1


def receive_request():
    global LN
    global RN
    global Q
    global in_cs
    global waiting_for_token
    global has_token
    while True:
        message = comm.recv(source=MPI.ANY_SOURCE)
        if message[0] == 'RN':
            with rn_lock:
                requester_id = message[1]
                cs_value = message[2]
                RN[requester_id] = max([cs_value, RN[requester_id]])
                if cs_value < RN[requester_id]:
                    print("%s: Request from %d has expired." % (datetime.now().strftime('%M:%S'), requester_id))

                    sys.stdout.flush()

                if (has_token == 1) and (in_cs == 0) and (RN[requester_id]== (LN[requester_id] + 1)):
                    has_token = 0
                    send_token(requester_id)

        elif message[0] == 'token':
            with token_lock:
                print("%s: %d I received a token." % (datetime.now().strftime('%M:%S'), tid))
                sys.stdout.flush()
                has_token = 1
                waiting_for_token = 0
                LN = message[1]
                Q = message[2]
                critical_section()


def send_request(message):
    for i in range(N):
        if tid != i:
            to_send = ['RN', tid, message]
            comm.send(to_send, dest=i)


def send_token(recipient):
    global Q
    with send_lock:
        print("%s: I am %d and sending token to %d." % (datetime.now().strftime('%M:%S'), tid, recipient))
        sys.stdout.flush()
        global in_cs
        to_send = ['token', LN, Q]
        comm.send(to_send, dest=recipient)


def request_cs():
    global RN
    global in_cs
    global waiting_for_token
    global has_token

    with request_lock:
        if has_token == 0:
            RN[tid] += 1
            print("%s: I am %d and I want a token once more %d." %

                (datetime.now().strftime('%M:%S'), tid, RN[tid]))

            sys.stdout.flush()
            waiting_for_token = 1
            send_request(RN[tid])


def release_cs():


    global in_cs
    global LN
    global RN
    global Q
    global has_token
    with release_lock:
        LN[tid] = RN[tid]
        for k in range(N):
            if k not in Q:
                if RN[k] == (LN[k] + 1):
                    Q.append(k)
                    print("% s: I am % d and adding % d to the queue. Queue after adding: % s." % ( datetime.now().strftime('%M:%S'), tid, k, str(Q)))
        sys.stdout.flush()

        if len(Q) != 0:
            has_token = 0
            send_token(Q.popleft())


def critical_section():
    global in_cs
    global has_token
    with cs_lock:
        if has_token == 1:
            in_cs = 1
            print("%s: I am %d and performs %d Critical Section." %

                (datetime.now().strftime('%M:%S'), tid, RN[tid]))

            sys.stdout.flush()

            sleep(random.uniform(2, 5))
            print("%s: I am %d and finished doing %d Critical Section." %

                (datetime.now().strftime('%M:%S'), tid, RN[tid]))

            sys.stdout.flush()
            in_cs = 0
            release_cs()

    try:
        thread_receiver = Thread(target=receive_request)
        thread_receiver.start()
    except:
        print("Error: unable to start thread! ")
        sys.stdout.flush()
    while True:
        if has_token == 0:
            sleep(random.uniform(1, 3))
            request_cs()
        elif in_cs == 0:
            critical_section()
        while waiting_for_token:
            sleep(0.5)


def lock_unlock_file(client_socket, client_id, filename, lock_or_unlock):


    serverName = 'localhost'
    serverPort = 4040  # port of directory service
    client_socket.connect((serverName, serverPort))
    if lock_or_unlock == "lock":
        msg = client_id + "_1_:" + filename  # 1 = lock the file
    elif lock_or_unlock == "unlock":
        msg = client_id + "_2_:" + filename  # 2 = unlock the file
    # send the string requesting file info to directory service
    client_socket.send(msg.encode())
    reply = client_socket.recv(1024)

    reply = reply.decode()
    return reply


def cache(filename_DS, write_client_input, RW, client_id):

    # append the cache folder and filename to the path
    cache_file = curr_path + "\\client_cache" + client_id + "\\" + filename_DS
    # create the directory/file
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    if RW == "a+" or RW == "w":
        # write to the cached file
        with open(cache_file, RW) as f:
            f.write(write_client_input)

    else:
        with open(cache_file, "r") as f:
            print_breaker()
            print(f.read())
            print_breaker()
