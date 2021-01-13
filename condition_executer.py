



class ColumnIdx():
    def __init__(self, locond, dataframe):
        self.locond = locond
        self.table = dataframe
        self.header = self.table.columns
    #Finds unique words of conditions to check if they are columns name or not
    def elements(self):
        all_names = set()
        i = 0
        length = len(self.locond)
        while i < length:
            j = 0
            length2 = len(self.locond[i])
            while j < length2:
                list_of_conditions = self.locond[i][j]['condition']
                for condition in list_of_conditions:
                    all_names.add(condition[1])
                    all_names.add(condition[3])
                try:
                    list_of_actions = self.locond[i][j]['action']
                    for action in list_of_actions:
                        all_names.add(action[1])
                except:
                    pass
                j += 1
            i += 1
        return all_names
    #Take locond and dataframe table and return integer location of columns
    def column_idx(self):
        unique_names = self.elements()
        header_idx = {}
        for elem in unique_names:
            if elem in self.header:
                header_idx[elem] = self.table.columns.get_loc(elem)
        return header_idx



class IfStatement():
    
    def __init__(self, condition, header_idx, row):
        self.condition = condition
        self.header_idx = header_idx
        self.row = row
    
    def seperator(self, i):
        first_elem = self.condition[i][1]
        if first_elem in self.header_idx:
            column = self.header_idx[first_elem]
            first_elem = self.row[column]
        comparator = self.condition[i][2]
        second_elem = self.condition[i][3]
        if second_elem in self.header_idx:
            column = self.header_idx[second_elem]
            second_elem = self.row[column]
        return first_elem, comparator, second_elem
    
    def logic_comp(self):
        #call comparison and check logical conditions
        result = self.comparison()
        counter = len(self.condition)
        i = 1
        while i < counter:
            if self.condition[i][0] == 'and':
                res = all([result[0], result[1]])
                result = result[2:]
                result.insert(0, res)
            elif self.condition[i][0] == 'or':
                res = any([result[0], result[1]])
                result = result[2:]
                result.insert(0, res)
            elif self.condition[i][0] == 'not and':
                res = not all([result[0], result[1]])
                result = result[2:]
                result.insert(0, res)
            elif self.condition[i][0] == 'not or':
                res = not any([result[0], result[1]])
                result = result[2:]
                result.insert(0, res)
            i += 1
        return result[0]
                
    
    def comparison(self):
        i = 0
        result = []
        while i < len(self.condition):
            first_elem, comparator, second_elem = self.seperator(i)
            if comparator == 'gt':
                result.append(first_elem > second_elem)
            elif comparator == 'ge':
                result.append(first_elem >= second_elem)
            elif comparator == 'lt':
                result.append(first_elem < second_elem)
            elif comparator == 'le':
                result.append(first_elem <= second_elem)
            elif comparator == 'eq':
                result.append(first_elem == second_elem)
            elif comparator == 'in':
                result.append(first_elem in second_elem)
            elif comparator == 'not in':
                result.append(first_elem not in second_elem)
            elif comparator == '':
                result.append(True)
            i += 1
        return result


def mainFunction(conditions_list, df_table):
    #sending list of ocnditions to ColumnIdx class to obtain id of columns
    header_idx = ColumnIdx(conditions_list, df_table).column_idx()
    unique_rows = set()
    i = 0
    length = len(df_table.index)
    while i < length: # i is the length of table
        row = df_table.iloc[i]
        j = 0
        while j < len(conditions_list): # j is the j-th sublist of main condition list
            k = 0
            while k < len(conditions_list[j]): #k is the k-th condition of jth sublist
                result = IfStatement(conditions_list[j][k]['condition'], header_idx, row).logic_comp()
                if result:
                    unique_rows.add(i)
                    #do then
                    action = conditions_list[j][k]['action']
                    action_length = len(action)
                    z = 0
                    while z < action_length:
                        first_elem = action[z][1]
                        if first_elem in header_idx:
                            column = header_idx[first_elem]
                            df_table.iloc[i, column] = action[z][3]
                        z += 1
                    break #go to next sublist
                k += 1
            j += 1
        i += 1
    rows_to_drop = [m for m in df_table.index if m not in list(unique_rows)]
    df_table.drop(rows_to_drop, inplace = True)
    return df_table



def primaryFunction(conditions_list, df_table):
    #sending list of ocnditions to ColumnIdx class to obtain id of columns
    header_idx = ColumnIdx(conditions_list, df_table).column_idx()
    unique_rows = set()
    i = 0
    length = len(df_table.index)
    while i < length: # i is the length of table
        row = df_table.iloc[i]
        result = IfStatement(conditions_list[0][0]['condition'], header_idx, row).logic_comp()
        if result:
            unique_rows.add(i)
        i += 1
    rows_to_drop = [m for m in df_table.index if m not in list(unique_rows)]
    df_table.drop(rows_to_drop, inplace = True)
    df_table.reset_index(drop = True, inplace = True)
    return df_table

