from tkinter import *
from Tools.graphical_widgets import ExternalWindows

class Whiteboard:

    # Here we initiate with the line drawing tool, this is the tool currently used to draw
    drawing_tool = "line"
    # Here we have the dictionary with the used colors to paint!
    Colors = {'b': 'blue', 'r': 'red', 'g': 'green', 'o': 'orange', 'y': 'yellow', 'c': 'cyan', 'p': 'purple1',
              'd': 'black', 's': 'snow'}

    # Here we initiate the whiteboard by calling all the functions necessary to construct it
    # And also initiate the parent class!
    # We call the save and load and permission classes here, we need them to instantiate the buttons
    def __init__(self, connexion , save_and_load, permissions):
        self.my_connexion = connexion
        self.save_and_load = save_and_load
        self.permissions = permissions
        self._init_whiteboard()
        self._init_item_button()
        self._init_user_button()
        self._init_color_button()
        self._init_drawing_area()
        self.color = 'b'

    # Here we have the main loop of the Whiteboard when it is closed it executes the code just bellow
    # Which raises an exception that closes the software
    def show_canvas(self):
        mainloop()
        raise Exception("Board Closed Ending Execution")

    # Here we initiate the whiteboard with Tk() and set it's dimensions
    def _init_whiteboard(self):
        self.myWhiteBoard = Tk()
        self.myWhiteBoard.geometry('2000x1100')

    # ---------------------------------- Button functions ------------------------------------------
    # Here we have the buttons on the top of the whiteboard
    # Those buttons are responsible for changing the drawing tool as their name indicates
    # Every button pressed is a different drawing tool
    def _init_item_button(self):
        Button(self.myWhiteBoard, text='line', height=1, width=5, bg='dark goldenrod', font='Arial',
               command=lambda: self.set_drawing_tool('line')).place(x=70, y=0)
        Button(self.myWhiteBoard, text='rect', height=1, width=5, bg='saddle brown', font='Arial',
               command=lambda: self.set_drawing_tool('rectangle')).place(x=140, y=0)
        Button(self.myWhiteBoard, text='oval', height=1, width=5, bg='NavajoWhite4', font='Arial',
               command=lambda: self.set_drawing_tool('oval')).place(x=210, y=0)
        Button(self.myWhiteBoard, text='text', height=1, width=5, bg='SteelBlue4', font='Arial',
               command=self.get_text_from_user).place(x=280, y=0)
        Button(self.myWhiteBoard, text='pencil', height=1, width=5, bg='DeepSkyBlue2', font='Arial',
               command=lambda: self.set_drawing_tool('pencil')).place(x=350, y=0)
        Button(self.myWhiteBoard, text='circle', height=1, width=5, bg='Turquoise2', font='Arial',
               command=lambda: self.set_drawing_tool('circle')).place(x=420, y=0)
        Button(self.myWhiteBoard, text='square', height=1, width=5, bg='CadetBlue1', font='Arial',
               command=lambda: self.set_drawing_tool('square')).place(x=490, y=0)
        Button(self.myWhiteBoard, text='eraser', height=1, width=5, bg='purple1', font='Arial',
               command=lambda: self.set_drawing_tool('eraser')).place(x=560, y=0)
        Button(self.myWhiteBoard, text='drag', height=1, width=5, bg='green', font='Arial',
               command=lambda: self.set_drawing_tool('drag')).place(x=630, y=0)
        Button(self.myWhiteBoard, text='delALL', height=1, width=5, bg='snow', font='Arial',
               command=self.erase_all).place(x=700, y=0)

    # This is the own user button, it is used mostly as a display of the user name
    def _init_user_button(self):
        Button(self.myWhiteBoard, text=self.my_connexion.ID, height=1, width=5, bg='snow').place(x=1100, y=0)

    # This are the color buttons, they are responsible for changing the colors of the corresponding drawings
    def _init_color_button(self):

        Button(self.myWhiteBoard, height=1, width=5, bg='red',
               command=lambda: self.set_color('red')).place(x=1010,y=50)
        Button(self.myWhiteBoard, height=1, width=5, bg='orange',
               command=lambda: self.set_color('orange')).place(x=1010, y=100)
        Button(self.myWhiteBoard, height=1, width=5, bg='yellow',
               command=lambda: self.set_color('yellow')).place(x=1010, y=150)
        Button(self.myWhiteBoard, height=1, width=5, bg='green',
               command=lambda: self.set_color('green')).place(x=1010, y=200)
        Button(self.myWhiteBoard, height=1, width=5, bg='cyan',
               command=lambda: self.set_color('cyan')).place(x=1010, y=250)
        Button(self.myWhiteBoard, height=1, width=5, bg='blue',
               command=lambda: self.set_color('blue')).place(x=1010, y=300)
        Button(self.myWhiteBoard, height=1, width=5, bg='purple1',
               command=lambda: self.set_color('purple1')).place(x=1010, y=350)
        Button(self.myWhiteBoard, height=1, width=5, bg='black',
               command=lambda: self.set_color('black')).place(x=1010, y=400)
        Button(self.myWhiteBoard, height=1, width=5, bg='snow',
               command=lambda: self.set_color('snow')).place(x=1010, y=450)
        Button(self.myWhiteBoard, height=1, width=5, bg='snow', text="Save", command=self.save_and_load.save).place(x=1010,
                                                                                                           y=500)
        Button(self.myWhiteBoard, height=1, width=5, bg='snow', text="Load", command=self.save_and_load.load).place(x=1010,
                                                                                                           y=550)

    # This function updates the current connected users on the channel
    # Every time a user connects or disconnects we call this function
    # This function destroys all the buttons used for displaying the users and them recreates them based on the new list
    # Each client has a list of the connected users in the network
    # It is also used to show the list of users who gave you permission to delete their stuff
    # If you have received permission to delete somebody else's stuff, they will be in your list of permission
    # This generate a button with their ID displayed in the program
    def update_connected_user(self):
        start_y = 50
        while len(self.permissions.get_connected_users_buttons()) != 0:
            button = self.permissions.pop_from_connected_users_buttons()
            button.destroy()
        for userID in self.permissions.get_connected_users():
            if (userID in self.permissions.get_list_of_allowed()):
                button = Button(self.myWhiteBoard, text=userID, height=1, width=5, bg='green')
                button.bind('<Button-1>', self.permissions.send_permission_message)
            else:
                button = Button(self.myWhiteBoard, text=userID, height=1, width=5, bg='red')
                button.bind('<Button-1>', self.permissions.send_permission_message)
            button.place(x=1100, y=start_y)
            self.permissions.add_to_connected_users_buttons(button)

            start_y += 50

        start_y = 50
        while len(self.permissions.get_connected_users_permissions_buttons()) != 0:
            button = self.permissions.pop_from_connected_users_permissions_buttons()
            button.destroy()
        for userID in self.permissions.get_connected_users():
            if (userID in self.permissions.get_list_of_permissions()):
                button = Button(self.myWhiteBoard, text=userID, height=1, width=5, bg='snow')
                button.place(x=1150, y=start_y)
                self.permissions.add_to_connected_users_permissions_buttons(button)
                start_y += 50

    # Here we initiate the drawing area, which is a canvas
    # and place it accordingly
    def _init_drawing_area(self):
        self.drawing_area = Canvas(self.myWhiteBoard, width=1000, height=1000, bg='white')
        self.drawing_area.place(y=50)

    # ---------CHANGE DRAWING TOOL---------------
    # Here we change the drawing tools according to the widget that was pressed on the top
    def set_drawing_tool(self, tool):
        self.drawing_tool = tool

    # This functions are called when the user presses color button!
    # They set the byte that will be send on the message to send the color to be used to draw
    def set_color(self, color):
        color_to_set = [k for k, v in self.Colors.items() if v == color]
        if len(color_to_set) == 1:
            self.color = color_to_set[0]
        else:
            print("Unknown color, check the code!")

    #################################GETIING THE TEXT##################################################################
    # This part gets text from the user before printing it!
    # It refers to the text functionality of the text button widget on the top
    def get_text_from_user(self):
        self.drawing_tool = 'text'
        ExternalWindows.get_text_from_user()

    # ----------------------------- Erase All Function -----------------------------------------------------------------
    # Since this is an extra functionality i will explain it more extensively
    # This function finds every object tagged with the user nickname (user ID)
    # And also every single object tagged with an user which is in his list of permissions
    # Since every user is in it's own list of permissions, we only need to check the list of permissions
    # Disconnected users loose their privileges!
    # Them it sends a delete message for every one of them!
    def erase_all(self):
        A = self.drawing_area.find_all()
        for a in A:
            a = self.drawing_area.gettags(a)
            if a[0] in self.permissions.get_list_of_permissions() or a[0] not in self.permissions.get_connected_users():
                msg = ("E",a[1])
                self.my_connexion.send_message(msg)