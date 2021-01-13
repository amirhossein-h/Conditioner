#############################################################################
#                                                                           #
#                   ---Importing packages and libraries---                  #
#                                                                           #
#############################################################################
import json
import pickle
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, Scrollbar
import pandas as pd
import os
from field_maker1 import MainFrame
from data_organizer import Organizer
from data_organizer import Manipulator, final_function
from condition_executer import mainFunction, primaryFunction

from pandastable import Table
import matplotlib
import matplotlib.pyplot as plt

#############################################################################
#                                                                           #
#                       ---Functions defenitions---                         #
#                                                                           #
#############################################################################

#creating a data holder object
data_holder = Organizer()

def reader(f_address, skiprows = 4, header = [0,1]):
        address = os.path.join(f_address)
        table = pd.read_table(address, skiprows = skiprows, header = header, engine = 'python')
        new_header = [' '.join(tups) for tups in table.columns]
        new_header = [i.strip() for i in new_header]
        return new_header

#Open File
list_of_files_paths = []
titles = []
def open_file():
    """Open a file for editing."""
    global list_of_files_paths
    global titles
    #storing files path on variable filepath
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        multiple = True
    )
    #check to see if there is any path
    if not filepath:
        return
    list_of_files_paths = list(filepath)
    #delete previous file names on chosen files list
    tb1_chsn_files.delete(0, 'end')
    #delete previous elements on available columns list
    tb1_avbl_cols.delete(0, 'end')
    #delete previous elements on chosen columns list
    tb1_chsn_cols.delete(0, 'end')
    #delete previous values on Old Name list
    tb1_old_list.delete(0, 'end')
    #delete previous values on New Name list
    tb1_new_list.delete(0, 'end')
    #
    tb1_header_column.delete(0, 'end')
    #
    tb1_body_column.delete(0, 'end')
    # #delete previous elements on all final columns
    # tb1_all_for_final.delete(0, 'end')
    # #delete previous elements on chosen final columns
    # tb1_chosen_for_final.delete(0, 'end')
    #clearing mainframe(Conditions Tab)
    mainframe.clearForLoad()
    mainframe.start_page()
    #adding files name to the chosen files list
    for path in filepath:
        tb1_chsn_files.insert('end', str(os.path.basename(path)))
    #selecting first path
    path = filepath[0]

    #reading columns titles
    titles = reader(path)
    #adding columns title to available columns list
    for title in titles:
        tb1_avbl_cols.insert('end', str(title))
    #setting window title
    window.title(f"Conditions Maker App - {filepath}")

def files_list():
    global list_of_files_paths
    return list_of_files_paths

#Select all items on available columns list
def select_all(c1, c2):
    """Select all items in the list box"""
    for item in c1.get(0, 'end'):
        c2.insert('end', item)
        c1.delete(0, 'end')
#Select highlighted item on available columns list
def select_one(c3, c4):
    """Select one item in the list box"""
    choosen_item_idx = c3.curselection()
    choosen_item_elem = c3.get(choosen_item_idx[0])
    c4.insert('end', choosen_item_elem)
    c3.delete(choosen_item_idx[0])

#Deselect all columns on chosen columns list
def deselect_all(c5, c6):
    """Deselect all items in the list box"""
    for item in c6.get(0, 'end'):
        c5.insert('end', item)
        c6.delete(0, 'end')
#Deselect highlighted item on chosen columns list
def deselect_one(c7, c8):
    """Deselect one item in the list box"""
    choosen_item_idx = c8.curselection()
    choosen_item_elem = c8.get(choosen_item_idx[0])
    c7.insert('end', choosen_item_elem)
    c8.delete(choosen_item_idx[0])

#List to store confirmed columns
confirmed_col = []
#Dict to store changed names
new_name = {}
#List that stores new columns names that add by user
new_columns = []
#Confirm chosen column. Passing chosen columns to the Combobox for renaming
def confirm_col(chosen_columns):
    global confirmed_col
    global new_columns
    global new_name
    new_columns = []
    #delete previous values on Old Name list
    tb1_old_list.delete(0, 'end')
    #delete previous values on New Name list
    tb1_new_list.delete(0, 'end')
    #
    tb1_header_column.delete(0, 'end')
    #
    tb1_body_column.delete(0, 'end')
    # #delete previous elements on all final columns
    # tb1_all_for_final.delete(0, 'end')
    # #delete previous elements on chosen final columns
    # tb1_chosen_for_final.delete(0, 'end')
    #clear new_name dict
    new_name = {}
    #put values of Chosen columns list to confirmed coloumn
    confirmed_col = list(chosen_columns.get(0, 'end'))
    #set values of confirmed columns Combobox
    tb1_slct_col.config(values = confirmed_col)
    #set text of Combobox
    tb1_slct_col.set('Select to change')

