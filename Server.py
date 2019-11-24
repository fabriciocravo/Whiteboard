import socket
import threading
import time

# Here we have the global variables
# The Clients consists of the list of thread objects clients
# The logs consists of all the messages send through the server, it is used to redraw when someone new connects
Clients = []
Logs = {}


# -------------------------------SERVER ----------------------------------------
# This is the Server Thread, it is responsible for listening to connexions
# It opens new connections as it is a thread constantly listening at the port for new requests
class Server:
    ID = 1

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Initialize network
        self.network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.network.bind((self.host, self.port))
        self.network.listen(10)
        print("The Server Listens at {}".format(port))

        # Start the pinger
        threading.Thread(target=self.pinger).start()

    # Here we have the main listener
    # As somebody connects we send a small hello as confirmation
    # Also we give him an unique ID that will be able to differentiate them from other users
    # We send the server logs so the new user can redraw at the same state in the board
    # We send the list of connected users to construct the permission system
    def start(self):
        print('listener started\n')
        while True:
            connexion, infos_connexion = self.network.accept()
            print("Sucess at " + str(infos_connexion))
            connexion.send('HLO'.encode())
            time.sleep(0.1)

            # Send all ID's so user cannot repeat any id's
            msg = " "
            for client in Clients:
                msg = msg + " " + client.clientID
            connexion.sendall(msg.encode())
            time.sleep(0.1)

            # Here we start a thread to wait for the users nickname input
            # We do this so a server can wait for a nickname input and listen to new connections
            threading.Thread(target=self.wait_for_user_nickname, args=[connexion]).start()

    # This function was created just to wait for the users input nickname
    # Once it's done if sends the logs so the user can be up to date with the board
    # And finally it creates the Client Thread which will be responsible for listening to the user messages
    def wait_for_user_nickname(self, connexion):
        # Receive the chosen ID from user
        new_user_id = connexion.recv(1024).decode()

        for log in Logs:
            connexion.send(Logs[log])

        new_client = Client(connexion, new_user_id)
        new_client.load_users()
        Clients.append(new_client)
        Server.ID = Server.ID + 1
        new_client.start()

    # Function used by pinger
    # Sends a removal message to alert all users of the disconnection
    def announce_remove_user(self, disconnectedClient):
        print("delete message sent\n")
        msg = 'RE' + ' ' + str(disconnectedClient.clientID)
        msg = msg.encode('ISO-8859-1')
        for client in Clients:
            client.connexion.sendall(msg)

    # This is the pinger function, it is used to check how many users are currently connected
    # It pings all connections, if it receives a disconnection error, it does the following things:
    # 1.Sends a removal message to alert all users of the disconnection
    # 2.Removes client from list of clients to avoid sending messages to it again
    # 3.Sends the permission to delete the disconnected user stuff from the board!
    def pinger(self):
        print('pinger started\n')
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


# -----------------------------------CLIENTS -------------------------------------
# This is the client thread, it is responsible for dealing with the messages from all different clients
# There is one thread for every connected client, this allows us to deal with them all at the same time
class Client():
    MessageID = 0

    def __init__(self, connexion, clientID):
        self.connexion = connexion
        self.clientID = clientID

    def load_users(self):
        for client in Clients:
            msg = 'A' + ' ' + str(client.clientID) + ' ' + 'Ø'
            self.connexion.send(msg.encode('ISO-8859-1'))
            msg = 'A' + ' ' + str(self.clientID) + ' ' + 'Ø'
            client.connexion.send(msg.encode('ISO-8859-1'))

    def start(self):
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

                splitted_msg = msg.split()

                # Z is used to indicate message deletion so let's echo with a different function
                # Deletion messages are treated differently from normal messages
                # We don't keep track of them, and they must erase their log from the server
                # So we call a different function to deal with them
                if splitted_msg[0] == 'Z' or splitted_msg[0] == 'E':
                    self.echoes_delete(msg,splitted_msg)
                    continue
                # Here we have the drag messages
                elif splitted_msg[0] == 'DR':
                    self.update_position_in_logs(splitted_msg)
                    self.echoesAct3(msg)
                    continue
                # We do not want to keep the logs
                elif splitted_msg[0] in ['P', 'TA']:
                    self.echoesAct3(msg)
                    continue
                elif splitted_msg[0] in ['O', 'C', 'L', 'R', 'S', 'E', 'D', 'Z', 'T']:
                    self.echoes(msg)

            # We pass the Connection Reset Error since the pinger will deal with it more effectivelly
            except ConnectionResetError:
                pass
            except ConnectionAbortedError:
                pass

    # Main echoes function!
    # This is responsible for echoing the message between the clients
    def echoesAct3(self, msg):
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
    # And finally echo the message to all members of the server
    def echoes_delete(self, msg, splitMsg):
        try:
            Logs.pop(splitMsg[1])
        except KeyError:
            pass
        self.echoesAct3(msg)

    # Here we update the position of a draged object in the server
    def update_position_in_logs(self, splitMsg):

        # We retrieve the original message
        original_message = Logs[splitMsg[1]]
        original_message = original_message[:-1]
        print(original_message)
        original_message = original_message.decode('ISO-8859-1')
        original_message = original_message.split()

        # Them add to the coordinates according to the drag!
        # The position of the coordinates of each message is different for different types of message
        # This requires us to alternate the coordinates differently according to the type
        if original_message[0] in ['L', 'C', 'O', 'R', 'S', 'D']:
            original_message[1] = str(int(original_message[1]) + int(splitMsg[2]))
            original_message[3] = str(int(original_message[3]) + int(splitMsg[2]))
            original_message[2] = str(int(original_message[2]) + int(splitMsg[3]))
            original_message[4] = str(int(original_message[4]) + int(splitMsg[3]))
            original_message = " ".join(original_message)
        elif original_message[0] in ['T']:
            original_message[2] = str(int(original_message[2]) + int(splitMsg[2]))
            original_message[3] = str(int(original_message[3]) + int(splitMsg[3]))
            original_message = " ".join(original_message)

            # Rewrite the log
        original_message = original_message + " Ø"
        Logs[splitMsg[1]] = original_message.encode('ISO-8859-1')


if __name__ == "__main__":
    host = ''
    port = 5000
    server = Server(host, port)
    server.start()


