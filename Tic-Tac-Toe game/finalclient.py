"""necessary libraries"""
import Tkinter as tk
import socket
import select
import tkMessageBox
from time import sleep

"""FINALS"""
IP = '127.0.0.1'
PORT = 9010
TYPE1 = "blue"
TYPE2 = "red"
POINTERSM = [[None, None, None], [None, None, None], [None, None, None]]
FUTURE = 0.4


"""If the exit button is clicked while playing"""


def cls():
    global root
    global mainwindow
    global client_socket
    if tkMessageBox.askokcancel('Leave', 'Are you sure you want to leave?'):
        if client_socket is not None:
            mainwindow = False
            client_socket.send("5")
            root.destroy()


"""
change the color of the cube by click only 
if its the right turn 
then send the indexes to the server
"""


def color_click_change(event):
    global turn
    if event.widget['bg'] == TYPE1 or event.widget['bg'] == TYPE2 or turn is False:
        return
    event.widget['bg'] = TYPE1  # change the color to blue - your color
    a = (event.widget.grid_info()['row'], event.widget.grid_info()['column'])
    row = a[0]
    column = a[1]
    client_socket.send(row)  # send the row
    client_socket.send(column)  # send the column
    turn = False
    t['text'] = "opps turn"


"""change the turns"""


def changeColor(r, c):
    global POINTERSM
    global turn
    global root
    global t
    turn = True
    t['text'] = "Your turn"
    POINTERSM[r][c].config(bg='red')


"""Make the grid when duplicate clients are connected"""


def makeGrid():
    global wa
    global mainwindow
    global gridpacket
    global root
    global t
    root.state('zoomed')
    root.title("Tic-Tac-Toe")
    root.protocol("WM_DELETE_WINDOW", cls)
    root.configure(background='#b29691')
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()
    root.geometry("%dx%d" % (x+100, y))
    t = tk.Label(root, text="Try to be the first\n", font=("Arial Bold", 20), pady=10, fg="Red", background='#b29691')
    t.pack(side='left', padx=80)
    gridpacket = tk.Frame(root, width=200, height=y)
    gridpacket.pack()
    gridpacket.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    for j in range(0, 3, 1):#create 3 on 3 grid
        for x in range(0, 3, 1):
            c = tk.Label(gridpacket, width=30, height=15, relief="solid", background="white", borderwidth=2)
            c.bind("<Button-1>", color_click_change)
            c.grid(row=j, column=x)
            POINTERSM[j][x] = c
    mainwindow = True


"""check if the client wins"""


def checkwin(ty):
    global POINTERSM
    # loop through rows and columns
    for c in range(0, 3):
        # check for horizontal line
        if POINTERSM[c][0].cget('bg') == POINTERSM[c][1].cget('bg') == POINTERSM[c][2].cget('bg') == ty:
            return True
        # check for vertical line
        elif POINTERSM[0][c].cget('bg') == POINTERSM[1][c].cget('bg') == POINTERSM[2][c].cget('bg') == ty:
            return True
        # check for diagonal win (left to right)
        elif POINTERSM[0][0].cget('bg') == POINTERSM[1][1].cget('bg') == POINTERSM[2][2].cget('bg') == ty:
            return True
        # check for diagonal win (right to left)
        elif POINTERSM[0][2].cget('bg') == POINTERSM[1][1].cget('bg') == POINTERSM[2][0].cget('bg') == ty:
            return True
    return False


"""function for the case that the client press on exit"""


def exb():
    global wa
    global out
    if tkMessageBox.askokcancel('Leave', 'Are you sure you want to leave?'):
        out = True  # global var fpr the client situation


"""window while waiting"""


def waitingwindow():
    global wa
    wa = tk.Tk()
    wa.state('zoomed')
    wa.title('Tic-Tac-Toe')
    wa.protocol("WM_DELETE_WINDOW", exb)
    x = wa.winfo_screenwidth()
    y = wa.winfo_screenheight()
    wa.geometry("%dx%d" % (x, y))
    lb1 = tk.Label(wa, text="Waiting For Player\n", font=("Arial Bold", 70), pady=40, fg="green")
    p1 = tk.Label(wa, text="YOUR COLOR: BLUE \n", font=("Arial Bold", 30), pady=40, fg="blue")
    p2 = tk.Label(wa, text="RIVAL COLOR: RED ", font=("Arial Bold", 30), pady=40, fg="Red")
    lb1.pack()
    p1.pack()
    p2.pack()


"""window for a winner"""


