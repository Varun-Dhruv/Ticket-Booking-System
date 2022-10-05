import socket
import threading
import time
import select

from xmlrpc.server import SimpleXMLRPCServer
import string
import random

FilmInfo = [
    {
        "name": "F&F",
        "time": "3",
        "location": "Malad"
    }, {
        "name": "Race",
        "time": "6",
        "location": "Malad"
    }, {
        "name": "Inception",
        "time": "9",
        "location": "Malad"
    }
]


def getFilmInfo(time, name):
    Filmlist = []
    for inforFilm in FilmInfo:
        if inforFilm["name"] == name and inforFilm["time"] == time:
            Filmlist.append(inforFilm['location'])
    return Filmlist


class Film:
    def __init__(self, Film_id, Film_name, available_seats, genre):
        self.Film_id = Film_id
        self.Film_name = Film_name
        self.available_seats = available_seats
        self.genre = genre

    def reduceAMovieCopy(self):
        if self.available_seats != 0:
            self.available_seats -= 1
        else:
            self.available_seats = -1


# Data
Films_list = [
    {
        'name': 'Fast and Furious',
        'genre': 'Thriller'
    },
    {
        'name': 'Hulk',
        'genre': 'Fiction'
    },
    {
        'name': 'Avengers: End Game',
        'genre': 'Fantasy'
    },
    {
        'name': 'Lord of the Rings',
        'genre': 'Adventure'
    },
    {
        'name': 'Brahmastra',
        'genre': 'Bollywood'
    },
    {
        'name': "The Ring",
        'genre': 'Horror'
    }
]


Films = []
for film in Films_list:
    Films.append(
        Film(
            Film_id=''.join(random.choices(string.digits, k=6)), Film_name=film["name"],
            available_seats=100,
            genre=film["genre"]
        )
    )


def view_Films():
    table = [
        ["Film ID", "Genre", "Seats", "Film Name"]]
    # table.title = 'Films'
    for Film in Films:
        table.append(
            [
                Film.Film_id, Film.genre, Film.available_seats, Film.Film_name,

            ]
        )
    return table


def book_seat(name):
    for film in Films:
        if (film.Film_name == name):
            film.reduceAMovieCopy()
            break
    print("out")
    return True

server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True)
server.register_function(getFilmInfo, "getFilmsInfo")
server.register_function(view_Films, "view_Films")
server.register_function(book_seat, "book_seat")
try:
    print("Starting and listening on port 8000...")
    print("Press Ctrl + C to exit.")
except:
    print("Exit.")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
to_port = 7777
s.connect((host, to_port))
cur_process_id = "1"
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