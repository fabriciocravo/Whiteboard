from threading import Thread
from Tools.drawing_tools import DrawingTools
from Tools.graphical_widgets import ExternalWindows
import tkinter
import random as rd
import os

# This class is responsible for generating the chat between the users in the Whiteboard
class Messager(DrawingTools):

    # Ok, in the init function we start by stating the parent class
    # Them afterwards we use everything we need to construct a messaging tollbox
    # We define a Text object that will contain the list of messages send in the channel
    # And bellow that a Entry object that takes the inputs from the user
    # After taking the input from the user it sends a message to the network
    def __init__(self):
        DrawingTools.__init__(self)

        self.scroll_bar = tkinter.Scrollbar(self.myWhiteBoard)
        self.msg_list = tkinter.Text(self.myWhiteBoard, height = 25, width=25, yscrollcommand = self.scroll_bar.set, font="Courier", state="disabled")
        self.msg_list.place(x = 1200, y = 50)
        self.scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.e1 = tkinter.Entry(self.myWhiteBoard, justify="left")
        self.e1.place(x = 1200, y = 675, width=300)
        self.e1.bind("<Return>", lambda talk: self.talk_message() )
        send_button = tkinter.Button(self.myWhiteBoard, text="Send", command=self.talk_message)
        send_button.place(x = 1200, y = 700)

    # Here we print the received messages
    # The method is called in the client after the end of message character Ø has been removed
    # The messages are from the time (TA,user,message)
    # So we just take the end of the message msg[2:] to print it
    # The user that said it is the msg[1]
    def print_message(self, msg):
        user_said = " ".join(msg[2:])

        self.msg_list.config(state="normal")
        self.msg_list.insert(tkinter.END, msg[1] + ": " + user_said + "\n")
        self.msg_list.see("end")
        self.msg_list.config(state="disabled")

    # Here we take the messages from the Entry object to send them to the network
    # So we start by getting the message from the entry widget with .get()
    # We check to see if the user has put the end of character in the message (character reserved from that)
    # If it has we just ignore the message and inform the user the character is invalid!
    # Them we format the messages as the required
    # TA is the type of message, talk message
    # The network needs to know who send the message so we send the ID
    # Finally we send the message
    def talk_message(self):
        msg = self.e1.get()

        if ("Ø" in msg ):
            self.e1.delete(0, 'end')
            ExternalWindows.show_error_box("Invalid Ø character")
            return None
        self.e1.delete(0, 'end')
        msg = ("TA", self.ID, msg)
        self.send_message(msg)



