#############################################################################
#                                                                           #
#                   ---Importing packages and libraries---                  #
#                                                                           #
#############################################################################
import pandas as pd
import os
import csv

from gui import files_list, finalize, get_list_of_conditions
from data_organizer import Manipulator
#from field_maker1 import MainFrame
from condition_executer import mainFunction

#############################################################################
#                                                                           #
#                       ---Functions defenitions---                         #
#                                                                           #
#############################################################################


#############################################################################
#                                                                           #
#                     ---Reading and preparing data---                      #
#                                                                           #
#############################################################################

list_of_files_paths = files_list()
_, added_col, del_col, new_names = finalize()
list_of_conditions = get_list_of_conditions()


def filePicker():
    for f in list_of_files_paths:
        table = Manipulator()
        table = table.reconstructor(f, added_col, del_col, new_names)
        new_table = mainFunction(list_of_conditions, table)