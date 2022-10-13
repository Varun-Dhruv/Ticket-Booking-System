from xmlrpc.server import SimpleXMLRPCServer
import string
import random
import slaveclient
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
sc = slaveclient.initiateSlaveClient(port=8080)
server.register_function(getFilmInfo, "getFilmsInfo")
server.register_function(view_Films, "view_Films")
server.register_function(book_seat, "book_seat")
try:
    print("Starting and listening on port 8000...")
    print("Press Ctrl + C to exit.")
    server.serve_forever()
    sc.close()

except:
    print("Exit.")