#Rename selected column
def rename_col():
    global new_name
    #taking index of selected item
    selected_idx = tb1_slct_col.current()
    #setting selected item as the key of new_name dict and it's new name as the value new_name dict
    new_name[str(confirmed_col[selected_idx])] = str(tb1_new_name.get())
    #put the selected item to Old Name tk-list
    tb1_old_list.insert('end', confirmed_col[selected_idx])
    #put the new name of selected item to New Name tk-list
    tb1_new_list.insert('end', new_name[str(confirmed_col[selected_idx])])
    #clearing new name tk-entry
    tb1_new_name.delete(0, 'end')
    #setting text of tk-combobox
    tb1_slct_col.set('Select to change')

#Adding new column name
def add_new_col():
    global new_columns
    #taking new column name from tk-entry
    new_col = str(tb1_add_new_col.get())
    #append name to new_columns list
    new_columns.append(str(new_col))
    #add new name to the Old Name tk-list
    tb1_old_list.insert('end', new_col)
    #add new name to the New Name tk-list
    tb1_new_list.insert('end', new_col)
    #clear tk-entry
    tb1_add_new_col.delete(0, 'end')
#Remove selected item from both Old or New name tk-lists
def remove_chosen_col():
    global new_columns
    global new_name
    if tb1_old_list.curselection():
        rmv_idx = tb1_old_list.curselection()[0]
        #remove from new_columns if it is there
        if tb1_old_list.get(rmv_idx) in new_columns:
            new_columns.remove(tb1_old_list.get(rmv_idx))
        #remove from new_name if it is there
        elif tb1_old_list.get(rmv_idx) in new_name.keys():
            del new_name[str(tb1_old_list.get(rmv_idx))]
        tb1_old_list.delete(rmv_idx)
        tb1_new_list.delete(rmv_idx)
    elif tb1_new_list.curselection():
        rmv_idx = tb1_new_list.curselection()[0]
        #remove from new_columns if it is there
        if tb1_new_list.get(rmv_idx) in new_columns:
            new_columns.remove(tb1_new_list.get(rmv_idx))
        #remove from new_name if it is there
        elif tb1_new_list.get(rmv_idx) in new_name.values():
            del new_name[str(tb1_old_list.get(rmv_idx))]
        tb1_old_list.delete(rmv_idx)
        tb1_new_list.delete(rmv_idx)
    

#Confirm defined condition and formatting them in the way that is used in !!!!! function
def finalize():
    global new_columns
    global new_name
    global titles
    #make list of all available columns
    all_columns = titles
    #make list of columns that are not chosen
    columns_to_delete = [c for c in all_columns if c not in confirmed_col]
    #pass list of added columns, not chosen columns and new names to the !!!!!! method of Mnipulator class to build new table
    #Manipulator().reconstructor(new_columns, columns_to_delete, new_name)
    temp_header = [elem for elem in all_columns if elem not in columns_to_delete]
    for k, v in new_name.items():
        if k in temp_header:
            elem_idx = temp_header.index(k)
            del temp_header[elem_idx]
            temp_header.insert(elem_idx, v)
    new_header = temp_header + new_columns
    return new_header, new_columns, columns_to_delete, new_name

def columnNames():
    #make list of all available columns
    header_titles, n_column, _,_ = finalize()
    mainframe.column_names(header_titles)
    mainframe.primary_first_row_names()
    mainframe.first_row_names()
    #
    tb1_header_column.delete(0, 'end')
    #
    tb1_body_column.delete(0, 'end')
    tb1_header_column.config(values = n_column)
    tb1_body_column.config(values = n_column)
    # tb1_all_for_final.delete(0, 'end')
    # tb1_chosen_for_final.delete(0, 'end')
    # for item in header_titles:
    #     tb1_all_for_final.insert('end', item)



