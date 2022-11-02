from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import string
import random
from datetime import datetime
from prettytable import PrettyTable
import threading
os.system('color')
from termcolor import colored
import asyncio

mutex = threading.Lock()
rate = 0.5
clock = 0 # Default rate 4 sec
queue = [] # Waitlist of clientId requesting CS
queue_mutex = threading.Lock()
clientList = [] # List of clientIds
clientId = 0
client_mutex = threading.Lock()
critical_mutex = threading.Lock()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def serverSynchronize():
    global clock
    mutex.acquire() # Keep increasing at "rate", keeping in mind race around condition
    clock += 1
    mutex.release()

# print(colored(f"\n[INFO] Server Logical Clock(Updated atinterval set): {clock}\n", 'yellow'))
# Lamport's Algorithm
def getServerClock(): # Server sends message to client
    return clock

def setServerClock(client_clock): # Server receives message from client
    global clock
    print(colored(f"\n[INFO] Before server receives message: Server Logical Clock = {clock}\n", 'yellow'))
    if client_clock > clock:
        mutex.acquire()
        clock = client_clock + 1  #Send clock + 1 by default from client side
        mutex.release()
    print(colored(f"\n[INFO] After server receives message: Server Logical Clock = {clock}\n", 'yellow'))


# Mutual Exclusion using Centralized Algorithm
def requestCS(client_clock, clientID): # Server receives message from client
    global clock,critical_mutex,queue
    print(colored(f"\n[INFO] Before server receives message: Server Logical Clock = {clock}\n", 'yellow'))
    if critical_mutex.locked():
        if clientID not in queue:  # If not already in queue, add the client in queue
            queue_mutex.acquire()
            print(colored(f"Queue Mutex Acquired by {clientID}; queue:{queue}","green"))
            queue.append(clientID)  # Append to the queue
            queue_mutex.release()
            print(colored(f"Queue released by {clientID}; queue:{queue}","green"))
        return False
    else:
        critical_mutex.acquire()
        print(colored(f"\nCritical Mutex Acquired by {clientID}","red"))
        if client_clock > clock:
            mutex.acquire()
            clock = client_clock + 1 # Send clock + 1 by default from client side
            mutex.release()
        print(colored(f"\n[INFO] After server receives message: Server Logical Clock = {clock}\n", 'yellow'))

        if clientID in queue:
            print(colored(f"Queue Mutex Acquired by {clientID}; queue:{queue}","green"))
            queue_mutex.acquire()
            try:
                queue.remove(clientID) # Remove
            except:
                pass
            queue_mutex.release()
            print(colored(f"Queue released by {clientID}; queue:{queue}","green"))
        return True

def releaseCS(client_clock, clientID): # Server receives message from client
    global clock,critical_mutex
    print(colored(f"\n[INFO] Before server receives message: Server Logical Clock = {clock}\n", 'yellow'))
    if client_clock > clock:
        mutex.acquire()
        clock = client_clock + 1 # Send clock + 1 by default from client side
        mutex.release()
    print(colored(f"\n[INFO] After server receives message: Server Logical Clock = {clock}\n", 'yellow'))
    critical_mutex.release()
    print(colored(f"\nCritical Mutex Released by {clientID}","red"))
    return clock

# Model classes
class User():
  def	__init__(self, username):
    self.username = username	# User Identification information
    self.history = []	# Contain the list of Phones, along with booked status
    self.curr_Phone = None	# Contains the active Phones if any

  def	__str__(self):
    return f"['username': {self.username}, 'history': {self.history}, 'curr_Phone': {self.curr_Phone}]"

  def addToSeen(self, f):
    self.history.append({"Phone": f.Phone_number, "status": "seen"})
    self.curr_Phone = f

  def bookPhone(self, Phone_class):
    self.history[-1]["status"] = "booked"
    self.curr_Phone.fillASeat(Phone_class)
    
class Phone():
    def	__init__(self, Phone_number, Manufactured, Reseller, Listed_On, total_stock, Brand_New, Refurbished_price,New_Price, Brand):
        self.Phone_number = Phone_number 
        self.Manufactured = Manufactured
        self.Reseller = Reseller
        self.Listed_On = Listed_On 
        self.total_stock = total_stock
        self.Brand_New = Brand_New 
        self.Refurbished = self.total_stock - self.Brand_New
        self.available_seats = total_stock 
        self.Refurbished_price = Refurbished_price
        self.New_Price = New_Price 
        self.Brand = Brand

    def fillASeat(self, Phone_class): 
        if Phone_class == "N":
            self.Brand_New -= 1 
        else:
            self.Refurbished -= 1
            self.available_seats = self.Brand_New + self.Refurbished

    def	__str__	(self):
        return f"['Phone_number': {self.Phone_number}, 'Manufactured': {self.Manufactured}, 'Reseller': {self.Reseller}, 'Listed_On': {self.Listed_On}, 'total_stock': {self.total_stock}, 'Brand_New': {self.Brand_New}, 'Refurbished_price': {self.Refurbished_price}, 'New_Price': {self.New_Price}, 'Brand': {Brand}]"

