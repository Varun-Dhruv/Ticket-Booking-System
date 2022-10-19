from pydoc import cli
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import string
import string
from datetime import datetime
from prettytable import PrettyTable
import threading
os.system('color')
from termcolor import colored
import asyncio

mutex=threading.Lock()
rate=0.5
clock=0
queue=[]
queue_mutex=threading.Lock()
clientList=[]
clientId=0
client_mutex=threading.Lock()
criticak_mutex=threading.Lock()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t=threading.Thread(target=func_wrapper)
    t.start()
    return t

def serverSynchronize():
    global clock
    mutex.acquire()
    clock+=1
    mutex.release()

def getServerClock():
    return clock

def setServerClock(client_clock):
    global clock
    print(colored(f"\n[INFO] Before server receives messafe: Server Logical Clock={clock}\n",'yellow'))
    if(client_clock>clock):
        mutex.acquire()
        clock=client_clock+1
        mutex.release()
    print(colored(f"\n[INFO] After server receives messafe: Server Logical Clock={clock}\n",'yellow'))

def requestCS(client_clock,clientID):
    global clock,criticak_mutex,queue
    
    print(colored(f"\n[INFO] Before server receives messafe: Server Logical Clock={clock}\n",'yellow'))
    if criticak_mutex.locked():
        if clientID not in queue:
            queue_mutex.acquire()
            print(colored(f"Queue mutex Acquird ny {clientID}",'green'))
            queue.append(clientID)
            queue_mutex.release()
            print(colored(f"Queue mutex released ny {clientID}",'green'))
            return False
        else:
            criticak_mutex.acquire()
            print(colored(f"Critical Mutex acquired ny {clientID}",'red'))
            if client_clock> clock:
                mutex.acquire()
                clock=client_clock+1
                mutex.release()
