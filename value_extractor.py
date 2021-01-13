#############################################################################
#                                                                           #
#                   ---Importing packages and libraries---                  #
#                                                                           #
#############################################################################
import json
import tkinter as tk
from tkinter import ttk

class ValueExtractor():

    def __init__(self, frm_hldr):
        self.total_list_of_conditions = []
        self.frame_holder = frm_hldr

    def condition_list_maker(self):
        """This fucntion produces a formatted state of conditions. formatted state is something like:
        total_list_of_conditions =  
        [
            [
                {
                    'condition': [('if', 'this', 'comparator', 'that'), ('and', 'this', 'comparator', 'that')],
                    'action': [('then', 'do', 'comparator', 'something')]
                },
                {
                    'condition': [('elif', 'this', 'comparator', 'that')],
                    'action' : [('then', 'do', 'comparator', 'something'), ('and', 'do', 'comparator', 'something')]
                }
            ],
            [
                {
                    'condition': [('if', 'this', 'comparator', 'that'), ('and', 'this', 'comparator', 'that')],
                    'action' : [('then', 'do', 'comparator', 'something'), ('and', 'do', 'comparator', 'something')]
                }
            ]
        ]
        """

        #Extract each group of conditions on Main Frame  
        groups_on_MF = [child for child in self.frame_holder.winfo_children()]    
        #Finding number of group of conditions on Main Frame
        length = len(groups_on_MF)
        i = 0
        #Iterate over each group of conditions to find elements and exctracting values
        while i < length:
            #condition_list holds dicts of conditions that compose an operation. like: [{'condition': '...', 'action': '...'}, ...]
            condition_list = []
            #condition_dict holds a complete condition consits of 'if', 'elif', 'else', 'then', 'and' , ... .
            # like: {'condition': [('if', 'this', 'comparator', 'that')], 'action': [('then', 'do', 'comparator', 'something')]}
            # this dict append to the above condition_list
            conditions_dict = {}
            #Taking one group of condition on Main Frame to extract it's elements
            condition_group = groups_on_MF[i]
            #Extracting lines of considered group
            line_group = [elem for elem in condition_group.winfo_children() if not isinstance(elem, tk.Button)]
            #Finding number of lines of considered group
            length2 = len(line_group)
            #Flag to control the flow of assignment
            flag = ''
            j = 0
            #Iterate over each extracted line of the group of condition
            while j < length2:
                #Extracting elements on the considered line
                line_condition = line_group[j].winfo_children()
                #Finding number of elements on the considered line
                length3 = len(line_condition)
                k = 0
                #List to store value of elements on the considered line
                condition_elements = []
                #Iterate over each element of the considered line to extract their values
                while k < length3:
                    #Checking to find if an element is a button or not
                    if not isinstance(line_condition[k], tk.Button):
                        if k < (length3-1) and line_condition[2].get() not in ['in', 'not in']:
                            try:
                                value = int(line_condition[k].get())
                            except:
                                value = line_condition[k].get()
                        else:
                            value = line_condition[k].get()
                        #Appending value of an element to the condition_elements list if that element is not a button
                        condition_elements.append(value)
                    k += 1
                #Variable to hold first value of each condition_elements list
                statement_starter = condition_elements[0]
                #Changing the list of values extraced from the considered line to a tuple
                condition_tuple = tuple(condition_elements)
                ######################################################################################################
                #                                                                                                    #
                #   |||\ --Making a formated state of extracted conditions to feed them to the main_script--/|||     #
                #                                                                                                    #
                ######################################################################################################
                
                #Checking to see if the line starts with one of the condition maker phrases or not
                if statement_starter == 'if' or statement_starter == 'elif' or statement_starter == 'else':
                    #if there is any condition_dict
                    if conditions_dict:
                        #append that condition_dict to condition_list
                        condition_list.append(conditions_dict)
                    #clear condition_dict
                    conditions_dict = {}
                    #make a list that stores tuples of conditions. this list will be appended to the 'condition' of conditions_dict.
                    # like: {'condition': [('if', 'this', 'comparator', 'that')], 'action': ...}
                    condition_part = []
                    #make a list that stores tuples of actions that must be done if condition part is True. this list will be appended to the 'action' of conditions_dict.
                    # like: {'condition': ..., 'action': [('then', 'do', 'comparator', 'something')]}
                    action_part = []
                    #if a tuple start with if, elif, else, it is a condition phrase and here will be appended to condition_part
                    condition_part.append(condition_tuple)
                    #adding condition_part to the 'condition' of the conditions_dict.
                    conditions_dict['condition'] = condition_part
                    #changing flag to the condition, that means last tuple since here is a condition
                    flag = 'condition'
                #Checking to see if the line starts with action maker phrase
                elif statement_starter == 'then':
                    #if a tuple start with then, it is an action phrase and here will be appended to action_part
                    action_part.append(condition_tuple)
                    #adding action_part to the 'action' of the conditions_dict.
                    conditions_dict['action'] = action_part
                    #changing flag to the action, that means last tuple since here is an action
                    flag = 'action'
                #If line do not start neither with condition makers nor action maker, then it is an 'and phrase'
                #and it must be added to the previous phrase
                else:
                    #if last tuple since here was a condition
                    if flag == 'condition':
                        #append current 'and phrase' to 'condition' of conditions_dict
                        conditions_dict['condition'].append(condition_tuple)
                    #if last tuple since here was an action
                    elif flag == 'action':
                        #append current 'and' phrase to 'action' of conditions_dict
                        conditions_dict['action'].append(condition_tuple)
                j += 1

            #Append conditions_dict of last iteration to condition_list
            condition_list.append(conditions_dict)
            #Append condition_list to the total_list_of_conditions. each condition_list contains all conditions on a group of condition
            self.total_list_of_conditions.append(condition_list)
            i += 1
        return self.total_list_of_conditions
