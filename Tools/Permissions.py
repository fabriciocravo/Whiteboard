from Tools.network import MConnection
from Tools.SaveAndLoad import SaveAndLoad

class Permission(MConnection):

    listOfAllowed = []
    listOfPermissions = []
    connected_users = []
    connected_users_buttons = []
    connected_users_permission_buttons = []

    def __init__(self):
        MConnection.__init__(self)

    def user_communication(self, msg):

        _type = msg[0]
        if _type == 'P':
            self._get_permission_from_message(msg)
        elif _type == 'A':
            self.connected_users.append(msg[1])
        elif _type == 'RE':
            self.connected_users.remove(msg[1])

    def _get_permission_from_message(self, msg):
        if (self.ID == msg[1]):
            if (msg[2] not in self.listOfPermissions):
                self.listOfPermissions.append(msg[2])
            else:
                self.listOfPermissions.remove(msg[2])

        elif (self.ID == msg[2]):
            if (msg[1] not in self.listOfAllowed):
                self.listOfAllowed.append(msg[1])
            else:
                self.listOfAllowed.remove(msg[1])

    def send_permission_message(self, event):
        msg = ("P", event.widget['text'], self.ID)
        self.send_message(msg)

