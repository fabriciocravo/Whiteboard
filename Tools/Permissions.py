from Tools.network import MConnection

# This class contains all the information relating the Permission part of the Whiteboard
# Which means keeping track of connected users (if user is disconnected we give all permission to delete his stuff)
# Keeping track of the users i gave permission to delete my stuff (listOfPermissions)
# Keeping track of the users that allowed me to delete their stuff (listOfAllowed)
# Those are all declared as empty lists in the beginning of the class
class Permission(MConnection):
    # ____________________________Necessary Data_______________________________________________
    listOfAllowed = []
    listOfPermissions = []
    connected_users = []
    connected_users_buttons = []
    connected_users_permission_buttons = []

    # For the initialization of this class, we just initialize the connection
    def __init__(self):
        MConnection.__init__(self)

    # ____________________________Permission Message Handling__________________________________
    # Here we deal with the permission type messages
    # If the message starts with a P of the type (P,user1,user2) it is user2 giving a permission to user1
    # If the message starts with an A it is the connection of a new user
    # If the message starts with an RE it is the removal (or exit) of an existing user
    def user_communication(self, msg):

        _type = msg[0]
        if _type == 'P':
            self._get_permission_from_message(msg)
        elif _type == 'A':
            self.connected_users.append(msg[1])
        elif _type == 'RE':
            self.connected_users.remove(msg[1])

    # Here we get the permissions from the message
    # The messages are from the type (P,user1,user2)
    # Which means user2 has given permission to user1
    # Since the message is echoed to the whole server (everyone receives a permission message)
    # I will only consider those for each there is a match
    # If i am user1 i will add user2 to my list of permissions
    # If i am user2 it means i just gave user1 permission so i add him to my listOfAllowed
    # If i am neither i just ignore the message!
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

    # ____________________________Permission Message Sending__________________________________
    # Here we have the function that sends the permission message
    # Since the text from the button is the username we want to grant our permission to, we use that in the function
    # and them our own ID, since we are giving our permission to that user
    def send_permission_message(self, event):
        msg = ("P", event.widget['text'], self.ID)
        self.send_message(msg)