def winnerwindow():
    global client_socket
    print "victory"
    global root
    w = tk.Tk()
    w.state('zoomed')
    w.title('YOU WON')
    x = w.winfo_screenwidth()
    y = w.winfo_screenheight()
    w.geometry("%dx%d" % (x, y))
    lb1 = tk.Label(w, text="YOU WON", font=("Arial Bold", 100), pady=40, fg="green")
    btn1 = tk.Button(w, text='Exit', command=exit, font=("Arial Bold", 40), activebackground="black", pady=10)
    lb1.pack()
    btn1.pack()
    client_socket.send("9")
    w.mainloop()


"""window winner by the leaving of the competition"""


def winnerbyleave():
    global client_socket
    print "victory"
    w = tk.Tk()
    w.state('zoomed')
    w.title('Tic-Tac-Toe')
    x = w.winfo_screenwidth()
    y = w.winfo_screenheight()
    w.geometry("%dx%d" % (x, y))
    lb1 = tk.Label(w, text="Rival left, YOU WON", font=("Arial Bold", 80), pady=40, fg="green")
    btn1 = tk.Button(w, text='Exit', command=exit, font=("Arial Bold", 40), activebackground="black", pady=10)
    lb1.pack()
    btn1.pack()
    w.mainloop()


"""get the after even window"""


def evenwindow():
    global client_socket
    print "even"
    w = tk.Tk()
    w.state('zoomed')
    w.title('DRAW')
    x = w.winfo_screenwidth()
    y = w.winfo_screenheight()
    w.geometry("%dx%d" % (x, y))
    lb1 = tk.Label(w, text="DRAW", font=("Arial Bold", 100), pady=40, fg="blue")
    btn1 = tk.Button(w, text='Exit', command=exit, font=("Arial Bold", 40), activebackground="black", pady=10)
    lb1.pack()
    btn1.pack()
    client_socket.send("9")
    w.mainloop()


"""check a case of even game"""


def even():
    for j in range(0, 3, 1):#create 3 on 3 grid
        for x in range(0, 3, 1):
            if POINTERSM[j][x].cget('bg') == "white":
                return False
    return True


"""The window that each looser get"""


def losewindow():
    print "lose"
    w = tk.Tk()
    w.title('YOU LOST')
    w.state('zoomed')
    x = w.winfo_screenwidth()
    y = w.winfo_screenheight()
    w.geometry("%dx%d" % (x, y))
    lb1 = tk.Label(w, text="YOU LOST", font=("Arial Bold", 100), pady=40, fg="Red")
    btn1 = tk.Button(w, text='Exit', command=exit, font=("Arial Bold", 40), activebackground="red", pady=10)
    lb1.pack()
    btn1.pack()
    w.mainloop()



def main():
    global client_socket
    global POINTERSM  # pointers for each square in the grid
    global turn #your turn or not
    global FUTURE
    global wa  # like root of all of the other window than the grid
    global out  # global var fpr the client situation
    global root
    out = False
    turn = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.settimeout(0.2) #help to overcome errors
    print "Client is running"
    waitingwindow()  # window until 2 players are connected
    while True:
        wa.update()
        print out
        try:
            q = client_socket.recv(1)
            if q == "1":
                break
        except socket.timeout: #because of the timeout definition
            if out is True:
                print "in out is true"
                wa.destroy()
                client_socket.close()
                return
    sleep(2)  # wait 2 second until start
    wa.destroy()
    root = tk.Tk()
    makeGrid()  # make the boardgame
    while mainwindow:  # while nobody is out
        root.update()  # update the board
        rlist, wlist, xlist = select.select([client_socket], [client_socket], [], 0.1)  # timeout is small so its ok
        for stream in rlist:
            r = stream.recv(1)
            if r == "":
                break
            elif r == "5":  # winning by others leaving
                client_socket.send("5")
                root.destroy()
                winnerbyleave()
                break
            elif r == "9":  # lose situation
                root.destroy()
                losewindow()
                break
            else:
                try:
                    c = stream.recv(1)
                    print r + c # the index of the square to press
                    changeColor(int(r), int(c))
                except socket.timeout:
                    pass
        if mainwindow is True: # check situations of winning oor loosing
            if checkwin("blue") is True:
                root.destroy()
                winnerwindow()
                break
            elif checkwin("red"):
                print "got he lost"
                root.destroy()
                losewindow()
                break
            elif even() is True:
                evenwindow()
                break
    client_socket.close()
    if mainwindow is False:  # if the player is out
        losewindow()


if __name__ == '__main__':
    main()