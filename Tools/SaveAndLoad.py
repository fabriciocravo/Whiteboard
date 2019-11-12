import pickle
from tkinter import Tk
from Tools.graphical_widgets import ExternalWindows
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Tools.network import MConnection
import os
import time

class SaveAndLoad():

    #Here we define an object that allows the user to register the logs from his whiteboard
    Logs = {}

    def __init__(self, connexion, send_message_method):
        self.connexion = connexion
        self.send_message = send_message_method


    #For each message the user receives we append it to it's logs object
    #If the message is from the drag type we change it's position
    def append_to_Logs(self, msg):
        if(msg[0] in ['O', 'C', 'L', 'R', 'S', 'D', 'T']):
            self.Logs[msg[-1]] = msg[:-1]
        elif(msg[0] in ['E', 'Z']):
            self.delete_from_local_logs(msg)
        elif(msg[0] == 'DR'):
            self.change_position(msg)



    # Here we change the position in the Logs of objects that have been dragged on the scream
    def change_position(self, msg):

        # We retrieve the original message
        OriginalMessage = self.Logs[msg[1]]

        # Them add to the coordinates according to the drag!
        # The position of the coordinates of each message is different for different types of message
        # This requires us to alternate the coordinates differently according to the type
        if (OriginalMessage[0] in ['L', 'C', 'O', 'R', 'S', 'D']):
            OriginalMessage[1] = str(int(OriginalMessage[1]) + int(msg[2]))
            OriginalMessage[3] = str(int(OriginalMessage[3]) + int(msg[2]))
            OriginalMessage[2] = str(int(OriginalMessage[2]) + int(msg[3]))
            OriginalMessage[4] = str(int(OriginalMessage[4]) + int(msg[3]))
            OriginalMessage = " ".join(OriginalMessage)

            # Rewrite the log
        elif (OriginalMessage[0] in ['T']):
            OriginalMessage[2] = str(int(OriginalMessage[2]) + int(msg[2]))
            OriginalMessage[3] = str(int(OriginalMessage[3]) + int(msg[3]))
            OriginalMessage = " ".join(OriginalMessage)


    def delete_from_local_logs(self, msg):
        try:
            self.Logs.pop(msg[1])
        except KeyError:
            pass

    def save(self):
        path = asksaveasfilename( defaultextension=".pickle")
        try:
            with open(path, "wb") as file:
                pickle.dump(self.Logs, file)
        except FileNotFoundError:
            pass



    # Here we process and send the load messages
    def load(self):
        Tk().withdraw()
        filename = askopenfilename()
        try:
            with open(filename, 'rb') as file:

                self.LoadedLogs = pickle.load(file)
                for key in self.LoadedLogs:
                    self.send_message(self.LoadedLogs[key])
        except FileNotFoundError:
            pass




if __name__ == '__main__':

    s = SaveAndLoad()
    print(s)
