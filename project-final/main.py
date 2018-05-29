from tkinter import *

# -*- coding: utf-8 -*-

import modelet

import autocomplete

import autocorrect

FJALET_MODELE = {}

FJALET_MODELE_TUPLES = {}

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()

        model = modelet.merr_modelet()
        global FJALET_MODELE
        global FJALET_MODELE_TUPLES
        FJALET_MODELE = model[0]
        FJALET_MODELE_TUPLES = model[1]



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

    def update_list(self, *args):
        fjala = self.search_var.get()
        mundesite_e_fjales = autocorrect.kontrolloFjalen(fjala) #Shikojme nese fjala nuk eshte shkruar mire
        print(mundesite_e_fjales)
        if len(mundesite_e_fjales) > 1 and mundesite_e_fjales != '': #Vendosim fjalet qe mund te ishin korrekte ne vend te fjales gabim
            self.lbox.delete(0, END)
            for item in mundesite_e_fjales[0:5]:
                self.lbox.insert(END, item)
            return

        results = autocomplete.sugjero(fjala, FJALET_MODELE_TUPLES) #Marrim rezulatet e mundshme per nje fjale

        results = sorted(results, key=lambda res: res[1])[::-1] #bejm reverse listes sepse rezultatet i kemi nga me i vogli
        results = filter(lambda x: not (x[0] in autocomplete.alfabeti), results) #Largojm mundesite qe vijne si shkronja alfabeti
        results = list(results)

        self.lbox.delete(0, END)

        for item in results[0:10]:
            self.lbox.insert(END, item[0])


root = Tk()
root.title('Sugjero fjalen')
app = Application(master=root)
print ('Starting mainloop()')
app.mainloop()