#Load File
def load_set_up_file():
    """Load a pre-writen condition"""
    global list_of_files_paths
    global titles
    global confirmed_col
    global new_columns
    global new_name
    #storing files path on variable filepath
    filepath = askopenfilename(
        filetypes = [("Pickle Files", "*.pickle"), ("All Files", "*.*")]
    )
    #check to see if any file has been chosen
    if not filepath:
        return
    else:
        list_of_files_paths = []
        titles = []
        confirmed_col = []
        new_columns = []
        new_name.clear()
        tb1_chsn_files.delete(0, 'end')
        tb1_avbl_cols.delete(0, 'end')
        tb1_chsn_cols.delete(0, 'end')
        tb1_slct_col.delete(0, 'end')
        tb1_old_list.delete(0, 'end')
        tb1_new_list.delete(0, 'end')
        #
        tb1_header_column.delete(0, 'end')
        #
        tb1_body_column.delete(0, 'end')
        # tb1_all_for_final.delete(0, 'end')
        # tb1_chosen_for_final.delete(0, 'end')
        #open chosen file as a pickle
        with open(filepath, 'rb') as infile:
            set_up_file = pickle.load(infile)
            #clear mainframe
            mainframe.clearForLoad()
            #write loaded chosen file on Selected Files tkinter listbox
            list_of_files_paths = set_up_file.chosen_files
            for path in list_of_files_paths:
                tb1_chsn_files.insert('end', str(os.path.basename(path)))
            #write loaded available columns on Available columns tkinter listbox
            titles = set_up_file.available_columns
            for title in titles:
                tb1_avbl_cols.insert('end', str(title))
            #write loaded chosen columns on chosen columns, tkinter listbox
            confirmed_col = set_up_file.selected_columns
            for chosen in confirmed_col:
                tb1_chsn_cols.insert('end', chosen)
            #set values of confirmed columns Combobox
            tb1_slct_col.config(values = confirmed_col)
            #set text of Combobox
            tb1_slct_col.set('Select to change')
            #reset new_name dict
            new_name = set_up_file.dict_of_new_names
            #reset new_columns list
            new_columns = set_up_file.new_columns
            #add old names of chosen columns to Old Name tkinter listbox
            for old in set_up_file.old_names:
                tb1_old_list.insert('end', old)
            #add new names of chosen columns to New Name tkinter listbox
            for new in set_up_file.new_names:
                tb1_new_list.insert('end', new)
            #
            tb1_header_column.config(values = set_up_file.new_columns)
            tb1_header_column.set(set_up_file.header_column)
            #
            tb1_body_column.config(values = set_up_file.new_columns)
            tb1_body_column.set(set_up_file.body_column)
            # #add all out put files to all for final column tkinter listbox
            # for item in set_up_file.all_output:
            #     tb1_all_for_final.insert('end', item)
            # #add chosen out put files to chosen final column tkinter listbox
            # for item in set_up_file.chosen_output:
            #     tb1_chosen_for_final.insert('end', item)
            #send loaded list of conditions to loader_page method to write it on the frame
            headers, _, _, _ = finalize()
            mainframe.column_names(headers)
            mainframe.loader_page(set_up_file.list_of_prim_conditions, set_up_file.list_of_sec_conditions, headers)

def get_list_of_conditions():
    return mainframe.final()

#Save File
def save_file():
    """Save the current file as a new file."""
    global list_of_files_paths
    global titles
    global confirmed_col
    global new_name
    global new_columns
    #adding writen condition to data holder
    #saving files path on data holder
    data_holder.chosen_files = list_of_files_paths
    #saving available columns name on data holder
    data_holder.available_columns = titles
    #save chosen columns name on data holder
    data_holder.selected_columns = confirmed_col
    #save old names list to data holder
    data_holder.old_names = list(tb1_old_list.get(0, 'end'))
    #save new names list to data holder
    data_holder.new_names = list(tb1_new_list.get(0, 'end'))
    #
    data_holder.header_column = tb1_header_column.get()
    #
    data_holder.body_column = tb1_body_column.get()
    # #save all available column for out put to data holder
    # data_holder.all_output = list(tb1_all_for_final.get(0, 'end'))
    # #save chosen column for out put to data holder
    # data_holder.chosen_output = list(tb1_chosen_for_final.get(0, 'end'))
    #save new names dict to data holder
    data_holder.dict_of_new_names = new_name
    #save new columns list to data holder
    data_holder.new_columns = new_columns
    #data_holder.list_of_all_conditions = []
    prim, sec = mainframe.final()
    data_holder.list_of_prim_conditions = prim
    data_holder.list_of_sec_conditions = sec
    filename = asksaveasfilename(
        defaultextension="pickle",
        filetypes=[("Pickle Files", "*.pickle"), ("All Files", "*.*")],
    )
    if not filename:
        return
    try:
        if filename.endswith('.pickle'):
            with open(filename, 'wb') as outfile:
                pickle.dump(data_holder, outfile)
        else:
            tk.messagebox.showerror('Error Saving File',
                                    'You should choose .pickle extension for the file')
    except:
        tk.messagebox.showerror('Error Saving File',
                                'Unable to save on file: %r' % filename)

