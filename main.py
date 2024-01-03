import customtkinter as ctk
from customtkinter import *
import tkinter as tk
from tkinter import *
import os
from scraper import *

changerate = []


def change(ticker):

    cur.execute(f"SELECT * FROM charts Where ticker = '{ticker}' ORDER BY date DESC limit 2 ")

    data = cur.fetchall()

    all_data = []

    for row in data:
        all_data.append(row[4])

    print(all_data)

    yesterday = all_data[1]
    today = all_data[0]

    change = today / yesterday
    percent = change * 100
    percent = percent - 100
    percent = round(percent, 2)
    changerate.append(percent)

    print("Today's change is " + str(percent)+"%")


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# class Tabview(CTkTabview):
#     def __init__(self):
#         super().__init__()

#         self.add("Trending")
#         self.add("Charts")
#         self.add("Track")
#         self.tab("Trending").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
#         self.tab("Charts").grid_columnconfigure(0, weight=1)

class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Stock Analyzer 1.0")
        self.geometry(f"{1250}x{800}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.main_frame = ctk.CTkFrame(self, width = 1100, height= 750)
        self.main_frame.grid(row = 0, column = 1, padx = 20, pady = 20, sticky="nsew" )
        self.main_frame.grid_rowconfigure(4, weight=1)

        #generates all tickers historical data
        self.Generatebutton = CTkButton(self.sidebar_frame, text = 'Generate', command = Generate )
        self.Generatebutton.grid(padx=20, pady=20)

        #does a 1 day update to csv file
        self.Updatebutton = CTkButton(self.sidebar_frame, text = 'Update', command= Update)
        self.Updatebutton.grid(padx=20, pady=20)

        #adds tickers to the list
        self.addticker = CTkEntry(self.sidebar_frame, placeholder_text='Add your Tickers')
        self.addticker.grid(padx=20, pady=20)
        self.addButton = CTkButton(self.sidebar_frame, text = 'Add', command=lambda: addTicker(ticker = self.addticker.get()))
        self.addButton.grid(padx=20, pady=20)

        #Gets the change % for the previous day
        self.getratechange = CTkEntry(self.main_frame, placeholder_text='Rate of Change')
        self.getratechange.grid(column= 0,padx=20, pady=20)
        self.getratechangebtn = CTkButton(self.main_frame, text = 'Search', command=lambda: change(ticker = self.getratechange.get()))
        self.getratechangebtn.grid(row=0, column = 1, padx=20, pady=20) 
        self.getratechangelabel = CTkLabel(self.main_frame, text = changerate )
        self.getratechangelabel.grid(row=1, column = 0, padx=20, pady=20)

        #adds tickers to the list
        self.gettable = CTkEntry(self.sidebar_frame, placeholder_text='Search your Tickers')
        self.gettable.grid(padx=20, pady=20)
        self.gettablebtn = CTkButton(self.sidebar_frame, text = 'Search', command=lambda: fetch_table(ticker = self.gettable.get()))
        self.gettablebtn.grid(padx=20, pady=20)

        self.canvas = CTkCanvas(self.main_frame)
        self.canvas.grid(padx=20, pady=20)

        #Treeview tables

        # #tabview
        # self.tabview = Tabview(self)
        # self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()