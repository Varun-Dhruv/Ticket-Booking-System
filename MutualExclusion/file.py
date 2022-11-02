fileread = open("myfile.txt", "r")
#filewrite = open("myfile.txt", "w")
# file read
num = int(fileread.read(1))
print(num)
if num == 0:
    print('No more seats avaible please try another time')
else:
    num =num-1
    print(f'one ticket booked: tickets available are: {num}')
    filewrite = open("myfile.txt", "w")
    filewrite.write(str(num))
                # write file