def Preview():
    global list_of_files_paths
    _, n_cols, del_cols, n_names = finalize()
    primary_conditions_list, secondary_conditions_list = get_list_of_conditions()
    table = Manipulator(list_of_files_paths[0])
    table = table.reconstructor(n_cols, del_cols, n_names)
    try:
        table = primaryFunction(primary_conditions_list, table)
        try:
            table = mainFunction(secondary_conditions_list, table)
        except:
            pass
    except ValueError:
        print(ValueError)
        try:
            table = mainFunction(secondary_conditions_list, table)
        except:
            pass
        pass
    new_window = tk.Toplevel(window)
    preview = Table(new_window, dataframe = table, showtoolbar = True, showstatusbar = True)
    preview.show()


# def run_script():
#     out_put_column = list(tb1_chosen_for_final.get(0, 'end'))
#     if not out_put_column:
#         tk.messagebox.showerror('Error!','First choose columns you want for output')
#         return
#     problematic_files = {}
#     file_name = asksaveasfilename(
#         filetypes=[("All Files", "*.*")],
#     )
#     if not file_name:
#         return

#     global list_of_files_paths
#     allcol, n_cols, del_cols, n_names = finalize()
#     col_to_drop = [col for col in allcol if col not in out_put_column]
#     primary_conditions_list, secondary_conditions_list = get_list_of_conditions()
#     final_dict = {'Participant Name': [], 'Gender': [], 'Correct Response':[]}

#     for f in list_of_files_paths:
#         base = os.path.basename(f)
#         base = os.path.splitext(base)[0]
#         try:
#             prm_table = Manipulator(f)
#             pn, ge, cr = prm_table.final_dict_values()
#             final_dict['Participant Name'].append(pn)
#             final_dict['Gender'].append(ge)
#             final_dict['Correct Response'].append(cr)
#             prm_table = prm_table.reconstructor(n_cols, del_cols, n_names)
#             new_table = primaryFunction(primary_conditions_list, prm_table)
#             new_table = mainFunction(secondary_conditions_list, new_table)
#             new_table.drop(columns = col_to_drop, inplace = True)
#             with open('{}-{}.txt'.format(file_name, base), 'w') as f_obj:
#                 f_obj.write(new_table.to_string(index = False))
#         except ValueError as e:
#             problematic_files[base] = "Can't process file due to {} error".format(e)

#     if problematic_files:
#         list_of_errors = [ f'{key} : {problematic_files[key]}' for key in problematic_files ]
#         fo = open(file_name + '-Error file.txt', 'w')
#         for item in list_of_errors:
#             fo.write('{}\n'.format(item))
#         fo.close()

#     final_table = pd.DataFrame.from_dict(final_dict)
#     with open('{}-Final.txt'.format(file_name), 'w') as final_obj:
#         final_obj.write(final_table.to_string(index = False))

def write_files_process(file_n, writing_list, problematic_files = None):
    if problematic_files:
        list_of_errors = [ f'{key} : {problematic_files[key]}' for key in problematic_files ]
        fo = open(file_n + '-Error file.txt', 'w')
        for item in list_of_errors:
            fo.write('{}\n'.format(item))
        fo.close()

    final_table = pd.DataFrame(writing_list)
    with open('{}-Final.txt'.format(file_n), 'w') as final_obj:
        final_obj.write(final_table.to_string(index = False))

def plot_files_process(file_n, writing_list, problematic_files):
    path = os.path.split(file_n)
    path = os.path.join(path[0], 'Figures')
    os.makedirs(path, exist_ok= True)
    for item in writing_list:
        title = item.pop('Participant Name', "-")
        try:
            del item['Gender']
            del item['Correct Response']
        except:
            pass
        fig, ax = plt.subplots()
        p = ax.bar(item.keys(), item.values())
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Percentage Synchrony Response')
        ax.set_xlabel('Steps of alignment')
        ax.set_title('Participant-{}'.format(title))

        save_name_path = os.path.join(path, '{}.png'.format(title))
        plt.xticks(rotation = -45)
        plt.tight_layout()
        plt.savefig(save_name_path)
        plt.close()
        




