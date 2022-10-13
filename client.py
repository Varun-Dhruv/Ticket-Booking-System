import slaveclient
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
if __name__ == '__main__':
   # sc = slaveclient.initiateSlaveClient(port=8080)
    while True:

        print(
            '''
1. Films in theater 
2. Get Film Location By Time
3. Exit
4. Book a seat
'''
        )
        print("Enter your choice: ", end='')
        choice = int(input())
        if choice == 1:
            Films = (proxy.view_Films())
            for Film in Films:
                for Film_id in Film:
                    print("{:<15}".format(Film_id), end="\t")
                print("\n")
        elif choice == 2:
            name = input('Enter Film ID to rent your Film:').strip()
            timings = input('Enter the time of Film').strip()
            Filmlist = (proxy.getFilmsInfo(timings, name))
            if (len(Filmlist) == 0):
                print("No Films available at this time")
                continue
            print("The Film is available in: ")
            for Film in Filmlist:
                print(Film)
        elif choice == 3:
            print('Thank you! Visit us again!')
            break
        elif choice == 4:
            name = input('Enter Film ID to rent your Film:').strip()
            proxy.book_seat(name)
        else:
            print("Wrong choice! Enter correct choice")
