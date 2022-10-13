def process_Pool(id, message_case=0):
    nodes_list = [1, 2, 3, 4, 5] 
    if message_case == 1: 
        new_list = []
        for x in nodes_list:
            if id < x:
                new_list.append(x)  
        if id == len(nodes_list):  
            return None  

        return new_list
    if message_case == 2 and id is not 1: 
        return [nodes_list[int(id)-2]]
    
    if message_case == 3: 
        del nodes_list[len(nodes_list)-1]
        return nodes_list 


def sending_data(recepients, message):  

    if recepients is not None: 
        for node in recepients:
            print(message+" sent to Node"+str(node))


def node(myId):
    sending_list = process_Pool(myId, 1)
    if sending_list is None: 
        sending_data(process_Pool(myId, 3), "I've won")
    else:
        sending_data(sending_list, "Election")
    sending_data(process_Pool(myId, 2), "OK")

node(1)
node(2)
node(3)
node(4)
node(5)