def run_script():
    plot_files = plot_check.get()
    write_files = write_check.get()
    if not write_files and not plot_files:
        tk.messagebox.showerror('Error!', 'You should choose at least one option!')
        return
    else:
        header_output = tb1_header_column.get()
        body_output = tb1_body_column.get()
        if not header_output or not body_output:
            tk.messagebox.showerror('Error!','First choose columns you want for output')
            return
        problematic_files = {}
        file_name = asksaveasfilename(
            filetypes=[("All Files", "*.*")],
        )
        if not file_name:
            return

        global list_of_files_paths
        _, n_cols, del_cols, n_names = finalize()
        primary_conditions_list, secondary_conditions_list = get_list_of_conditions()
        list_of_final_dicts = []

        for f in list_of_files_paths:
            final_dict = {}
            dict_for_plot = {}
            base = os.path.basename(f)
            base = os.path.splitext(base)[0]
            try:
                prm_table = Manipulator(f)
                pn, ge, cr = prm_table.final_dict_values()
                final_dict['Participant Name'] = pn
                final_dict['Gender'] = ge
                final_dict['Correct Response'] = cr
                prm_table = prm_table.reconstructor(n_cols, del_cols, n_names)
                new_table = primaryFunction(primary_conditions_list, prm_table)
                new_table = mainFunction(secondary_conditions_list, new_table)
                final_dict.update(final_function(new_table, header_output, body_output, secondary_conditions_list))
                list_of_final_dicts.append(final_dict)
            except ValueError as e:
                problematic_files[base] = "Can't process file due to {} error".format(e)

    if write_files and not plot_files:
        write_files_process(file_name, list_of_final_dicts, problematic_files)
    elif not write_files and plot_files:
        plot_files_process(file_name, list_of_final_dicts, problematic_files)
    elif write_files and plot_files:
        write_files_process(file_name, list_of_final_dicts, problematic_files)
        plot_files_process(file_name, list_of_final_dicts, problematic_files)



def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

#############################################################################################
#                                                                                           #
#                                          --BODY--                                         #
#                                                                                           #
#############################################################################################

window = tk.Tk()
window.title("Conditions Maker App")

window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

#Frames
fr_buttons = tk.Frame(window, relief = tk.RIDGE, borderwidth = 3)
fr_conditions = tk.Frame(window, relief = tk.RIDGE, borderwidth = 3)
fr_conditions.rowconfigure(0, weight = 1)
fr_conditions.columnconfigure(0, weight = 1)

#Tabs
tab_parent = ttk.Notebook(fr_conditions)
tab_parent.rowconfigure(0, weight = 1)
tab_parent.columnconfigure(0, weight = 1)

tab1 = ttk.Frame(tab_parent)
tab1.rowconfigure([0,1,2,3,4,5], weight = 1)
tab1.columnconfigure([0,1,2,3,4,5,6], weight = 1)
tab2 = ttk.Frame(tab_parent)
tab2.rowconfigure(0, weight = 1)
tab2.columnconfigure([0,1,2], weight = 1)
tab3 = ttk.Frame(tab_parent)

#Tabs element defenition
#Tab 1########################################################
tb1_section_1 = tk.Frame(tab1)
tb1_section_2 = tk.Frame(tab1)
tb1_section_3 = tk.Frame(tab1)

tb1_title = tk.Label(tb1_section_1, text = 'Raw data selection')
tb1_files = tk.Label(tb1_section_1, text = 'Selected Files')
tb1_avbl = tk.Label(tb1_section_1, text = 'Available columns')
tb1_chsn = tk.Label(tb1_section_1, text = 'Chosen columns')
sb1 = Scrollbar(tb1_section_1)
sb1x = Scrollbar(tb1_section_1, orient=tk.HORIZONTAL)
sb2 = Scrollbar(tb1_section_1)
sb2x = Scrollbar(tb1_section_1, orient=tk.HORIZONTAL)
sb3 = Scrollbar(tb1_section_1)
sb3x = Scrollbar(tb1_section_1, orient=tk.HORIZONTAL)
tb1_chsn_files = tk.Listbox(tb1_section_1, relief = tk.SUNKEN, xscrollcommand = sb1x.set, yscrollcommand = sb1.set)
tb1_avbl_cols = tk.Listbox(tb1_section_1, relief = tk.SUNKEN, xscrollcommand = sb2x.set, yscrollcommand = sb2.set)
tb1_chsn_cols = tk.Listbox(tb1_section_1, relief = tk.SUNKEN, xscrollcommand = sb3x.set, yscrollcommand = sb3.set)




