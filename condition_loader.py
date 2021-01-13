import tkinter as tk
from tkinter import ttk
#from field_maker1 import MainFrame as mf

class Loader(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.conditions_list = [
            [
                {
                    'condition': [('if', 'this', 'comparator', 'that'), ('and', 'this', 'comparator', 'that')],
                    'action': [('then', 'do', 'comparator', 'something')]
                },
                {
                    'condition': [('elif', 'this', 'comparator', 'that')],
                    'action' : [('then', 'do', 'comparator', 'something'), ('and', 'do', 'comparator', 'something')]
                }
            ]]
        self.condition_writer()

    def condition_writer(self):
        if self.conditions_list:
            length1 = len(self.conditions_list)
            i = 0
            while i < length1:
                length2 = len(self.conditions_list[i])
                j = 0
                while j < length2:
                    condition = self.conditions_list[i][j]['condition']
                    length3 = len(condition)
                    k = 0
                    while k < length3:
                        line = list(condition[k])
                        print(line)
                        self.line_writer(line)
                        k += 1
                    action = self.conditions_list[i][j]['action']
                    length4 = len(action)
                    z = 0
                    while z < length4:
                        line = list(action[z])
                        print(line)
                        self.line_writer(line)
                        z += 1
                    j += 1
                i += 1
                #mf.create_new_condition(self, mf.new_field)

    def line_writer(self, list_of_elements):
        #first element of conidition line(this could be either a condition or an action)
        tb2_condition_or_action = ttk.Combobox(self, values = list_of_elements[0])
        #second element of conidition line(this is a phrase entered by user)
        tb2_cond_first_phrase = tk.Entry(self)
        tb2_cond_first_phrase.insert('end', list_of_elements[1])
        #third element of conidition line(this is a comparator)
        tb2_logical_comparator = ttk.Combobox(self, values = list_of_elements[2])
        #forth element of conidition line(this is a phrase entered by user)
        tb2_cond_second_phrase = tk.Entry(self)
        tb2_cond_second_phrase.insert('end', list_of_elements[3])

        #grid elments
        tb2_condition_or_action.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        tb2_cond_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        tb2_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        tb2_cond_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)