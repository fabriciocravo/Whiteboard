import socket
from Tools.graphical_widgets import ExternalWindows


class MConnection:
    def __init__(self):
        ExternalWindows.getValuesFromUser()
        self.host = ExternalWindows.return_ip()
        self.port = ExternalWindows.return_port()

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

    def send_message(self, msg):
        msg = ' '.join(map(str, msg))
        msg = msg + " Ø"
        try:
            msg = msg.encode('ISO-8859-1')
            self.s.send(msg)
        except UnicodeEncodeError:
            ExternalWindows.show_error_box("Invalid character!")


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
        return msg


