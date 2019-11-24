from Tools.network import MConnection

# This class contains all the information relating the Permission part of the Whiteboard
# Which means keeping track of connected users (if user is disconnected we give all permission to delete his stuff)
# Keeping track of the users i gave permission to delete my stuff (listOfPermissions)
# Keeping track of the users that allowed me to delete their stuff (listOfAllowed)
# Those are all declared as empty lists in the beginning of the class
class Permission():

    # For the initialization of this class, we initialize the data necessary for the permission module
    def __init__(self, connexion):
        self.my_connexion = connexion
        self._listOfAllowed = []
        self._listOfPermissions = []
        self._connected_users = []
        self._connected_users_buttons = []
        self._connected_users_permission_buttons = []


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
            self._connected_users.append(msg[1])
        elif _type == 'RE':
            print(self._listOfPermissions)
            self._connected_users.remove(msg[1])

    # Here we get the permissions from the message
    # The messages are from the type (P,user1,user2)
    # Which means user2 has given permission to user1
    # Since the message is echoed to the whole server (everyone receives a permission message)
    # I will only consider those for each there is a match
    # If i am user1 i will add user2 to my list of permissions
    # If i am user2 it means i just gave user1 permission so i add him to my listOfAllowed
    # If i am neither i just ignore the message!
    def _get_permission_from_message(self, msg):
        if (self.my_connexion.ID == msg[1]):
            if (msg[2] not in self._listOfPermissions):
                self._listOfPermissions.append(msg[2])
            else:
                self._listOfPermissions.remove(msg[2])

        elif (self.my_connexion.ID == msg[2]):
            if (msg[1] not in self._listOfAllowed):
                self._listOfAllowed.append(msg[1])
            else:
                self._listOfAllowed.remove(msg[1])

    # ____________________________Permission Message Sending__________________________________
    # Here we have the function that sends the permission message
    # Since the text from the button is the username we want to grant our permission to, we use that in the function
    # and them our own ID, since we are giving our permission to that user
    def send_permission_message(self, event):
        msg = ("P", event.widget['text'], self.my_connexion.ID)
        self.my_connexion.send_message(msg)


    # ENCAPSULATION PART ###############################################
    # - Protecting the List of Permissions
    def add_to_list_of_permission(self, userID):
        self._listOfPermissions.append(userID)

    def remove_from_list_of_permission(self, userID):
        self._listOfPermissions.remove(userID)

    def get_list_of_permissions(self):
        return self._listOfPermissions

    # Protecting List of Allowed########################################
    def add_to_list_of_allowed(self, userID):
        self._listOfAllowed.append(userID)

    def remove_from_list_of_allowed(self, userID):
        self._listOfPermissions.remove(userID)

    def get_list_of_allowed(self):
        return self._listOfAllowed

    # Protecting Connected Users########################################
    def add_to_connected_users(self, userID):
        self._connected_users.append(userID)

    def remove_from_connected_users(self, userID):
        self._connected_users.remove(userID)

    def get_connected_users(self):
        return self._connected_users

    # Protecting Connected Users Buttons#################################
    def add_to_connected_users_buttons(self, userID):
        self._connected_users_buttons.append(userID)

    def remove_from_connected_users_buttons(self, userID):
        self._connected_users_buttons.remove(userID)

    def pop_from_connected_users_buttons(self):
        self._connected_users_buttons.pop()

    def get_connected_users_buttons(self):
        return self._connected_users_buttons

    # Protecting Connected Users Permission Buttons######################
    def add_to_connected_users_permissions_buttons(self, userID):
        self._connected_users_permission_buttons.append(userID)

    def remove_from_connected_users_permissions_buttons(self, userID):
        self._connected_users_permission_buttons.remove(userID)

    def pop_from_connected_users_permissions_buttons(self):
        self._connected_users_buttons.pop()

    def get_connected_users_permissions_buttons(self):
        return self._connected_users_permission_buttons