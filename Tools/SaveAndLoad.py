import pickle
from tkinter import Tk
from Tools.graphical_widgets import ExternalWindows
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Tools.Permissions import Permission

# This class allows the user to save and load the state of the Whiteboard
# To do that each user keeps a record of the server logs within themselves
# However, they are stored differently, here they are store in tuple format
# In the server they are stored in message format
# This allows for direct sending in both cases!
class SaveAndLoad(Permission):

    #Here we define an object that allows the user to register the logs from his whiteboard
    Logs = {}

    def __init__(self):
        Permission.__init__(self)


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
    # Quite similar to a function in the Server!
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
        elif (OriginalMessage[0] in ['T']):
            OriginalMessage[2] = str(int(OriginalMessage[2]) + int(msg[2]))
            OriginalMessage[3] = str(int(OriginalMessage[3]) + int(msg[3]))

    # Here we delete an object from the logs if a delete message has been received
    def delete_from_local_logs(self, msg):
        try:
            self.Logs.pop(msg[1])
        except KeyError:
            pass

    # Here we save the state of the board by using a pickle of the dictionary created to store the logs
    def save(self):
        path = asksaveasfilename( defaultextension=".pickle")
        try:
            with open(path, "wb") as file:
                pickle.dump(self.Logs, file)
        except FileNotFoundError:
            pass

    # Here we process and send the load messages
    # Ask to open the pickle file and them spam the messages from the dictonary
    # Since the messages are already in the needed format we just send them directly
    def load(self):
        filename = askopenfilename()
        try:
            with open(filename, 'rb') as file:
                self.LoadedLogs = pickle.load(file)
                for key in self.LoadedLogs:
                    self.send_message(self.LoadedLogs[key])
        except FileNotFoundError:
            pass



