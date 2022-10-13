from xmlrpc.client import ServerProxy
import multiprocessing


def make_request(pid):
    critical_server = ServerProxy("http://127.0.0.1:8000")
    print("Making Request to the CriticalResourceServer")
    critical_server.backup_data(pid)
    print("Process Completed")


if __name__ == "__main__":
    no_of_processes = 4
    with multiprocessing.Pool(processes=no_of_processes) as pool:
        try:
            pool.map(make_request, range(1, no_of_processes + 1))
        except TypeError as err:
            print(1)
