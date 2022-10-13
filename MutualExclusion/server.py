from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import sys
import multiprocessing
import time
import queue

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass    

class CriticalResourceServer:
    def __init__(self) -> None:
        self.mutex = multiprocessing.Lock()
        self.process_queue = queue.Queue()
    def backup_data(self, pid):
        self.process_queue.put(pid)
        print(f"Added {pid} in the queue")
        self.access_critical_resources(pid)
    def access_critical_resources(self, pid):
        self.mutex.acquire()
        print(f"Process {pid} is inside the Critical Section and has started backing it's Data !" )
        print(list(self.process_queue.queue))
        time.sleep(5)
        self.process_queue.get()
        print(f"Backup Complete for process {pid}!")
        print(f"Process {pid} exited the Critical Section!")
        self.mutex.release()

PORT = 8000
server_addr = ("localhost", PORT)
server = SimpleThreadedXMLRPCServer(server_addr)
server.register_instance(CriticalResourceServer())
try:
    print("Critical Server has Started")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)

