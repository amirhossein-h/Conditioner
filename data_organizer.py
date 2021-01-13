#############################################################################
#                                                                           #
#                   ---Importing packages and libraries---                  #
#                                                                           #
#############################################################################
import pickle
import pandas as pd
import os

class Organizer():

    def __init__(self):
        self.chosen_files = []
        self.available_columns = []
        self.selected_columns = []
        self.old_names = []
        self.new_names = []
        self.list_of_prim_conditions = []
        self.list_of_sec_conditions = []
        self.new_columns = []
        self.dict_of_new_names = {}
        self.all_output = []
        self.chosen_output = []
        self.header_column = None
        self.body_column = None


class Manipulator():
    #Reading table and rearranging header
    def __init__(self, f_address, skiprows = 4, header = [0,1]):
        address = os.path.join(f_address)
        self.table = pd.read_table(address, skiprows = skiprows, header = header, engine= 'python')
        self.new_header = [' '.join(tups) for tups in self.table.columns]
        self.new_header = [i.strip() for i in self.new_header]
        self.table.columns = self.new_header

    #Rturn old table header
    def read_header(self):
        return self.new_header

    #Reconstructing table
    def reconstructor(self, added_columns, deleted_columns, changed_names):
        reconstructed_table = self.table.drop(columns = deleted_columns)
        reconstructed_table.rename(columns = changed_names, inplace = True)
        for column in added_columns:
            reconstructed_table[column] = ''
        return reconstructed_table
    
    #Return specific value of old table
    def final_dict_values(self):
        v = self.table.iloc[0, 0]
        w = self.table.iloc[0]['Correct Response']
        return v, v[0], w




################################
def conditions_index(list_of_conditions, already_sorted, header_column_elem):
    length = len(list_of_conditions)
    temp = None
    if header_column_elem not in already_sorted:
        i = 0
        while i < length:
            length1 = len(list_of_conditions[i])
            j = 0
            while j < length1:
                length2 = len(list_of_conditions[i][j]['action'])
                k = 0
                while k < length2:
                    if list_of_conditions[i][j]['action'][k][3] == header_column_elem:
                        temp = {str(header_column_elem):(i, j)}
                    k += 1
                j += 1
            i += 1
    else:
        pass
    return temp

################################
##########---sort---############
def sorting(dict_to_sort):
    sorted_values = []
    sorted_keys = []
    for value in sorted(dict_to_sort.values()):
        sorted_values.append(value)

    for item in sorted_values:
        for key, value in dict_to_sort.items():
            if value == item:
                sorted_keys.insert(sorted_values.index(item), key)
    return sorted_keys

#############################################################################################



def final_function(processed_df, header_column, body_column, conditions_list):
    header_idx = processed_df.columns.get_loc(header_column)
    body_idx = processed_df.columns.get_loc(body_column)
    header_counter_dict = {}
    value_counter_dict = {}
    computed_dict = {}
    indices_dict = {}
    already_sorted = set()
    length = len(processed_df.index)
    i = 0
    while i < length:
        if not processed_df.iloc[i, header_idx] in header_counter_dict:
            header_counter_dict[processed_df.iloc[i, header_idx]] = 1
        else:
            header_counter_dict[processed_df.iloc[i, header_idx]] += 1
        indexed_elem = conditions_index(conditions_list, already_sorted, processed_df.iloc[i, header_idx])
        if indexed_elem:
            already_sorted.add(list(indexed_elem.keys())[0])
            indices_dict.update(indexed_elem)
        if not processed_df.iloc[i, header_idx] in value_counter_dict:
            value_counter_dict[processed_df.iloc[i, header_idx]] = processed_df.iloc[i, body_idx]
        else:
            value_counter_dict[processed_df.iloc[i, header_idx]] += processed_df.iloc[i, body_idx]
        i += 1

    sorted_dict = sorting(indices_dict)

    for item in value_counter_dict.keys():
        computed_dict[item] = int(value_counter_dict[item])/int(header_counter_dict[item])

    sorted_computed_dict = {}
    for item in sorted_dict:
        sorted_computed_dict.update({item: computed_dict[item]})
    return sorted_computed_dict
