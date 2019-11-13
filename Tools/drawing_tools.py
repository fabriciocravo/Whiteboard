import tkinter.font as font
import math
from Tools.Whiteboard import Whiteboard


class DrawingTools(Whiteboard):
    # ----------DEFINING METHODS FOR DRAWING FROM MESSAGE----------------
    Colors = {'b': 'blue', 'r': 'red', 'g': 'green', 'o': 'orange', 'y': 'yellow', 'c': 'cyan', 'p': 'purple1',
              'd': 'black', 's': 'snow'}
    line_width = 2

    def __init__(self):
        Whiteboard.__init__(self)

    # ---------- DRAW FROM MESSAGE----------

    # Here we draw from the received message
    # All messages here are tuples with the format (A,B,C,D,F)
    # And A, the first index of the tuple, contains the type of message
    # B,C usually contain coordinates from creation of the message
    # D contains the user that has draw the message
    # F contains an unique id for each message, this allows us to find the object when needed
    def draw_from_message(self, msg):
        _type = msg[0]
        if _type == 'O':
            self._draw_oval_from_message(msg)
        elif _type == 'C':
            self._draw_circle_from_message(msg)
        elif _type == 'L':
            self._draw_line_from_message(msg)
        elif _type == 'R':
            self._draw_rectangle_from_message(msg)
        elif _type == 'S':
            self._draw_square_from_message(msg)
        elif _type == 'E':
            self._draw_erase_from_message(msg)
        elif _type == 'D':
            self._draw_from_message(msg)
        elif _type == 'Z':
            self._delete_from_message(msg)
        elif _type == 'T':
            self._draw_text_from_message(msg)
        elif _type == 'DR':
            self._drag_from_message(msg)

    # Here we draw an oval from the received message, taking the four received points
    # The points are the sections 1 to 4 of the message
    # The color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_oval_from_message(self, msg):

        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        item = self.drawing_area.create_oval(a, b, c, d, fill=self.Colors[color], width=0)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # Here we draw an oval from the received message, taking the four received points
    # The points are the sections 1 to 4 of the message
    # The color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_circle_from_message(self, msg):
        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        radius = math.sqrt((a-c)**2+(b-d)**2)/2
        x_center = (a + c) / 2
        y_center = (b + d) / 2
        item = self.drawing_area.create_oval(x_center-radius, y_center-radius, x_center+radius, y_center+radius,
                                             fill=self.Colors[color], width=0)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # ---------- DRAW LINE FROM MESSAGE----------
    # Here we draw a line from the received message, taking the four received points
    # The points are the sections 1 to 4 of the message
    # The color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_line_from_message(self, msg):
        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        item = self.drawing_area.create_line(a, b, c, d, fill=self.Colors[color], width=self.line_width)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # ---------- DRAW RECTANGLE FROM MESSAGE----------
    # Here we draw a rectangle from the received message, taking the four received points
    # The points are the sections 1 to 4 of the message
    # The color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_rectangle_from_message(self, msg):
        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        item = self.drawing_area.create_rectangle(a, b, c, d, fill=self.Colors[color], width=0)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # ---------- DRAW RECTANGLE FROM MESSAGE----------
    # Here we draw a rectangle from the received message, taking the four received points
    # The points are the sections 1 to 4 of the message
    # The color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_square_from_message(self, msg):
        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        radius = (c+d-a-b)/2
        item = self.drawing_area.create_rectangle(a, b, a+radius, b+radius, fill=self.Colors[color], width=0)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # ---------- ERASE ALL -------------------------
    # This message erases everything in the whiteboard!
    # This message also erases all logs in the server to avoid a memory leak
    def _draw_erase_from_message(self, msg):
        for s in msg:
            item = self.drawing_area.find_withtag(s)
            self.drawing_area.delete(item)

    # ---------- PENCIL    -------------------------
    # Here we have the pencil, it draws a line from the 4 points received
    # As with the others the points are sections 1 to 4 and color is section 5
    # Section 6 is the user who draw this object and section 7 is the ID we bind to this object
    def _draw_from_message(self, msg):
        a, b, c, d = float(msg[1]), float(msg[2]), float(msg[3]), float(msg[4])
        color = msg[5]
        # print('[Network]Received point: (%s, %s)' % (a, b))
        # print('[Canvas]Drawing lines')
        item = self.drawing_area.create_line(a, b, c, d, fill=self.Colors[color], width=self.line_width)
        self.drawing_area.itemconfig(item, tags=(msg[6], msg[7]))

    # ---------- TEXT    -------------------------
    # The text message is a little bit more complicated since the sections are more complex
    # Here we need to send the text plus a pair of coordinates we are putting the text into!
    # But the text can have spaces between them, that is why we use the join function here
    # And the coordinates are numbered as bellow, a and b refer to the two coordinates
    # color refers to the color of the text
    def _draw_text_from_message(self, msg):
        write, a, b, color = " ".join(msg[1:-5]), float(msg[-5]), float(msg[-4]), msg[-3]
        text_font = font.Font(family='Helvetica',
                              size=20, weight='bold', slant='italic')
        item = self.drawing_area.create_text(a, b, fill=self.Colors[color], font=text_font, text=write)
        self.drawing_area.itemconfig(item, tags=(msg[-2], msg[-1]))

    # -------------------- DRAG --------------------------------
    # Here we drag objects from a received drag message
    # The drag message structure is (DR, msg_identification, newposition1, newposition2, user)
    # So we use the part 2 and 3 to move, and the msg_identification to find the object on the board
    # All objects are tagged with their message identification, which allows us to find them this way
    def _drag_from_message(self, msg):
        a, b = msg[2], msg[3]
        item = self.drawing_area.find_withtag(msg[1])
        self.drawing_area.move(item, a, b)

    # -------------------- DELETE --------------------------------
    # Delete messages are from the format ("E", msg_identification)
    # So since every object is tagged with their message identification
    # We find them using this tag and delete it!
    def _delete_from_message(self, msg):
        item = self.drawing_area.find_withtag(msg[1])
        self.drawing_area.delete(item)