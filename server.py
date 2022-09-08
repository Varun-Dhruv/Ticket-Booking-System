from xmlrpc.server import SimpleXMLRPCServer

movieInfo = {
  "Malad" : {
    "name" : "F&F",
    "time" : "3",
    "location":"Malad"
  },
  "Andheri" : {
    "name" : "Race",
    "time" : "6",
    "location":"Malad"
  },
  "Sion" : {
    "name" : "Inception",
    "time" : "9",
    "location":"Malad"
  }
}

def getMovieInfo(time,name):
    # for x in movieInfo: 
    #     print(x)
    x = movieInfo.values()
    for inforMovie in x: 
        if inforMovie["name"] == name and inforMovie["time"] == time:
          print(inforMovie)
          return inforMovie
    return "No Movie Available"

server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True)
server.register_function(getMovieInfo, "getMoviesInfo")

try:
    print("Starting and listening on port 8000...")
    print("Press Ctrl + C to exit.")
    server.serve_forever()

except:
    print("Exit.")

