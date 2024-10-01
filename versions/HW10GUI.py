from tkinter import *  
import tkinter.filedialog 
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import glob
import os
from urllib.parse import urlencode 
import random
import string
import requests
import feedparser 

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry("700x500") # set the window siz
        self.title("The Holy Grail of RSS Feeds") # set window title

        # Define the font and size
        self.font = ("Helvetica", 18)
                     
        # create and place ScrolledText widget
        self.text = ScrolledText(self, height=20)
        self.text.grid(row=4, column=0, columnspan=3, padx=25, pady=5)
        
        # Submit search query 
        self.ok_button = Button(self, text="Start Search?", font=self.font, bg="blue", fg="yellow", command=self.search)
        #self.entry.bind("<ButtonRelease-1>", self.r) 
        self.ok_button.grid(row=2, column=0, padx=0, pady=5, sticky="e")

        # Cancel button 
        self.cancel_button = Button(self, text="No! Quit!", font=self.font, bg="yellow", fg="blue", command=self.quit_app)
        self.cancel_button.grid(row=2, column=2, padx=0, pady=5, sticky="w")

        # Label for search entry
        self.name_label = Label(self, text="What is your quest?", font=self.font)
        self.name_label.grid(row=0, column=0, columnspan=2, padx=25, pady=5, sticky="w")

        # Entry field for search
        self.entry_text_variable = StringVar() # need a StringVar for this!
        self.entry_text_variable.set("Enter search term")  
        self.name_entry = Entry(self, font=self.font, textvariable=self.entry_text_variable) # must use StringVar here!         
        self.name_entry.grid(row=1, column=0, columnspan=3, padx=25, pady=5, sticky="we")

    def quit_app(self):
        self.destroy()
        exit()

    def search(self):
        search_term = self.entry_text_variable.get()

        base_url = "https://news.google.com/rss/search"
        query_params = {
            'q': search_term
            # there could be other query parameters ...
        }

        rss_feed_url = f"{base_url}?{urlencode(query_params)}"
        #print("query:", rss_feed_url)

        # Google spoofer
        def random_name(): 
            '''Return a moderately long string with jumbled letters '''
            name_list = []
            length = random.randint(5, 12)
            for i in range(0, length):
                name_list.append(random.choice(string.ascii_letters))
            return "".join(name_list)

        r = requests.get(rss_feed_url, headers={'User-agent': random_name()})
        r.raise_for_status() # raise exception if request didn't work

        f = feedparser.parse(r.text) # parse into a feedparse dictionary
        list_of_entries = f.entries 

        for num_item, item in enumerate(list_of_entries): # num_item starts with 0
            #print(num_item+1, item["updated"], item["title"], item["link"], "\n") # start at counter at 1
            long_string=f"{num_item+1} {item["updated"]}\n{item["title"]}\n{item["link"]}\n\n"
            #long_string=num_item+1, item["updated"], item["title"], item["link"], "\n"
            # instead of print(), make a single string from all these and insert it into the text area.
            # to make a string you could use + or a f-string e.g. long_string = f"{num_item+1} {item['updated']} etc."
            # To insert into the Text widget use: self.text.insert(END, long_string)

            # Put some default text into the text area
            self.text.insert(INSERT, "" ) # insert text at cursor 
            self.text.insert(END, long_string)
            
app = App()
app.mainloop()