from tkinter import *
import tkinter.font as font

class ExternalWindows:

    def __init__(self):
        pass

    # Default ip and port for debbuging
    _IP = "127.0.0.1"
    _Port = 5000
    # Text for the drawing text part!
    _Text = "WOW"
    _Nickname = "lol"



    # This temporary variable is used to get any other things we might need from the user
    # A little bit confusing but it works
    _Temp = ""

    #This method is used to show error boxes
    #Everytime an error message we show a box with the given message
    @classmethod
    def show_error_box(cls, msg):
        master = Tk()
        Label(master, text= msg).grid(row=0)
        Button(master, text='OK', command= master.destroy ).grid(row=1,  pady=4)
        master.mainloop()

    #This is the method that is used to get the ip and the port from the user!
    #It sets the protected class variable _Ip and _port to the values given by our user
    #This value is set by inputing the value in the widgets
    @classmethod
    def getValuesFromUser(cls):

        def show_entry_fields():
            try:
                cls._IP = e1.get()
                cls._Port = int(e2.get())
            except:
                pass
            master.destroy()


        def exit_program():
            exit()

        master = Tk()
        Label(master, text="Please type the host information").grid(row=0)
        Label(master, text="IP:").grid(row=1)
        Label(master, text="Port:").grid(row=2)

        e1 = Entry(master)
        e2 = Entry(master)

        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)

        # Button(master,text='Start',command=master.quit).grid(row=3,column=1,sticky=W,pady=4)
        Button(master, text='Set', command=show_entry_fields).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='Exit Program', command=exit_program).grid(row=4, column=0, sticky=W, pady=4)
        master.mainloop()

        cls.check_ip_and_port()


    @classmethod
    def check_ip_and_port(cls):

        expression = r"^(?=.*[^\.]$)((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.?){4}$"
        if re.search(expression, cls._IP) is None:
            cls.show_error_box("Please type a valid IP address")
            cls.getValuesFromUser()

        if (type(cls._Port) != int or cls._Port <= 1024 or cls._Port > 50000):
            cls.show_error_box("Please type a valid port number")
            cls.getValuesFromUser()

        print("Information received IP: {} Port: {}".format(cls._IP, cls._Port))


    #Method for getting text from user
    #This is used to print the text on the drawing board!
    @classmethod
    def get_text_from_user(cls):

        def get_text():
            temp = e1.get()
            master.destroy()
            if( "Ø" in temp):
                cls.show_error_box("Invalid character in expression")
            else:
                cls._Text = temp



        master = Tk()
        Label(master, text="What do you want to write?").grid(row=0)
        e1 = Entry(master)
        Label(master, text="Text: ").grid(row=1)
        e1.grid(row=1, column=1)

        Button(master, text='Set', command=get_text).grid(row=2, column=0, sticky=W, pady=4)
        master.mainloop()

    #This class is used to retrieve the user's selected nickname
    @classmethod
    def get_nickname_from_user(cls):

        def get_text():
            try:
                cls._Nickname = e1.get()
            except:
                pass
            master.destroy()



        master = Tk()
        Label(master, text="Choose a Nickname").grid(row=0)
        e1 = Entry(master)
        Label(master, text="Text: ").grid(row=1)
        e1.grid(row=1, column=1)

        Button(master, text='Set', command=get_text).grid(row=2, column=0, sticky=W, pady=4)
        Button(master, text='Exit', command= exit).grid(row=2, column=0, pady=4)
        master.mainloop()

        cls.check_nickname()

    @classmethod
    def check_nickname(cls):

        if (len(cls._Nickname) > 6):
            ExternalWindows.show_error_box("Please choose a shorter nickname. 6 characters long")
            cls.get_nickname_from_user()

        expression = r"^[a-zA-Z]+$"
        if re.search(expression, cls._Nickname) is None:
            cls.show_error_box("Only letters")
            cls.get_nickname_from_user()

    @classmethod
    def get_anything_from_user(cls, msg):

        def get_text():
            cls._Temp = e1.get()
            master.destroy()

        master = Tk()
        Label(master, text = msg).grid(row=0)
        e1 = Entry(master)
        Label(master, text="Text: ").grid(row=1)
        e1.grid(row=1, column=1)

        Button(master, text='Set', command=get_text).grid(row=2, column=0, sticky=W, pady=4)
        master.mainloop()

    #Return methods for the protected variables!
    @classmethod
    def return_ip(cls):
        return cls._IP

    @classmethod
    def return_port(cls):
        return cls._Port

    @classmethod
    def return_text(cls):
        return cls._Text

    @classmethod
    def return_nickname(cls):
        return cls._Nickname

    @classmethod
    def return_temp(cls):
        return cls._Temp

if __name__ == '__main__':

    ExternalWindows.getValuesFromUser()
    print(ExternalWindows.return_ip())

    ExternalWindows.get_nickname_from_user()
    print(ExternalWindows._Nickname)