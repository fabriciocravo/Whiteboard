from threading import Thread
from Tools.drawing_tools import DrawingTools
from Tools.graphical_widgets import ExternalWindows
import tkinter
import random as rd
import os

# This class is responsible for generating the chat between the user on the Python console
class Messager(DrawingTools):


    # In the init function we define what we need to construct the messaging part of our program
    # We have all that is needed to
    def __init__(self, ID, connexion, send_message_method):
        DrawingTools.__init__(self, ID, connexion, send_message_method)
        self.userID = ID
        self.connexion = connexion
        self.send_message = send_message_method

        self.scroll_bar = tkinter.Scrollbar(self.myWhiteBoard)
        self.msg_list = tkinter.Text(self.myWhiteBoard, height = 25, width=25, yscrollcommand = self.scroll_bar.set, font="Courier", state="disabled")
        self.msg_list.place(x = 1200, y = 50)
        self.scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.e1 = tkinter.Entry(self.myWhiteBoard, justify="left")
        self.e1.place(x = 1200, y = 675, width=300)
        self.e1.bind("<Return>", lambda talk: self.talk_message() )
        send_button = tkinter.Button(self.myWhiteBoard, text="Send", command=self.talk_message)
        send_button.place(x = 1200, y = 700)






    # This method is called in the client! If a message that needed to be printed was received
    # We print it here!
    def print_message(self, msg):
        user_said = " ".join(msg[2:])

        self.msg_list.config(state="normal")
        self.msg_list.insert(tkinter.END, msg[1] + ": " + user_said + "\n")
        self.msg_list.see("end")
        self.msg_list.config(state="disabled")


    def talk_message(self):
        msg = self.e1.get()

        if ("Ø" in msg ):
            self.e1.delete(0, 'end')
            ExternalWindows.show_error_box("Invalid character")
            return None
        self.e1.delete(0, 'end')
        msg = ("TA", self.userID, msg)
        self.send_message(msg)