tb1_scnd_title = tk.Label(tb1_section_2, text = 'Change columns name')
sb4 = Scrollbar(tb1_section_2)
sb4x = Scrollbar(tb1_section_2, orient=tk.HORIZONTAL)
sb5x = Scrollbar(tb1_section_2, orient=tk.HORIZONTAL)
sb6 = Scrollbar(tb1_section_3)
sb6x = Scrollbar(tb1_section_3, orient=tk.HORIZONTAL)
sb7 = Scrollbar(tb1_section_3)
sb7x = Scrollbar(tb1_section_3, orient=tk.HORIZONTAL)
tb1_cnfm_btn = tk.Button(tb1_section_2, text = 'Confirm chosen columns', command = lambda: confirm_col(tb1_chsn_cols))
tb1_slct_col = ttk.Combobox(tb1_section_2, values = confirmed_col)
tb1_new_name = tk.Entry(tb1_section_2)
tb1_chng_name = tk.Button(tb1_section_2, text = 'Rename column', command = lambda: rename_col())
tb1_old_title = tk.Label(tb1_section_2, text = 'Old Name')
tb1_old_list = tk.Listbox(tb1_section_2, relief = tk.SUNKEN, xscrollcommand = sb4x.set, yscrollcommand = sb4.set)
tb1_new_title = tk.Label(tb1_section_2, text = 'New Name')
tb1_new_list = tk.Listbox(tb1_section_2, relief = tk.SUNKEN, xscrollcommand = sb5x.set, yscrollcommand = sb4.set)
tb1_add_new_col = tk.Entry(tb1_section_2)
tb1_btn_add_new_col = tk.Button(tb1_section_2, text = 'Add new column', command = lambda: add_new_col())
tb1_btn_rmv_col = tk.Button(tb1_section_2, text = 'Remove selected column', command = lambda: remove_chosen_col())
tb1_btn_finalize = tk.Button(tb1_section_2, text = 'Finalize', command = lambda: columnNames())
tb1_section_3_title = tk.Label(tb1_section_3, text = 'Choose output columns')
tb1_header_column_title = tk.Label(tb1_section_3, text = 'Choose Header column')
tb1_header_column = ttk.Combobox(tb1_section_3)
tb1_body_column_title = tk.Label(tb1_section_3, text = 'Choose Body column')
tb1_body_column = ttk.Combobox(tb1_section_3)
plot_check = tk.IntVar()
tb1_plot_checkbox = tk.Checkbutton(tb1_section_3, text = 'Plot Diagrams', variable = plot_check)
write_check = tk.IntVar()
tb1_aggregated_output_checkbox = tk.Checkbutton(tb1_section_3, text = 'Produce Aggregated Output', variable = write_check)
tb1_aggregated_output_checkbox.select()
# tb1_section_3_title = tk.Label(tb1_section_3, text = 'Choose column for output')
# tb1_all_for_final_title = tk.Label(tb1_section_3, text = '--')
# tb1_all_for_final = tk.Listbox(tb1_section_3, relief = tk.SUNKEN, xscrollcommand = sb6x.set, yscrollcommand = sb6.set)
# tb1_chosen_for_final_title = tk.Label(tb1_section_3, text = '<-->')
# tb1_chosen_for_final = tk.Listbox(tb1_section_3, relief = tk.SUNKEN, xscrollcommand = sb7x.set, yscrollcommand = sb7.set)


btn_hldr1 = tk.Frame(tb1_section_1)
btn_add_all_1 = tk.Button(btn_hldr1, text = '>>', command = lambda: select_all(tb1_avbl_cols, tb1_chsn_cols))
btn_add_one_1 = tk.Button(btn_hldr1, text = '>', command = lambda: select_one(tb1_avbl_cols, tb1_chsn_cols))
btn_rmv_all_1 = tk.Button(btn_hldr1, text = '<<', command = lambda: deselect_all(tb1_avbl_cols, tb1_chsn_cols))
btn_rmv_one_1 = tk.Button(btn_hldr1, text = '<', command = lambda: deselect_one(tb1_avbl_cols, tb1_chsn_cols))

