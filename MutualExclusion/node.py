from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from threading import Timer
from time import time, sleep
import argparse
import sys
NETWORK = {
    "node_1": ("127.0.0.1", 5000),
    "node_2": ("127.0.0.1", 6000),
    "node_3": ("127.0.0.1", 7000),
    "node_4": ("127.0.0.1", 8000),
}
CRS = ("127.0.0.1", 4000)
# fileread = open("myfile.txt", "r")
# filewrite = open("myfile.txt", "w")


class RPCServer:
    def __init__(self, pid, pid_node_mapping, CRS, exetute_after=None):
        self.pid = pid
        self.pid_node_mapping = pid_node_mapping
        self.CRS = CRS
        self.request_queue = []
        self.reply_set = set()
        self.execute_at = None
        self.task_done = True
        if exetute_after:
            self.execute_at = time() + exetute_after
            self.timer = Timer(exetute_after, self.execute)
            self.timer.start()
            self.task_done = False

    def request(self, timestamp: float, remote_node_pid: str):
        """
        RPC method to request access for shared resource
        accross the resource
        Params:
        timestamp: seconds passed since an epoch
        pid: process id which requested access
        """
        print(
            f"[{round(time() * 1000)}] REQUEST --> {remote_node_pid}({round(timestamp*1000)})")

        if self.task_done or timestamp < self.execute_at:
            node = self.pid_node_mapping[remote_node_pid]
            sleep(1)
            node.reply(self.pid)
            return
        self.request_queue.append(remote_node_pid)

    def reply(self, rpid):
        self.reply_set.add(rpid)
        print(f"[{round(time() * 1000)}] REPLY --> {rpid}")
        if self.execute_at:
            if set(self.pid_node_mapping.keys()) == self.reply_set:
                self.execute(after_replay=True)

    def execute(self, after_replay=False):
       
        if not after_replay:
            for rpid, node in self.pid_node_mapping.items():
                if rpid == self.pid:
                    continue
                try:
                    timestamp = time()
                
                    node.request(timestamp, self.pid)
                    fileread = open("myfile.txt", "r")
                    #filewrite = open("myfile.txt", "w")
                    # file read
                    num = int(fileread.read(1))
                    print(num)
                    if num == 0:
                        print('No more seats avaible please try another time')
                    else:
                        num = num-1
                        print(f'one ticket booked: tickets available are: {num}')
                        fileread.close()
                        filewrite = open("myfile.txt", "w")
                        filewrite.write(str(num))
                        filewrite.close()
                except Exception as e:
                     print('')     # write file


        if set(self.pid_node_mapping.keys()) == self.reply_set:
            self.CRS.execute_task_in_critical(self.pid)
            self.task_done = True
            print(f"[{round(time()*1000)}] Critical Section Resource Released\n\n")

            for rpid in self.request_queue:
                self.pid_node_mapping[rpid].reply(self.pid)
            self.reply_set = set()


if __name__ == "__main__":
    try: 
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "pid", type=str, help="Enter pid (node_1, node_2, node_3,node_4)")
        parser.add_argument("--time_offset", type=int, default=None,
                            help="time in seconds after which task starts to execute",)
        args = parser.parse_args()
        PID = args.pid
        TIME_OFFSET = args.time_offset
        server = SimpleXMLRPCServer(
            NETWORK[PID], allow_none=True, logRequests=False)
        pid_mapping = dict()
        for pid, addr in NETWORK.items():
            if pid == PID:
                continue
            pid_mapping[pid] = ServerProxy(f"http://{addr[0]}:{addr[1]}")
        crs_proxy = ServerProxy(f"http://{CRS[0]}:{CRS[1]}")
        server.register_instance(
            RPCServer(PID, pid_mapping, crs_proxy, TIME_OFFSET))
        try:
            print("Starting RPC Server...")
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
    except Exception as e:
        print('')