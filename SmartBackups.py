'''Smart Backup'''
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import filedialog
from PIL import Image, ImageTk
import time
from time import sleep
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from create_dump import get_registry_values
from post_dump import restore
from registry import get_reg, set_reg
from delete_old_files import delete_backups

# Initialize Logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger()
sys.stderr.write = logger.error
sys.stdout.write = logger.info

# Initializing UI, Creating Frames
class SmartBackup(tk.Tk):
    '''Database backup'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=10, weight="bold", slant="italic")
        self.minsize(width=250, height=200)
        self.geometry()
        self.title("Smart Backup")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, Settings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    '''Select option to backop or restore'''

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Would you like to backup or restore?",
                      font=controller.title_font)
        label.pack(side="top", fill="x", padx="50", pady=50)

        global folder_path

        def browse_button():
            global folder_path
            folder_path = filedialog.askopenfilename(initialdir = "/home/murunga/Desktop/Database-backups",title = "Select file",filetypes = (("SQL files","*.sql"),("all files","*.*")))
            return folder_path

        folder_path = StringVar()
        variable_folder = Label(self, textvariable=folder_path, font=controller.title_font)
        variable_folder.pack()


        def combine_functions(*functions):
            '''Combine two functions'''
            def combined_functions(*args, **kwargs):
                '''Combined functions'''
                for function in functions:
                    function(*args, **kwargs)
                return function
            return combined_functions

        def wait():
            '''Wait for a few seconds'''
            time.sleep(1)
        def run_backup():
            '''Run backup in the background'''
            try:
                threading.Thread(target=get_registry_values, daemon=True).start()
            except:
                print("Threading failed")

        # Scheduling function
        def schedule():
            '''Set an interval to keep checking if ports are open and restart if closed'''
            # threading.Thread(target=run_backup, daemon=True)
            scheduler = BackgroundScheduler()
            scheduler.add_job(run_backup, IntervalTrigger(seconds=120))
            scheduler.add_job(delete_backups, IntervalTrigger(hours=48))
            scheduler.start()

        settings_button = Button(self, text="Settings", command=combine_functions((lambda: controller.show_frame("Settings")),(lambda: wait())))
        settings_button.pack()

        backup_button = Button(self, text="Backup", command=combine_functions((lambda: controller.show_frame("PageOne")),(lambda: wait()) ,(lambda: run_backup()), (lambda: schedule())))
        backup_button.pack()

        chosen_db = get_reg('database')
        database = chosen_db[0]

        Restore_button = Button(self, text="Restore", command=combine_functions((lambda: browse_button()), (lambda: controller.show_frame("PageThree")) ,(lambda: restore(str(folder_path), str(database)))))
        Restore_button.pack()

class PageOne(tk.Frame):
    '''Monitoring occurs on this page'''

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(
            self, text="Backing up necessary files...\n\nSaving data...\n\n", font=controller.title_font)
        label.pack(side="top", fill="x",padx="10", pady=10)

        img = Image.open("server.gif")
        img = img.resize((200, 150), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self, image=img)
        panel.image = img
        panel.pack()

        label = Label(
            self, text="\nEverything looks okay!", font=controller.title_font)
        label.pack(side="top", fill="x",padx="10", pady=10)

        button = Button(self, text="Choose a different task?",
                        command=lambda: controller.show_frame("StartPage")).pack()

        button = Button(self, text="Quit Application",
                        command=lambda: controller.show_frame("PageTwo")).pack()

# User interface to quit program
class PageTwo(tk.Frame):
    '''Function to quit'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Are you sure you want to quit?\n\n",
                      font=controller.title_font)
        label.pack(side="top", fill="x", padx="50", pady=50)

        button = Button(self, text="No, Continue backing up data",
                        command=lambda: controller.show_frame("PageOne")).pack()

        quit_button = Button(
            self, compound=TOP, text="Yes, leave application", command=controller.destroy).pack()

class PageThree(tk.Frame):
    '''Function to quit'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Successfully rolled back database\n\n",
                      font=controller.title_font)
        label.pack(side="top", fill="x", padx="10", pady=10)

        img = Image.open("server.gif")
        img = img.resize((200, 150), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self, image=img)
        panel.image = img
        panel.pack()

        button = Button(self, text="Continue backing up data",
                        command=lambda: controller.show_frame("PageOne")).pack()

        quit_button = Button(
            self, compound=TOP, text="Yes, leave application", command=controller.destroy).pack()

class Settings(tk.Frame):
    '''Function to quit'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Enter database information below: \n\n",
                      font=controller.title_font)
        label.pack(side="top", fill="x", padx="10", pady=10)


        # Getting Database
        def get_database():
            '''Get database value'''
            database = databaseentry.get()
            return database

        databaselabel=Label(self, text="Enter database name: ")
        databaselabel.pack(side="top", fill="x", padx="20", pady=10)

        databaseentry = Entry(self)
        databaseentry.pack()

        # Getting database user
        def get_user():
            '''Get user name value'''
            user = userentry.get()
            return user

        userlabel=Label(self, text="Enter user name: ")
        userlabel.pack(side="top", fill="x", padx="20", pady=10)

        userentry = Entry(self)
        userentry.pack()

        # Getting database host
        def get_host():
            '''Get host/ip value'''
            host = hostentry.get()
            return host

        hostlabel=Label(self, text="Enter host/IP address")
        hostlabel.pack(side="top", fill="x", padx="20", pady=10)

        hostentry = Entry(self)
        hostentry.pack()

        # Getting database password
        def get_password():
            '''Get password value'''
            password = passwordentry.get()
            return password

        passwordlabel=Label(self, text="Enter password")
        passwordlabel.pack(side="top", fill="x", padx="20", pady=10)

        passwordentry = Entry(self, show="*")
        passwordentry.pack()

        # Save data to Registry
        def set_registry_data():
            '''Set settings values to registry'''
            db = get_database()
            database = [db]

            host = get_host()
            host = [host]

            user = get_user()
            user = [user]

            password = get_password()
            password = [password]

            return set_reg('database', database), set_reg('user', user), set_reg('ip/host', host), set_reg('password', password)
        
        savinglabel=Label(self)
        savinglabel.pack(side="top", fill="x", padx="20", pady=10)
        save_button = Button(self, text="Save new settings",
                        command=lambda: set_registry_data()).pack()
        
        spacinglabel=Label(self)
        spacinglabel.pack(side="top", fill="x", padx="30", pady=30)


        button = Button(self, text="Start Backing up data",
                        command=lambda: controller.show_frame("StartPage")).pack()
        quit_button = Button(
            self, compound=TOP, text="Quit application", command=controller.destroy).pack()


if __name__ == "__main__":
    app = SmartBackup()
    app.mainloop()