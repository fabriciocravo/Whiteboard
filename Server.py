import socket
import struct
import threading
import time

# Here we have the global variables
# The clients consists of the list of thread objects clients
# The logs consists of all the messages send through the server, it is used to redraw when someone new connects
Clients = []
Logs = {}

# -------------------------------SERVER ----------------------------------------
# This is the Server Thread, it is responsible for listening to connexions
# It opens new connections as it is a thread constantly listening at the port for new requests
class Server(threading.Thread):

    ID = 1

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

        #Initialize network
        self.network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.network.bind((self.host, self.port))
        self.network.listen(10)
        print("The Server Listens at {}".format(port))

    # Here we have the main listener
    # As somebody connects we send a small hello as confirmation
    # Also we give him an unique ID that will be able to differentiate them from other users
    # We send the server logs so the new user can redraw at the same state in the board
    # We send the list of connected users to construct the permission system
    def run(self):
        while True:
            connexion, infos_connexion = self.network.accept()
            print("Sucess at " + str(infos_connexion))
            Hello = 'HLO'.encode()
            connexion.send(Hello)

            time.sleep(0.1)

            #Send all ID's so user cannot repeat any id's
            msg = b" "
            for client in Clients:
                msg = msg + b" " + client.clientID.encode()
            connexion.sendall(msg)

            time.sleep(0.1)

            # Here we start a thread to wait for the users nickname input
            # We do this so a server can wait for a nickname input and listen to new connections
            threading.Thread(target=self.wait_for_user_nickname, args=[connexion]).start()

    # This function was created just to wait for the users input nickname
    # Once it's done if sends the logs so the user can be up to date with the board
    # And finally it creates the Client Thread which will be responsible for listening to the user messages
    def wait_for_user_nickname(self, connexion):
        # Receive the chosen ID from user
        NewUserId = connexion.recv(1024).decode()

        for log in Logs:
            connexion.send(Logs[log])

        a = Client(connexion, NewUserId)

        a.load_users()
        Clients.append(a)
        Server.ID = Server.ID + 1
        a.start()