# btn_hldr2 = tk.Frame(tb1_section_3)
# btn_add_all_2 = tk.Button(btn_hldr2, text = '>>', command = lambda: select_all(tb1_all_for_final, tb1_chosen_for_final))
# btn_add_one_2 = tk.Button(btn_hldr2, text = '>', command = lambda: select_one(tb1_all_for_final, tb1_chosen_for_final))
# btn_rmv_all_2 = tk.Button(btn_hldr2, text = '<<', command = lambda: deselect_all(tb1_all_for_final, tb1_chosen_for_final))
# btn_rmv_one_2 = tk.Button(btn_hldr2, text = '<', command = lambda: deselect_one(tb1_all_for_final, tb1_chosen_for_final))
#Tab2##########################################################
canvas = tk.Canvas(tab2, borderwidth=0, width = '23 c')
vsb = tk.Scrollbar(tab2, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
#tb2_plc_hldr = tk.Frame(canvas)

mainframe = MainFrame(canvas)
mainframe.rowconfigure(0, weight = 1)
mainframe.columnconfigure([0,1,2], weight = 1)

#Tab 1#########################################################
tb1_section_1.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_section_2.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_section_3.grid(row = 1, column = 1, sticky = 'nsew', padx = 5, pady = 5)

tb1_title.grid(row = 0, column = 2, sticky = 'nsew', padx=5, pady=3)
tb1_files.grid(row =1 , column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_avbl.grid(row =1 , column = 2, sticky = 'nsew', padx = 5, pady = 5)
tb1_chsn.grid(row = 1, column = 5, sticky = 'nsew', padx = 5, pady = 5)
tb1_chsn_files.grid(row = 2, column = 0, sticky = 'w')
sb1.grid(row = 2, column = 1, sticky = 'ns')
sb1x.grid(row = 3, column = 0, sticky = 'ew')
tb1_avbl_cols.grid(row = 2, column = 2, sticky = 'w')
sb2.grid(row = 2, column = 3, sticky = 'ns')
sb2x.grid(row = 3, column = 2, sticky = 'ew')
btn_hldr1.grid(row = 2, column = 4)
btn_add_all_1.grid(row = 1, column = 0, sticky = 'ew', padx = 10, pady = 5)
btn_add_one_1.grid(row = 2, column = 0, sticky = 'ew', padx = 10, pady = 5)
btn_rmv_all_1.grid(row = 3, column = 0, sticky = 'ew', padx = 10, pady = 5)
btn_rmv_one_1.grid(row = 4, column = 0, sticky = 'ew', padx = 10, pady = 5)
tb1_chsn_cols.grid(row = 2, column = 5, sticky = 'w')
sb3.grid(row = 2, column = 6, sticky = 'ns')
sb3x.grid(row = 3, column = 5, sticky = 'ew')

tb1_scnd_title.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
tb1_cnfm_btn.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_slct_col.grid(row = 2, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_new_name.grid(row = 3, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_chng_name.grid(row = 4, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_add_new_col.grid(row = 5, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_btn_add_new_col.grid(row = 6, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_btn_rmv_col.grid(row = 7, column = 0, sticky = 'nsew', padx = 5, pady = 5)
tb1_old_title.grid(row = 1, column = 1, sticky = 'nsew', padx = 5, pady = 5)
tb1_old_list.grid(row = 2, column = 1, rowspan = 4, sticky = 'nsew', padx = 5, pady = 5)
tb1_new_title.grid(row = 1, column = 2, sticky = 'nsew', padx = 5, pady = 5)
tb1_new_list.grid(row = 2, column = 2, rowspan = 4, sticky = 'nsew', padx = 5, pady = 5)
sb4.grid(row = 2, column = 3, rowspan = 4, sticky = 'ns', padx = 5, pady = 5)
sb4x.grid(row = 6, column = 1, sticky = 'ew', padx = 5, pady = 5)
sb5x.grid(row = 6, column = 2, sticky = 'ew', padx = 5, pady = 5)
tb1_btn_finalize.grid(row = 7, column = 2, sticky = 'nsew', padx = 5, pady = 5)

tb1_section_3_title.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
tb1_header_column_title.grid(row = 1, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
tb1_header_column.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
tb1_body_column_title.grid(row = 3, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
tb1_body_column.grid(row = 4, column = 0, columnspan = 3, sticky = 'nsew', padx = 5, pady = 5)
tb1_plot_checkbox.grid(row = 5, column = 0, columnspan = 3, sticky = 'nsw', padx = 5, pady = 5)
tb1_aggregated_output_checkbox.grid(row = 6, column = 0, columnspan = 3, sticky = 'nsw', padx = 5, pady = 5)

# tb1_all_for_final_title.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 8)
# tb1_all_for_final.grid(row = 2, rowspan = 4, column = 0, sticky = 'nsew', padx = 5, pady = 5)
# btn_hldr2.grid(row = 2, rowspan = 4, column = 2, sticky = 'nsew', padx = 5, pady = 5)
# btn_add_all_2.grid(row = 1, column = 0, sticky = 'ew', padx = 5, pady = 5)
# btn_add_one_2.grid(row = 2, column = 0, sticky = 'ew', padx = 5, pady = 5)
# btn_rmv_all_2.grid(row = 3, column = 0, sticky = 'ew', padx = 5, pady = 5)
# btn_rmv_one_2.grid(row = 4, column = 0, sticky = 'ew', padx = 5, pady = 5)
# tb1_chosen_for_final_title.grid(row = 1, column = 3, sticky = 'nsew', padx = 5, pady = 8)
# tb1_chosen_for_final.grid(row = 2, rowspan = 4, column = 3, sticky = 'nsew', padx = 5, pady = 5)
# sb6.grid(row = 2, rowspan = 4, column = 1, sticky = 'nsew', padx = 5, pady = 5)
# sb6x.grid(row = 6, column = 0, sticky = 'nsew', padx = 5, pady = 5)
# sb7.grid(row = 2, rowspan = 4, column = 4, sticky = 'nsew', padx = 5, pady = 5)
# sb7x.grid(row = 6, column = 3, sticky = 'nsew', padx = 5, pady = 5)
#Tab 2#########################################################
#btn_add_cond.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)
#btn_rmv_all_cond.grid(row = 0, column = 2, sticky = 'nsew', padx = 5, pady = 5)
#tb2_plc_hldr.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 5)
mainframe.grid(sticky = 'nsew')



vsb.grid(row = 0, column = 3, sticky="nse")
canvas.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew')
canvas.create_window((4,4), window=mainframe, anchor="nw")

mainframe.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
################################################################



sb1.config(command = tb1_chsn_files.yview )
sb1x.config(command = tb1_chsn_files.xview )
sb2.config(command = tb1_avbl_cols.yview ) 
sb2x.config(command = tb1_avbl_cols.xview )
sb3.config(command = tb1_chsn_cols.yview )
sb3x.config(command = tb1_chsn_cols.xview ) 
sb4.config(command = tb1_old_list.yview )
sb4x.config(command = tb1_old_list.xview ) 
sb5x.config(command = tb1_new_list.xview)
# sb6.config(command = tb1_all_for_final.yview)
# sb6x.config(command = tb1_all_for_final.xview)
# sb7.config(command= tb1_chosen_for_final.yview)
# sb7x.config(command = tb1_chosen_for_final)


tab_parent.add(tab1, text = 'Set Up')
tab_parent.add(tab2, text = 'Conditions')
tab_parent.add(tab3, text = 'Agregation')

#Buttons
btn_open = tk.Button(fr_buttons, text="Open", command = open_file)
btn_load = tk.Button(fr_buttons, text ="Load File", command = load_set_up_file)
btn_save = tk.Button(fr_buttons, text="Save Script", command = save_file)
btn_preview = tk.Button(fr_buttons, text="Preview", command = Preview)
btn_run = tk.Button(fr_buttons, text="Run Script", command = run_script)

#Assign tabs to the fr_conditions
tab_parent.grid(sticky = 'nsew')

#Assign buttons to the fr_buttons
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=3)
btn_load.grid(row=1, column=0, sticky="ew", padx=5, pady=3)
btn_save.grid(row=2, column=0, sticky="ew", padx=5, pady=3)
btn_preview.grid(row=3, column=0, sticky="ew", padx=5, pady=3)
btn_run.grid(row=4, column=0, sticky="ew", padx=5, pady=3)

#Set the frame on window
fr_buttons.grid(row=0, column=0, sticky="ns")
fr_conditions.grid(row=0, column=1, sticky="nsew")

# Run the application
window.mainloop()