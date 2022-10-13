import sys
from xmlrpc.server import SimpleXMLRPCServer
import argparse
from time import time

class CRS:
    def execute_task_in_critical(self, rpid):
        print(f"[{round(time() * 1000)}] --> Backup Done By {rpid}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, help="Enter IP Address of Server",default="127.0.0.1")
    parser.add_argument("port", type=int, help="Enter Port Number")
    args = parser.parse_args()
    HOST = args.ip
    PORT = args.port
    # create a RPC server running on a node
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True, logRequests=False)
    server.register_instance(CRS())
    try:
        print("Starting RPC Server...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)