# -----------------------------------CLIENTS -------------------------------------
# This is the client thread, it is responsible for dealing with the messages from all different clients
# There is one thread for every connected client, this allows us to deal with them all at the same time
class Client(threading.Thread):

    MessageID = 0

    def __init__(self, connexion, clientID):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.clientID = clientID

    def load_users(self):
        for client in Clients:
            msg = 'A' + ' ' + str(client.clientID) + ' ' + 'Ø'
            self.connexion.send(msg.encode('ISO-8859-1'))
            msg = 'A' + ' ' + str(self.clientID) + ' ' + 'Ø'
            client.connexion.send(msg.encode('ISO-8859-1'))

    def run(self):
        while True:
            try:
                # Here we start by reading the messages
                # Split according to the protocol
                msg = ""
                while True:
                    data = self.connexion.recv(1).decode('ISO-8859-1')
                    if data == "Ø":
                        break
                    msg = msg + data

                splitMsg = msg.split()

                # Z is used to indicate message deletion so let's echo with a different function
                # Deletion messages are treated differently from normal messages
                # We don't keep track of them, and they must erase their log from the server
                # So we call a different function to deal with them
                if (splitMsg[0] == 'Z' or splitMsg[0] == 'E'):
                    self.echoes_delete(msg,splitMsg)
                    continue
                # Here we have the drag messages
                elif(splitMsg[0] == 'DR'):
                    self.update_position_in_logs(splitMsg)
                    self.echoesAct3(msg)
                    continue
                # We do not want to keep the logs
                elif(splitMsg[0] in ['P','TA'] ):
                    self.echoesAct3(msg)
                    continue
                elif(splitMsg[0] in ['O', 'C', 'L', 'R', 'S', 'E', 'D', 'Z', 'T']):
                    self.echoes(msg)

            # We pass the Connection Reset Error since the pinger will deal with it more effectivelly
            except ConnectionResetError:
                pass
            except ConnectionAbortedError:
                pass

    # Main echoes function!
    # This is responsible for echoing the message between the clients
    def echoesAct3(self,msg):
        msg = msg + " Ø"
        msg = msg.encode('ISO-8859-1')
        for client in Clients:
            client.connexion.sendall(msg)

    # Here we echo messages to all members of the network
    # Keep a dictionary of the messages to send it to new users
    # Update the message number for every message send
    def echoes(self, msg):
        msg = msg + " " + "m" + str(Client.MessageID)
        # We need to keep logs of all drawing messages to redraw them on new arriving clients
        Logs["m" + str(Client.MessageID)] = msg.encode('ISO-8859-1') + " Ø".encode('ISO-8859-1')
        Client.MessageID = Client.MessageID + 1
        # We do not want to log some types of messages. For instance like permission messages
        self.echoesAct3(msg)


    # Here we echo delete messages
    # We need to remove them from the message log
    # And finally echoe the message to all members of the server
    def echoes_delete(self, msg, splitMsg):
        try:
            Logs.pop(splitMsg[1])
        except KeyError:
            pass
        self.echoesAct3(msg)


    # Here we update the position of a draged object in the server
    def update_position_in_logs(self, splitMsg):

        # We retrieve the original message
        OriginalMessage = Logs[splitMsg[1]]
        OriginalMessage = OriginalMessage[:-1]
        print(OriginalMessage)
        OriginalMessage = OriginalMessage.decode('ISO-8859-1')
        OriginalMessage = OriginalMessage.split()

        # Them add to the coordinates according to the drag!
        # The position of the coordinates of each message is different for different types of message
        # This requires us to alternate the coordinates differently according to the type
        if( OriginalMessage[0] in ['L', 'C', 'O', 'R', 'S', 'D']):
            OriginalMessage[1] = str(int(OriginalMessage[1]) + int(splitMsg[2]))
            OriginalMessage[3] = str(int(OriginalMessage[3]) + int(splitMsg[2]))
            OriginalMessage[2] = str(int(OriginalMessage[2]) + int(splitMsg[3]))
            OriginalMessage[4] = str(int(OriginalMessage[4]) + int(splitMsg[3]))
            OriginalMessage = " ".join(OriginalMessage)
        elif( OriginalMessage[0] in ['T'] ):
            OriginalMessage[2] = str(int(OriginalMessage[2]) + int(splitMsg[2]))
            OriginalMessage[3] = str(int(OriginalMessage[3]) + int(splitMsg[3]))
            OriginalMessage = " ".join(OriginalMessage)

            # Rewrite the log
        OriginalMessage = OriginalMessage + " Ø"
        Logs[splitMsg[1]] = OriginalMessage.encode('ISO-8859-1')

# --------------------------------PINGER------------------------------------------------------------
# This is the pinger Thread, it is used to check how many users are currently connected
# It sends messages to all users, if it receives a disconnection error it does the following
# Sends a removal message to alert all users of the disconnection
# Removes client from list of clients to avoid sending messages to it again
# Also it sends the permission to delete the disconnected user stuff from the board!
class Pinger(Client):

    def __init__(self):
        threading.Thread.__init__(self)

    def announce_remove_user(self, disconnectedClient):
        msg = 'RE' + ' ' + str( disconnectedClient.clientID)
        self.echoesAct3(msg)


    def run(self):
        while True:
            time.sleep(0.1)
            for client in Clients:
                try:
                    msg = "ß".encode('ISO-8859-1')
                    client.connexion.send(msg)
                except ConnectionResetError:
                    Clients.remove(client)
                    self.announce_remove_user(client)
                except ConnectionAbortedError:
                    Clients.remove(client)
                    self.announce_remove_user(client)


if __name__ == "__main__":

    host = ''
    port = 5000
    server = Server(host,port)
    server.start()
    Pinger().start()


