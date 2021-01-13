#############################################################################
#                                                                           #
#                   ---Importing packages and libraries---                  #
#                                                                           #
#############################################################################
import tkinter as tk
from tkinter import ttk
from value_extractor import ValueExtractor
#from condition_loader import Loader

class MainFrame(tk.Frame):
    #Initiating class with making an empty frame, setting counters, and making a start page
    def __init__(self, master):
        #initiate a frame on the passed master
        tk.Frame.__init__(self, master)
        #setting counter of group conditions
        self.counter = -1
        #setting counter of fields(each line of a group condition)
        self.field_counter = 2
        #names of columns that will be used in conditioning
        self.columns_names = None
        #initiating a start page
        self.start_page()
    
    def start_page(self):
        '''Making a start page'''
        #tracker, trace that each line of condition should be added to which group
        self.tracker = {}
        #an empty frame that holds primary conditions
        self.prm_field_hldr = tk.Frame(self)
        self.prm_field_hldr.rowconfigure(0, weight = 1)
        self.prm_field_hldr.columnconfigure(0, weight = 1)
        #an empty frame that holds secondary conditions
        self.frm_field_hldr = tk.Frame(self)
        self.frm_field_hldr.rowconfigure(0, weight = 1)
        self.frm_field_hldr.columnconfigure(0, weight = 1)
        #title of the page
        self.tb2_title = tk.Label(self, text = 'Conditions defenition')
        #button that makes a new group of condition
        self.btn_add_condition = tk.Button(self, text = 'Add another condition', command = lambda: self.create_new_condition(self.new_field))
        #button that remove all group of conditions
        self.btn_remove_conditions = tk.Button(self, text = 'Remove all conditions', command = lambda: self.clearMainFrame(self.frm_field_hldr))
        #gridding above elements on the page
        self.tb2_title.grid(row = 0, column = 0, sticky = 'ns', padx = 5, pady = 5)
        self.prm_field_hldr.grid(row = 1, column = 0, columnspan = 5, sticky = 'nsew', padx = 5, pady = 5)
        self.btn_add_condition.grid(row = 2, column = 0, sticky = 'w', padx = 20, pady = 5)
        self.btn_remove_conditions.grid(row = 2, column = 0, sticky = 'w', padx = 160, pady = 5)
        self.frm_field_hldr.grid(row = 3, column = 0, columnspan = 5, sticky = 'nsew', padx = 5, pady = 5)
        #creating first group of condition
        self.create_primary_condition(self.primary_first_field)
        self.create_new_condition(self.new_field)

    def loader_page(self, list_of_primary_conditions, list_of_sec_conditions, c_titles):
        '''Clear the main page and load pre_writen conditions'''
        #list of pre_writen conditions
        plocond = list_of_primary_conditions
        locond = list_of_sec_conditions
        #list of columns titles
        column_titles = c_titles
        #tracker, trace that each line of condition should be added to which group
        self.tracker = {}
        #an empty frame that holds primary conditions
        self.prm_field_hldr = tk.Frame(self)
        self.prm_field_hldr.rowconfigure(0, weight = 1)
        self.prm_field_hldr.columnconfigure(0, weight = 1)
        #an empty frame that holds conditions
        self.frm_field_hldr = tk.Frame(self)
        self.frm_field_hldr.rowconfigure(0, weight = 1)
        self.frm_field_hldr.columnconfigure(0, weight = 1)
        #title of the page
        self.tb2_title = tk.Label(self, text = 'Conditions defenition')
        #button that makes a new group of condition
        self.btn_add_condition = tk.Button(self, text = 'Add another condition', command = lambda: self.create_new_condition(self.new_field))
        #button that remove all group of conditions
        self.btn_remove_conditions = tk.Button(self, text = 'Remove all conditions', command = lambda: self.clearMainFrame(self.frm_field_hldr))
        #gridding above elements on the page
        self.tb2_title.grid(row = 0, column = 0, sticky = 'ns', padx = 5, pady = 5)
        self.prm_field_hldr.grid(row = 1, column = 0, columnspan = 5, sticky = 'nsew', padx = 5, pady = 5)
        self.btn_add_condition.grid(row = 2, column = 0, sticky = 'w', padx = 20, pady = 5)
        self.btn_remove_conditions.grid(row = 2, column = 0, sticky = 'w', padx = 160, pady = 5)
        self.frm_field_hldr.grid(row = 3, column = 0, columnspan = 5, sticky = 'nsew', padx = 5, pady = 5)
        self.primary_condition_writer(plocond, column_titles)
        self.condition_writer(locond, column_titles)


    def create_primary_condition(self, field_func):
        '''Create a new group of condition'''
        self.field_counter = 0
        #frame that holds elements of a group of condition
        tb2_prm_frm = tk.Frame(self.prm_field_hldr)
        tb2_prm_frm.rowconfigure(0, weight = 1)
        tb2_prm_frm.columnconfigure([0,1,2,3], weight = 1)
        #button that adds a new field of conditions
        tb2_add_prm_field = tk.Button(tb2_prm_frm, name = str(self.counter), text = 'Add new field', command = lambda: self.new_field(tb2_prm_frm, PrimaryMaker, str(tb2_add_prm_field)))
        #tracker updating
        self.tracker[str(tb2_add_prm_field)] = self.field_counter
        #making new field of condition object(this line cause each group of condition initiate with one field of condition)
        tb2_pfield = field_func(tb2_prm_frm, PrimaryMakerFL, str(tb2_add_prm_field))
        #grid elements
        tb2_prm_frm.grid(row = 0, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)
        tb2_add_prm_field.grid(row = 0, column = 4, sticky = 'e', padx = 0, pady = 5)
        tb2_pfield.grid(row = 0, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)


    
    def create_new_condition(self, field_func):
        '''Create a new group of condition'''
        self.counter += 1
        self.field_counter = 2
        #frame that holds elements of a group of condition
        tb2_cond_frm = tk.Frame(self.frm_field_hldr)
        tb2_cond_frm.rowconfigure(0, weight = 1)
        tb2_cond_frm.columnconfigure([0,1,2,3], weight = 1)
        #button that adds a new field of conditions
        tb2_add_new_field = tk.Button(tb2_cond_frm, name = str(self.counter), text = 'Add new field', command = lambda: self.new_field(tb2_cond_frm, FieldMaker, str(tb2_add_new_field)))
        #tracker updating
        self.tracker[str(tb2_add_new_field)] = self.field_counter
        #making new field of condition object(this line cause each group of condition initiate with one field of condition)
        tb2_nfield = field_func(tb2_cond_frm, FieldMaker, str(tb2_add_new_field))
        #grid elements
        tb2_cond_frm.grid(row = self.counter, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)
        tb2_add_new_field.grid(row = 0, column = 0, sticky = 'w', padx = 10, pady = 5)
        tb2_nfield.grid(row = 1, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)

    
    def create_new_empty_condition(self):
        '''Create a new empty group of condition'''
        self.counter += 1
        self.field_counter = 1
        #frame that holds elements of a group of condition
        tb2_cond_frm = tk.Frame(self.frm_field_hldr)
        tb2_cond_frm.rowconfigure(0, weight = 1)
        tb2_cond_frm.columnconfigure([0,1,2,3], weight = 1)
        #button that adds a new field of conditions
        tb2_add_new_field = tk.Button(tb2_cond_frm, name = str(self.counter), text = 'Add new field', command = lambda: self.new_field(tb2_cond_frm, FieldMaker, str(tb2_add_new_field)))
        #tracker updating
        self.tracker[str(tb2_add_new_field)] = self.field_counter
        #grid elements
        tb2_cond_frm.grid(row = self.counter, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
        tb2_add_new_field.grid(row = 0, column = 0, sticky = 'ns', padx = 5, pady = 5)
        return tb2_cond_frm, str(tb2_add_new_field)


    def primary_first_field(self, master, field_class, button_name):
        """Creates new field"""
        #make a new field
        newfield = field_class(master, self.columns_names)
        newfield.rowconfigure(0, weight = 1)
        newfield.columnconfigure([0,1,2,3,4], weight = 1)
        #updating counter with the number of fields in current condition group(it finds that Add new field button of wich group condition is pressed)
        self.field_counter = self.tracker[button_name]
        #gridding elements
        newfield.grid(row = self.field_counter, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
        self.field_counter += 1
        #tracker updating
        self.tracker[button_name] = self.field_counter
        return newfield


    def new_field(self, master, field_class, button_name):
        """Creates new field"""
        #make a new field
        newfield = field_class(master, self.columns_names)
        newfield.rowconfigure(0, weight = 1)
        newfield.columnconfigure([0,1,2,3,4], weight = 1)
        #make remove button(this button removes line of condition next to it)
        tb2_remv_btn = tk.Button(newfield, text = '✕', font="TkDefaultFont 8 bold", width = 6, command = lambda: self.remove_field(newfield))
        #updating counter with the number of fields in current condition group(it finds that Add new field button of wich group condition is pressed)
        self.field_counter = self.tracker[button_name]
        #gridding elements
        newfield.grid(row = self.field_counter, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)
        tb2_remv_btn.grid(row = 0, column = 4, sticky = 'nsew', padx = 5, pady = 5)
        self.field_counter += 1
        #tracker updating
        self.tracker[button_name] = self.field_counter
        return newfield

    def prim_field_filler(self, master, field_class, button_name, elements, listOfColumnTitles, row_number):
        """Creates new field"""
        list_of_column_titles = listOfColumnTitles
        #make a new field
        newfield = field_class(master, elements, list_of_column_titles)
        newfield.rowconfigure(0, weight = 1)
        newfield.columnconfigure([0,1,2,3,4], weight = 1)
        if row_number != 0:
            #make remove button(this button removes line of condition next to it)
            tb2_remv_btn = tk.Button(newfield, text = '✕', font="TkDefaultFont 8 bold", width = 6, command = lambda: self.remove_field(newfield))
            tb2_remv_btn.grid(row = 0, column = 4, sticky = 'nsew', padx = 5, pady = 5)
        #updating counter with the number of fields in current condition group(it finds that Add new field button of wich group condition is pressed)
        self.field_counter = self.tracker[button_name]
        #gridding elements
        newfield.grid(row = self.field_counter, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
        self.field_counter += 1
        #tracker updating
        self.tracker[button_name] = self.field_counter
        return newfield

    def field_filler(self, master, field_class, button_name, elements, listOfColumnTitles):
        """Creates new field"""
        list_of_column_titles = listOfColumnTitles
        #make a new field
        newfield = field_class(master, elements, list_of_column_titles)
        newfield.rowconfigure(0, weight = 1)
        newfield.columnconfigure([0,1,2,3,4], weight = 1)
        #make remove button(this button removes line of condition next to it)
        tb2_remv_btn = tk.Button(newfield, text = '✕', font="TkDefaultFont 8 bold", width = 6, command = lambda: self.remove_field(newfield))
        #updating counter with the number of fields in current condition group(it finds that Add new field button of wich group condition is pressed)
        self.field_counter = self.tracker[button_name]
        #gridding elements
        newfield.grid(row = self.field_counter, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
        tb2_remv_btn.grid(row = 0, column = 4, sticky = 'nsew', padx = 5, pady = 5)
        self.field_counter += 1
        #tracker updating
        self.tracker[button_name] = self.field_counter
        return newfield

    def primary_condition_writer(self, primListOfConditions, listOfColumnNames):
        '''writes loaded primary condition on the page'''
        list_of_primary_conditions = primListOfConditions
        list_of_column_names = listOfColumnNames
        #check to see if there is any list of conditions
        if primListOfConditions:
            #Create a new empty group of condition
            self.field_counter = 1
            #frame that holds elements of a group of condition
            tb2_cond_frm = tk.Frame(self.prm_field_hldr)
            tb2_cond_frm.rowconfigure(0, weight = 1)
            tb2_cond_frm.columnconfigure([0,1,2,3], weight = 1)
            #button that adds a new field of conditions
            tb2_add_new_field = tk.Button(tb2_cond_frm, name = str(self.counter), text = 'Add new field', command = lambda: self.new_field(tb2_cond_frm, FieldMaker, str(tb2_add_new_field)))
            button_name = str(tb2_add_new_field)
            #tracker updating
            self.tracker[str(tb2_add_new_field)] = self.field_counter
            #grid elements
            tb2_cond_frm.grid(row = 0, column = 0, columnspan = 4, sticky = 'nsew', padx = 5, pady = 5)
            tb2_add_new_field.grid(row = 0, column = 0, sticky = 'ns', padx = 5, pady = 5)
            condition = list_of_primary_conditions[0][0]['condition']
            length = len(condition)
            i = 0
            while i < length:
                #making a list of each tuple of condition part
                line = list(condition[i])
                self.prim_field_filler(tb2_cond_frm, PrimaryLoader, button_name, line, list_of_column_names, i)
                i += 1

    def condition_writer(self, listOfConditions, listOfColumnNames):
        '''writes loaded condition on the page'''
        list_of_conditions = listOfConditions
        list_of_column_names = listOfColumnNames
        #check to see if there is any list of conditions
        if list_of_conditions:
            length1 = len(list_of_conditions)
            i = 0
            while i < length1:
                #make an empty frame for each group of conditions
                grp_frm, button_name = self.create_new_empty_condition()
                length2 = len(list_of_conditions[i])
                j = 0
                while j < length2:
                    #extracting condition part of condition dicts
                    condition = list_of_conditions[i][j]['condition']
                    length3 = len(condition)
                    k = 0
                    while k < length3:
                        #making a list of each tuple of condition part
                        line = list(condition[k])
                        #sending elements to the field_filler to wirte them on the fields
                        self.field_filler(grp_frm, Loader, button_name, line, list_of_column_names)
                        k += 1
                    #extracting action part of condition dicts
                    action = list_of_conditions[i][j]['action']
                    length4 = len(action)
                    z = 0
                    while z < length4:
                        #making a list of each tuple of action part
                        line = list(action[z])
                        #sending elements to the field_filler to wirte them on the fields
                        self.field_filler(grp_frm, Loader, button_name, line, list_of_column_names)
                        z += 1
                    j += 1
                i += 1

    def clearMainFrame(self, conditions_frame):
        '''Clear Main Frame from widgets'''
        # destroy all widgets from frame
        conditions_frame.destroy()
        self.counter = -1
        self.start_page()

    def clearForLoad(self):
        '''Clear the page and prepare it to load conditions'''
        self.prm_field_hldr.destroy()
        self.frm_field_hldr.destroy()
        self.columns_names = None
        self.counter = -1


    def remove_field(self, field):
        '''Remove field previous to it'''
        #destroy field
        field.destroy()

    def column_names(self, c_names):
        self.columns_names = c_names

    def primary_first_row_names(self):
        prim_cond = self.prm_field_hldr.winfo_children()
        #Extracting lines of considered group
        line_group = [elem for elem in prim_cond[0].winfo_children() if not isinstance(elem, tk.Button)]
        #Finding number of lines of considered group
        length = len(line_group)
        i = 0
        #Iterate over each extracted line of the group of condition
        while i < length:
            #Extracting elements on the considered line
            line_condition = line_group[i].winfo_children()
            line_condition[1].config(values = self.columns_names)
            line_condition[3].config(values = self.columns_names)
            i += 1


    def first_row_names(self):
        groups_on_MF = [child for child in self.frm_field_hldr.winfo_children()]
        #Finding number of group of conditions on Main Frame
        length = len(groups_on_MF)
        i = 0
        #Iterate over each group of conditions to find elements and exctracting values
        while i < length:
            #Taking one group of condition on Main Frame to extract it's elements
            condition_group = groups_on_MF[i]
            #Extracting lines of considered group
            line_group = [elem for elem in condition_group.winfo_children() if not isinstance(elem, tk.Button)]
            #Finding number of lines of considered group
            length2 = len(line_group)
            j = 0
            #Iterate over each extracted line of the group of condition
            while j < length2:
                #Extracting elements on the considered line
                line_condition = line_group[j].winfo_children()
                line_condition[1].config(values = self.columns_names)
                line_condition[3].config(values = self.columns_names)
                j += 1
            i += 1
        
    
    def final(self):
        '''Finalize and save writen conditions to a text file'''
        all_primary_conditions = ValueExtractor(self.prm_field_hldr).condition_list_maker()
        all_secondary_conditions = ValueExtractor(self.frm_field_hldr).condition_list_maker()
        return all_primary_conditions, all_secondary_conditions

    def create_empty_frame(self):
        empty_frm = tk.Frame(self)
        empty_frm.grid(row = self.counter, column = 0, columnspan = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.counter += 1
        return empty_frm


class PrimaryMakerFL(tk.Frame):

    def __init__(self, master, c_names):
        tk.Frame.__init__(self, master)
        #names of columns that will be used in conditioning
        self.columns = c_names
        #create first line
        self.create_first_line_widgets()

    def create_first_line_widgets(self):
        '''Creates fields to write conditions on them'''
        #first element of conidition line
        tb2_prm_condition = ttk.Combobox(self)
        tb2_prm_condition.set('if')
        tb2_prm_condition.configure(state = 'disabled')
        #second element of conidition line(this is a phrase entered by user)
        self.tb2_prm_first_phrase = ttk.Combobox(self, values = self.columns)
        #third element of conidition line(this is a comparator)
        self.tb2_prm_logical_comparator = ttk.Combobox(self, values = ['in', 'not in'])
        #forth element of conidition line(this is a phrase entered by user)
        self.tb2_prm_second_phrase = ttk.Combobox(self, values = self.columns)
        #grid elments
        tb2_prm_condition.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)

class PrimaryMaker(tk.Frame):

    def __init__(self, master, c_names):
        tk.Frame.__init__(self, master)
        #names of columns that will be used in conditioning
        self.columns = c_names
        #create first line
        self.create_rest_lines_widgets()

    def create_rest_lines_widgets(self):
        '''Creates fields to write conditions on them'''
        #first element of conidition line
        tb2_prm_condition = ttk.Combobox(self)
        tb2_prm_condition.set('and')
        tb2_prm_condition.configure(state = 'disabled')
        #second element of conidition line(this is a phrase entered by user)
        self.tb2_prm_first_phrase = ttk.Combobox(self, values = self.columns)
        #third element of conidition line(this is a comparator)
        self.tb2_prm_logical_comparator = ttk.Combobox(self, values = ['in', 'not in'])
        #forth element of conidition line(this is a phrase entered by user)
        self.tb2_prm_second_phrase = ttk.Combobox(self, values = self.columns)
        #grid elments
        tb2_prm_condition.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_prm_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)


class FieldMaker(tk.Frame):

    def __init__(self, master, c_names):
        tk.Frame.__init__(self, master)
        #names of columns that will be used in conditioning
        self.columns = c_names
        #create a line of condition
        self.create_line_widgets()


    def update_combos(self, event):
        value = event.widget.get()
        if value == 'else':
            self.tb2_cond_first_phrase.set('')
            self.tb2_cond_first_phrase.configure(state = 'disabled')
            self.tb2_logical_comparator.set('')
            self.tb2_logical_comparator.configure(state = 'disabled')
            self.tb2_cond_second_phrase.set('')
            self.tb2_cond_second_phrase.configure(state = 'disabled')
        elif value == 'then':
            self.tb2_cond_first_phrase.configure(state = 'normal')
            self.tb2_logical_comparator.set('=')
            self.tb2_logical_comparator.configure(state = 'disabled')
            self.tb2_cond_second_phrase.configure(state = 'normal')
        else:
            self.tb2_cond_first_phrase.configure(state = 'normal')
            self.tb2_logical_comparator.set('')
            self.tb2_logical_comparator.configure(state = 'normal')
            self.tb2_cond_second_phrase.configure(state = 'normal')

    def create_line_widgets(self):
        '''Creates fields to write conditions on them'''
        #first element of conidition line(this could be either a condition or an action)
        tb2_condition_or_action = ttk.Combobox(self, values = ['if', 'elif', 'else', 'then', 'and', 'not and', 'or', 'not or'])
        tb2_condition_or_action.bind('<<ComboboxSelected>>', self.update_combos)
        #second element of conidition line(this is a phrase entered by user)
        self.tb2_cond_first_phrase = ttk.Combobox(self, values = self.columns)
        #third element of conidition line(this is a comparator)
        self.tb2_logical_comparator = ttk.Combobox(self, values = ['gt', 'ge', 'eq', 'lt', 'le', 'in', 'not in'])
        #forth element of conidition line(this is a phrase entered by user)
        self.tb2_cond_second_phrase = ttk.Combobox(self, values = self.columns)
        #grid elments
        tb2_condition_or_action.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_cond_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_cond_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)



class PrimaryLoader(tk.Frame):

    def __init__(self, master, elements, column_titles):
        tk.Frame.__init__(self, master)
        self.list_of_elements = elements
        self.list_of_column_titles = column_titles
        self.line_writer()

    # def set_state(self, value_of_combo):
    #     if value_of_combo == 'else':
    #         self.tb2_cond_first_phrase.set('')
    #         self.tb2_cond_first_phrase.configure(state = 'disabled')
    #         self.tb2_logical_comparator.set('')
    #         self.tb2_logical_comparator.configure(state = 'disabled')
    #         self.tb2_cond_second_phrase.set('')
    #         self.tb2_cond_second_phrase.configure(state = 'disabled')
    #     elif value_of_combo == 'then':
    #         self.tb2_logical_comparator.configure(state = 'disabled')

    def line_writer(self):
        '''Creates fields and writes loaded pre-writen conditions on them'''
        #first element of conidition line(this could be either a condition or an action)
        tb2_condition = ttk.Combobox(self, values = ['if', 'and'])
        #set the first element of condition line to the first element of loaded line
        tb2_condition.set(self.list_of_elements[0])
        tb2_condition.configure(state = 'disabled')
        #second element of conidition line(this is a phrase entered by user)
        tb2_cond_first_phrase = ttk.Combobox(self, values = self.list_of_column_titles)
        #set the second element of condition line to the second element of loaded line
        tb2_cond_first_phrase.set(self.list_of_elements[1])
        #third element of conidition line(this is a comparator)
        tb2_logical_comparator = ttk.Combobox(self, values = ['in', 'not in'])
        #set the third element of condition line to the third element of loaded line
        tb2_logical_comparator.set(self.list_of_elements[2])
        #forth element of conidition line(this is a phrase entered by user)
        tb2_cond_second_phrase = ttk.Combobox(self, values = self.list_of_column_titles)
        #set the forth element of condition line to the forth element of loaded line
        tb2_cond_second_phrase.set(self.list_of_elements[3])
        ##self.set_state(self.list_of_elements[0])

        #grid elments
        tb2_condition.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        tb2_cond_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        tb2_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        tb2_cond_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)


    
class Loader(tk.Frame):

    def __init__(self, master, elements, column_titles):
        tk.Frame.__init__(self, master)
        self.list_of_elements = elements
        self.list_of_column_titles = column_titles
        self.line_writer()

    def update_combos(self, event):
        value = event.widget.get()
        if value == 'else':
            self.tb2_cond_first_phrase.set('')
            self.tb2_cond_first_phrase.configure(state = 'disabled')
            self.tb2_logical_comparator.set('')
            self.tb2_logical_comparator.configure(state = 'disabled')
            self.tb2_cond_second_phrase.set('')
            self.tb2_cond_second_phrase.configure(state = 'disabled')
        elif value == 'then':
            self.tb2_cond_first_phrase.configure(state = 'normal')
            self.tb2_logical_comparator.set('=')
            self.tb2_logical_comparator.configure(state = 'disabled')
            self.tb2_cond_second_phrase.configure(state = 'normal')
        else:
            self.tb2_cond_first_phrase.configure(state = 'normal')
            self.tb2_logical_comparator.set('')
            self.tb2_logical_comparator.configure(state = 'normal')
            self.tb2_cond_second_phrase.configure(state = 'normal')

    def set_state(self, value_of_combo):
        if value_of_combo == 'else':
            self.tb2_cond_first_phrase.set('')
            self.tb2_cond_first_phrase.configure(state = 'disabled')
            self.tb2_logical_comparator.set('')
            self.tb2_logical_comparator.configure(state = 'disabled')
            self.tb2_cond_second_phrase.set('')
            self.tb2_cond_second_phrase.configure(state = 'disabled')
        elif value_of_combo == 'then':
            self.tb2_logical_comparator.configure(state = 'disabled')

    def line_writer(self):
        '''Creates fields and writes loaded pre-writen conditions on them'''
        #first element of conidition line(this could be either a condition or an action)
        tb2_condition_or_action = ttk.Combobox(self, values = ['if', 'elif', 'else', 'then', 'and', 'not and', 'or', 'not or'])
        tb2_condition_or_action.bind('<<ComboboxSelected>>', self.update_combos)
        #set the first element of condition line to the first element of loaded line
        tb2_condition_or_action.set(self.list_of_elements[0])
        #second element of conidition line(this is a phrase entered by user)
        self.tb2_cond_first_phrase = ttk.Combobox(self, values = self.list_of_column_titles)
        #set the second element of condition line to the second element of loaded line
        self.tb2_cond_first_phrase.set(self.list_of_elements[1])
        #third element of conidition line(this is a comparator)
        self.tb2_logical_comparator = ttk.Combobox(self, values = ['gt', 'ge', 'eq', 'lt', 'le', 'in', 'not in'])
        #set the third element of condition line to the third element of loaded line
        self.tb2_logical_comparator.set(self.list_of_elements[2])
        #forth element of conidition line(this is a phrase entered by user)
        self.tb2_cond_second_phrase = ttk.Combobox(self, values = self.list_of_column_titles)
        #set the forth element of condition line to the forth element of loaded line
        self.tb2_cond_second_phrase.set(self.list_of_elements[3])
        self.set_state(self.list_of_elements[0])

        #grid elments
        tb2_condition_or_action.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_cond_first_phrase.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_logical_comparator.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.tb2_cond_second_phrase.grid(row = 0, column = 3, sticky = 'nsew', padx = 5, pady = 5)

