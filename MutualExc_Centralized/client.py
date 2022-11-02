from termcolor import colored
from xmlrpc.client import ServerProxy
from prettytable import PrettyTable
import threading
import os
import sys
os.system('color')
import asyncio
import time
import atexit
clientID = 0
proxy = ServerProxy('http://localhost:3069')

mutex = threading.Lock()
rate = 1
clock = 0 # Default rate 7 sec

def exit_handler():
    proxy.removeId(clientID)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def clientSynchronize():
    global clock
    mutex.acquire() # Keep increasing at "rate", keeping in mind race around condition
    clock += 1
    mutex.release()
    # print(colored(
    # f"\n[INFO] Client Logical Clock(Updated at interval set):{clock}\n", 'yellow'))
    # Lamport's Algorithm

def setClientClock(server_clock): # Client receives message from server
    global clock
    print(colored(f"\n[INFO] Before client receives message: Client Logical Clock = {clock}\n", 'yellow'))
    if server_clock > clock:
        mutex.acquire()
        clock = server_clock + 1 # Send clock + 1 by default from client side
        mutex.release()
    print(colored(f"\n[INFO] After client receives message: Client Logical Clock = {clock}\n", 'yellow'))

def synchronize(func, *args): # Synchronizes server and client clocks before an event
    proxy.setServerClock(clock) # Synchronise with server
    if args:
        result = func(*args)
    else:
        result = func() # Critical section
    # Update the client clock after the function call
    setClientClock(proxy.getServerClock())
    return result

def synchronizeCS(func, *args): # Synchronizes server and client clocks before an event
    reply = False # Synchronise with server, requestServer() => send clock and request CS
    while not reply:
        reply = proxy.requestCS(clock, clientID)
    if args:
        result = func(*args)
    else:
        result = func() # Critical section
    # Update the client clock after the function call
    setClientClock(proxy.releaseCS(clock, clientID))
    return result

if __name__ == '__main__':
    clientID = proxy.getId() # call the clientID function here => assign_ID and store in server as well as in client
    t = set_interval(clientSynchronize, rate)
    # atexit.register(exit_handler)
    while True:
        print('\nLoading Mobile Information...')

        Phones = synchronize(proxy.get_Phones) # Synchronize
        print("Welcome To Phone Buying Portal\nPress 1. To View Phones \nPress 2. To Book a Phone \nPress 3. To Exit")
        print("Enter your choice: ", end='')
        choice = int(input())
        if choice == 1:
            print(synchronize(proxy.view_Phones)) # Synchronize
        elif choice == 2:
            id = input('Enter Phone ID to book your Phone:').strip()
            Phone_class = input('Choose Phone Condition (N-New, R-Refurbished):').strip().upper()
            cost = synchronizeCS(proxy.bookPhone, id, Phone_class) # Synchronize
            if cost == -1:
                print("Invalid Phone ID entered ")
                continue
            if input(f"Cost of Phone - Rs. {cost}\n Pay to book? [Y/N]: ").upper()[0] == 'Y':
                result = synchronizeCS(proxy.pay, Phone_class) #Synchronize pay()

                if result:
                    print("Your Phone has been booked")
                else:
                    print("No Available Stock. Please book another Phone.")
            else:
                print("You have cancelled your booking :(")

        elif choice == 3:
            print('Thank you for using this app :)')
            proxy.removeId(clientID) # call another function in server to close the assignedID
            t.cancel()
            break
        else:
            print("You have entered a wrong choice.")