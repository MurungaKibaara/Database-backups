'''Smart Backup'''
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from PIL import Image, ImageTk
import time
from time import sleep
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from backup_to_db import excel_to_database
from write_to_backup import read_database

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
        for F in (StartPage, PageOne, PageTwo, PageThree):
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
        label = Label(self, text="Select the host and the server",
                      font=controller.title_font)
        label.pack(side="top", fill="x", padx="50", pady=50)


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
            time.sleep(2)
        def run_backup():
            '''Run backup in the background'''
            try:
                threading.Thread(target=read_database, daemon=True)
            except:
                print("Threading failed")


        # Scheduling function
        def schedule():
            '''Set an interval to keep checking if ports are open and restart if closed'''
            threading.Thread()
            scheduler = BackgroundScheduler()
            scheduler.add_job(read_database, IntervalTrigger(seconds=120))
            scheduler.start()

        backup_button = Button(self, text="Backup", command=combine_functions((lambda: controller.show_frame("PageOne")),(lambda: wait()) ,(lambda: run_backup()), (lambda: schedule())))
        backup_button.pack()

        Restore_button = Button(self, text="Restore", command=combine_functions((lambda: controller.show_frame("PageThree")),(lambda: wait()) ,(lambda: excel_to_database())))
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
        label.pack(side="top", fill="x", padx="50", pady=50)

        button = Button(self, text="Continue backing up data",
                        command=lambda: controller.show_frame("PageOne")).pack()

        quit_button = Button(
            self, compound=TOP, text="Yes, leave application", command=controller.destroy).pack()


if __name__ == "__main__":
    app = SmartBackup()
    app.mainloop()