# Static Data

Brands = [
  {
  "name": "Iphone",
  "cost_b": random.randint(100000, 200000),
  "cost_e": random.randint(10000, 20000)
  },
  {
  "name": "Samsung",
  "cost_b": random.randint(100000, 200000),
  "cost_e": random.randint(10000, 20000)
  },
  {
  "name": "One Plus",
  "cost_b": random.randint(100000, 200000),
  "cost_e": random.randint(10000, 20000)
  },
  {
  "name": "Vivo",
  "cost_b": random.randint(100000, 200000),
  "cost_e": random.randint(10000, 20000)
  }
]

Countries = ['India', 'Japan', 'China', 'California', 'Canada','Malaysia']	
times = [	
  datetime.strptime('13  Sep	2022',	'%d	%b	%Y').replace(hour=9,minute=00),					
  datetime.strptime('13  Sep	2022',	'%d	%b	%Y').replace(hour=12,minute=00),					
  datetime.strptime('13  Sep	2022',	'%d	%b	%Y').replace(hour=15,minute=00),					
  datetime.strptime('13  Sep	2022',	'%d	%b	%Y').replace(hour=18,minute=00),					
  datetime.strptime('13  Sep	2022',	'%d	%b	%Y').replace(hour=21,minute=00),					
]					

Phones = []	# list of randomly generated Phones
user = User("admin")	# default user

for i in range(6):
  c = random.sample(Countries, 2)

  Brand = random.choice(Brands) 
  Phones.append(
    Phone(
      Phone_number=''.join(random.choices(
      string.ascii_letters, k=3)), Manufactured=c[0],
      Reseller=c[1],
      Listed_On=random.choice(times), total_stock=random.randint(200, 300),
      Brand_New=random.randint(150, 200), Refurbished_price=Brand['cost_e'],
      New_Price=Brand['cost_b'], Brand=Brand['name']
    )
  )

server = SimpleXMLRPCServer(('localhost', 3069), allow_none=True)

# Custom Server-side functions

def get_Phones():	# Returns list of Phone objects to the client terminal using pretty table
  return Phones

def view_Phones():	# Display Phones in tabular format
  table = PrettyTable( [
          'Phone_number', 'Manufactured', 'Reseller', 'Listed_On', 'available_seats',
          'Brand_New', 'Refurbished', 'Refurbished_price', 'New_Price', 'Brand'
          ])
  table.title = 'Phones'

  for i in range(len(Phones)):	# Storing the output tuples in table
    f = Phones[i] 
    table.add_row(
      [
        f.Phone_number, f.Manufactured, f.Reseller, f.Listed_On, f.available_seats,
        f.Brand_New,
        f.Refurbished, f.Refurbished_price, f.New_Price, f.Brand
      ]
    )
  return table.get_string()


def bookPhone(id, Phone_class): 
  for f in Phones:
    if f.Phone_number == id: 
      user.addToSeen(f)
      break

  if Phone_class == "B":
    return user.curr_Phone.New_Price 
  else:
    return user.curr_Phone.Refurbished_price


def pay(Phone_class):
  user.bookPhone(Phone_class)

def getId():
    global clientList, clientId
    print(colored(f'Client List acquired : {clientList}','red'))
    client_mutex.acquire()
    clientId = 0 if len(clientList) == 0 else (max(clientList) + 1)
    clientList.append(clientId)
    client_mutex.release()
    print(colored(f'Client List released : {clientList}','red'))
    return clientId

def removeId(clientId):
    global clientList
    client_mutex.acquire()
    clientList.remove(clientId)
    client_mutex.release()

server.register_function(setServerClock)
server.register_function(getServerClock)
server.register_function(get_Phones)
server.register_function(pay)
server.register_function(bookPhone)
server.register_function(view_Phones)
server.register_function(requestCS)
server.register_function(getId)
server.register_function(removeId)
server.register_function(releaseCS)

if __name__ == '__main__':
    try:
        print('Serving...')
        set_interval(serverSynchronize, rate)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')