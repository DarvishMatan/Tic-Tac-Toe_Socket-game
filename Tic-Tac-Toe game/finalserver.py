import socket
import select

"""finals"""
IP = "127.0.0.1"
PORT = 9010

"""global variables"""
message_to_send = []
open_client_sockets = []
players = []  # Make players matrix


"""update the players array index 0 vs index 1"""


def updateP(p1, p2):
    global players
    players.append([p1, p2])


"""send messages for the waiting clients except the sender client with the indexes of the pressed cube"""


def send_waiting_messages():
    global players
    for message in message_to_send:
        (client_socket, data) = message
        for couple in players:
            if client_socket in couple:
                if client_socket is not couple[0]:  # send to the rival
                    couple[0].send(data)
                elif client_socket is not couple[1]:  # send to the rival
                    couple[1].send(data)
                message_to_send.remove(message)


"""if there are 2 or more start the game by splitting each 2 into a game"""


def startinclient():
    global players
    print "send 1"
    for couple in players:
        for s in couple:
            s.send("1")  # q for start


"""if endgame q is recieved, rempove the sockets connections of the players"""


def endgame(s):
    global players
    for couple in players:
        if s in couple:
            players.remove(couple)
            print players


def main():
    global players  # players array, 2-d array. 2*n couples length
    global rlist
    print "Server is running"
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])#always on, open new connections
        if len(wlist) - len(players)*2 == 2:  # if 2 new players added
            new1 = wlist[len(wlist)-2]
            new2 = wlist[len(wlist)-1]
            updateP(new1, new2)  # add 2 players 1 vs the other to the players database
            startinclient()  # send the q for start to the client
        """TODO add a case which a player is leaving"""
        if len(rlist) > 0:
            for current_socket in rlist:  # get all over the input messages
                if current_socket is server_socket:  # append to  sockets
                    (new_socket, address) = server_socket.accept()
                    open_client_sockets.append(new_socket)
                else:  # get the data
                    row = current_socket.recv(1)
                    if row == "":
                        open_client_sockets.remove(current_socket)
                        print 'Connection with client was closed.'
                    elif row == "5":  # q for winner by leave
                        message_to_send.append((current_socket, "5"))
                        send_waiting_messages()
                        for couple in players:
                            if current_socket in couple:
                                players.remove(couple)
                                open_client_sockets.remove(couple[0])
                                open_client_sockets.remove(couple[1])
                        continue
                    elif row == "9":  # 9 is the q for the winner
                        message_to_send.append((current_socket, row))
                        send_waiting_messages()
                        for couple in players:
                            if current_socket in couple:
                                players.remove(couple)
                                open_client_sockets.remove(couple[0])
                                open_client_sockets.remove(couple[1])
                        continue
                    else:
                        print "in the else"
                        c = current_socket.recv(1)
                        data = row + c  # send the together - client sends 2 packets
                        message_to_send.append((current_socket, data))
            send_waiting_messages()  # send it


if __name__ == '__main__':
    main()