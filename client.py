import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/") 
print(proxy.getMoviesInfo("3","F&F"))


