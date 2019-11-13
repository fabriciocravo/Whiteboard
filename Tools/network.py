import socket
from Tools.graphical_widgets import ExternalWindows

# Here we have the connection class! It is responsible for starting the connection with the server
# It also does the message sending and receiving part (handles all messages)
class MConnection:

    # Here we have the first part, we start the program by using the getValuesFromUser function
    # This function is the main box that appears requesting the IP and the port from the user
    # From this class we recover the values that have been typed on the widget to start our connection!
    def __init__(self):
        ExternalWindows.getValuesFromUser()
        self.host = ExternalWindows.return_ip()
        self.port = ExternalWindows.return_port()

        # Here we attempt to establish a connection
        # We open a socket in the given port and IP
        # And start by checking to see if we received a greeting 'HLO'
        # Afterwards the server will send a list with all the names of the connected users
        # This is done to avoid repeating names when creating a new user
        # After the id has been chosen it responds to the server so it can add to the list of clients
        try:
            self.s = socket.socket()
            self.s.connect((self.host, self.port))
            data = self.s.recv(3).decode()
            if data == 'HLO':
                print('[Network]Connection with %s:%s established.' % (self.host, self.port))

            data = self.s.recv(1024).decode()
            UserNames = data.split()

            while True:
                ExternalWindows.get_nickname_from_user()
                self.ID = ExternalWindows.return_nickname()
                if (self.ID in UserNames):
                    ExternalWindows.show_error_box("User name is taken")
                    continue
                break

            self.s.sendall(self.ID.encode())
            print("Received ID is : " + self.ID)
        except SystemExit:
            exit()
        except:
            ExternalWindows.show_error_box("Could not connect to server")
            raise Exception("Connection Failed")

    # Here we have the send message function
    # The messages are received in the form of a tuple (A,B,C)
    # And in here they are transformed in a binary message of the form b"A B C Ø"
    # The Ø indicates the end of the message! and the type and beginning of the message is indicated
    # with a set of specific letters.
    def send_message(self, msg):
        msg = ' '.join(map(str, msg))
        msg = msg + " Ø"
        try:
            msg = msg.encode('ISO-8859-1')
            self.s.send(msg)
        except UnicodeEncodeError:
            ExternalWindows.show_error_box("Invalid character!")

    # Here we receive the messages, we take in a message of the form b"A B C Ø" and transform it
    # We transform it in a tuple of format (A,B,C)
    # From that tuple each class will recover the essential information for all it's functions
    # Now the ß that is ignored is a ping from the server
    # It is used to detect if users are still connected and act accordingly to their connection
    # So we ignore it when receiving messages
    def receive_message(self):
        msg = ""
        while True:
            data = self.s.recv(1).decode('ISO-8859-1')
            if data == "Ø":
                break
            if data == "ß":
                continue
            msg = msg + data
        msg = msg.split()
        print(msg)
        return msg


