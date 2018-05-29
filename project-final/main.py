from Tkinter import *

# First create application class
"""AUTOCOMPLETE -
This file contains the process where we train our predictive models, Also
helpful are the load_models and save_models functions.
"""
# -*- coding: utf-8 -*-

import modelet

import autocomplete

WORDS_MODEL = {}

WORD_TUPLES_MODEL = {}

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()

        model = modelet.merr_modelet()
        global WORDS_MODEL
        global WORD_TUPLES_MODEL
        WORDS_MODEL = model[0]
        WORD_TUPLES_MODEL = model[1]



    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        #self.search_var.trace("w", self.update_list)
        self.entry = Entry(self, textvariable=self.search_var, width=50)
        self.button = Button(self, text="Sugjero", background="#009688", foreground="white", command=self.update_list)
        self.lbox = Listbox(self, width=45, height=15)

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.button.grid(row=0, column=1, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self, *args):
        name = self.search_var.get()
        results = []
        for letter in autocomplete.alphabet:
            results = results + autocomplete.sugjero(name, letter, 10, WORD_TUPLES_MODEL)

        results = sorted(results, key=lambda res: res[1])[::-1]
        results = filter(lambda x: not (x[0] in autocomplete.alphabet), results)

        self.lbox.delete(0, END)

        for item in results:
            self.lbox.insert(END, item[0])


root = Tk()
root.title('Sugjero fjalen')
app = Application(master=root)
print ('Starting mainloop()')
app.mainloop()
