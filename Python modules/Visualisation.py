import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.patches import Patch
import textwrap
import seaborn as sns
import copy
import os

SAVE_PATH = os.getcwd()

class Visualisation:

    def __init__(self):
        self.input_dataframe_species = pd.DataFrame()
        self.input_dataframe_functionalities = pd.DataFrame()
        self.species_and_functionalities_matrix = pd.DataFrame()
        self.visualisation_dataframe = pd.DataFrame()
        self.input_dataframe_healthy = pd.DataFrame()
        self.input_dataframe_ill = pd.DataFrame() 
        self.healthy_with_ill_dataframe = pd.DataFrame()
        self.itemset_stats_dataframe = pd.DataFrame()
        self.association_stats_dataframe = pd.DataFrame()

    def set_input_dataframe_species(self, assign):
        self.input_dataframe_species = assign

    def get_input_dataframe_species(self):
        return self.input_dataframe_species

    def set_input_dataframe_functionalities(self, assign):
        self.input_dataframe_functionalities = assign

    def get_input_dataframe_functionalities(self):
        return self.input_dataframe_functionalities

    def set_species_and_functionalities_matrix(self, assign):
        self.species_and_functionalities_matrix = assign

    def get_species_and_functionalities_matrix(self):
        return self.species_and_functionalities_matrix

    def set_visualisation_dataframe(self, assign):
        self.visualisation_dataframe = assign

    def get_visualisation_dataframe(self):
        return self.visualisation_dataframe

    def set_input_dataframe_healthy(self, assign):
        self.input_dataframe_healthy = assign

    def get_input_dataframe_healthy(self):
        return self.input_dataframe_healthy

    def set_input_dataframe_ill(self, assign):
        self.input_dataframe_ill = assign

    def get_input_dataframe_ill(self):
        return self.input_dataframe_ill

    def set_healthy_with_ill_dataframe(self, assign):
        self.healthy_with_ill_dataframe = assign

    def get_healthy_with_ill_dataframe(self):
        return self.healthy_with_ill_dataframe

    def set_itemset_stats_dataframe(self, assign):
        self.itemset_stats_dataframe = assign

    def get_itemset_stats_dataframe(self):
        return self.itemset_stats_dataframe

    def set_association_stats_dataframe(self, assign):
        self.association_stats_dataframe = assign

    def get_association_stats_dataframe(self):
        return self.association_stats_dataframe

    '''
    It merges the closed species and functionality itemset matrices.
    '''
    def merge_species_with_functionalities(self, extension, input_file_species, input_file_functionalities, output_name, species_sheet='Closed itemsets by sample mtx', functionlities_sheet = 'Closed itemsets by sample mtx'):

        if extension == 'csv':
            self.set_input_dataframe_species(pd.read_csv(f'{SAVE_PATH}/{input_file_species}.csv', low_memory = False, index_col = 0))
            self.set_input_dataframe_functionalities(pd.read_csv(f'{SAVE_PATH}/{input_file_functionalities}.csv', low_memory = False, index_col = 0))
        elif extension == 'xlsx':
            self.set_input_dataframe_species(pd.read_excel(f'{SAVE_PATH}/{input_file_species}.xlsx', sheet_name = species_sheet, index_col = 0))
            self.set_input_dataframe_functionalities(pd.read_excel(f'{SAVE_PATH}/{input_file_functionalities}.xlsx', sheet_name = functionlities_sheet, index_col = 0))
        else:
            print('Use a valid extension name such as csv or xlsx')

        
        self.set_input_dataframe_species(self.get_input_dataframe_species().loc[:, ~self.get_input_dataframe_species().columns.str.contains('^Unnamed')])
        self.set_input_dataframe_functionalities(self.get_input_dataframe_functionalities().loc[:, ~self.get_input_dataframe_functionalities().columns.str.contains('^Unnamed')])
        self.set_species_and_functionalities_matrix(pd.merge(self.get_input_dataframe_species(), self.get_input_dataframe_functionalities(), left_index = True, right_index = True, how = 'left'))
        self.set_species_and_functionalities_matrix(self.order_column_elements(self.get_species_and_functionalities_matrix()))
        self.get_species_and_functionalities_matrix().sort_index(axis = 1, inplace = True)
        self.get_species_and_functionalities_matrix().to_csv(f"{SAVE_PATH}//species_with_functionalities_{output_name}.csv")


    '''
    It merges the closed healthy and ill species itemset matrices or the closed healthy and ill functionalities itemset matrices.
    '''
    def merge_healthy_with_ill(self, extension, input_file_healthy, input_file_ill, output_name, healthy_sheet='Closed itemsets by sample mtx', ill_sheet = 'Closed itemsets by sample mtx'):

        if extension == 'csv':
            self.set_input_dataframe_healthy(pd.read_csv(f'{SAVE_PATH}/{input_file_healthy}.csv', low_memory = False, index_col = 0))
            self.set_input_dataframe_ill(pd.read_csv(f'{SAVE_PATH}/{input_file_ill}.csv', low_memory = False, index_col = 0))
        elif extension == 'xlsx':
            self.set_input_dataframe_healthy(pd.read_excel(f'{SAVE_PATH}/{input_file_healthy}.xlsx', sheet_name = healthy_sheet, index_col = 0))
            self.set_input_dataframe_ill(pd.read_excel(f'{SAVE_PATH}/{input_file_ill}.xlsx', sheet_name = ill_sheet, index_col = 0))
        else:
            print('Use a valid extension name such as csv or xlsx')

        self.set_input_dataframe_healthy(self.get_input_dataframe_healthy().loc[:, ~self.get_input_dataframe_healthy().columns.str.contains('^Unnamed')])
        self.set_input_dataframe_ill(self.get_input_dataframe_ill().loc[:, ~self.get_input_dataframe_ill().columns.str.contains('^Unnamed')])
        self.set_healthy_with_ill_dataframe(pd.concat([self.get_input_dataframe_healthy(), self.get_input_dataframe_ill()], axis = 0))
        for item in self.get_healthy_with_ill_dataframe().columns:
            for i, thing in enumerate(self.get_healthy_with_ill_dataframe()[item]):
                if thing != True:
                    self.get_healthy_with_ill_dataframe().at[self.get_healthy_with_ill_dataframe().index.values[i], item] = False
        self.get_healthy_with_ill_dataframe().to_csv(f"{SAVE_PATH}//healthy_with_ill_{output_name}.csv")

    '''
    It ensures that an ordered list with tags is recreated when a file read in. 
    '''
    def order_column_elements(self, input_dataframe):
        self.temp_list = []
        self.new_title = ""
        self.final_list = []
        for i, item in enumerate(input_dataframe.columns):
            if isinstance(item, str) == True:
                item = item.replace("frozenset({", "")
                item = item.replace("})", "")
                item = item.replace(",", "")
                item = item.replace("'", "")
                split_item = item.split(' ')
                for member in split_item:
                    self.temp_list.append(member)
                self.temp_list.sort()
                for member in self.temp_list:
                    if (member[0:3] == "GO:") | (member[0:4] == "IPR:"):
                        if self.new_title == "":
                            self.new_title = '$' + member
                        else:
                            self.new_title = self.new_title + '$' + member
                    else:
                        if self.new_title == "":
                            self.new_title = '#' + member
                        else:
                            self.new_title = self.new_title + '#' + member
                input_dataframe.columns.values[i] = self.new_title
                self.temp_list = []
                self.new_title = ""
            else:
                for member in item:
                    self.temp_list.append(member)
                self.final_list.append(self.temp_list.sort())
                self.temp_list = []

        input_dataframe = input_dataframe[sorted(input_dataframe.columns)]
        
        return input_dataframe
 
    '''
    It reads in an excel file.
    '''       
    def read_in_excel_for_visualisation(self, extension, input_file, input_sheet):  
        self.set_visualisation_dataframe(pd.read_excel(f'{SAVE_PATH}/{input_file}.xlsx', sheet_name = input_sheet, index_col = 0))
        self.set_visualisation_dataframe(self.get_visualisation_dataframe().loc[:, ~self.get_visualisation_dataframe().columns.str.contains('^Unnamed')])

    '''
    It reads in a csv file. 
    '''
    def read_in_csv_for_visualisation(self, extension, input_file):
        self.set_visualisation_dataframe(pd.read_csv(f'{SAVE_PATH}/{input_file}.csv', low_memory = False, index_col = 0))
        self.set_visualisation_dataframe(self.get_visualisation_dataframe().loc[:, ~self.get_visualisation_dataframe().columns.str.contains('^Unnamed')])

    '''
    It visualizes the boolean matrix of presence/absence of closed itemsets.
    '''  
    def matrix_visualisation(self, extension, input_file, title, input_sheet = "", threshold = 25, wraplength = 150, max_lines = 2,  title_fontsize = 22):
        self.sub_dataframe = pd.DataFrame()
        self.plot_rows = 0
        self.plot_range_values_list = []
        self.x_labels = []
        self.y_labels = []
        self.new_labels_list = []
        self.legend_values = ""
        self.label_text = ""
        
        if extension == 'csv':
            self.read_in_csv_for_visualisation(extension = extension, input_file = input_file)
            
        elif extension == 'xlsx':
            self.read_in_excel_for_visualisation(extension = extension, input_file = input_file, input_sheet = input_sheet)
            
        if self.get_visualisation_dataframe().shape[1] < threshold:
            self.plot_range_values_list.append(0)
            self.plot_range_values_list.append(self.get_visualisation_dataframe().shape[1])
            self.plot_rows = 1

        else: 
            if (self.get_visualisation_dataframe().shape[1] / threshold) > float(int(round((self.get_visualisation_dataframe().shape[1] / threshold), 0))):
                self.plot_rows = int((round((self.get_visualisation_dataframe().shape[1] / threshold), 0)) + 1)
            else:
                self.plot_rows = int((round((self.get_visualisation_dataframe().shape[1] / threshold), 0)))

            for number in range(0, threshold * self.plot_rows, threshold):
                self.plot_range_values_list.append(number)

            if self.get_visualisation_dataframe().shape[1] % threshold != 0:
                self.plot_range_values_list.append(self.get_visualisation_dataframe().shape[1])

        self.get_visualisation_dataframe().to_csv(f"{SAVE_PATH}//{title}_species-functionality_matrix.csv")

        
        for m in range(self.plot_rows): 
            
            self.sub_dataframe = self.get_visualisation_dataframe().iloc[:,self.plot_range_values_list[m]:self.plot_range_values_list[m+1]]
            self.x_labels = self.sub_dataframe.index.values
            self.y_labels = self.sub_dataframe.columns.values
            
            self.cmap = mpl.colormaps['autumn']
            self.fig, self.ax = plt.subplots(figsize=(25, 40))
            self.im = self.ax.imshow(self.sub_dataframe.T, cmap = self.cmap, vmin = 0, vmax = 1)
            self.ax.set_xticks(ticks = np.arange(len(self.x_labels)), labels = self.x_labels, fontsize = 12, fontweight = "bold")
            self.ax.set_yticks(ticks = np.arange(len(self.y_labels)), labels = self.y_labels, fontsize = 12, fontweight = "medium")
            for ytick_label in self.ax.get_yticklabels():
                self.label_text = ytick_label.get_text()
                self.new_labels_list.append(textwrap.fill(self.label_text, width = wraplength, max_lines = max_lines))
            self.ax.set_yticks(ticks = np.arange(len(self.new_labels_list)), labels = self.new_labels_list, fontsize = 9, fontweight = "semibold", horizontalalignment ='left')
            
            plt.setp(self.ax.get_xticklabels(), ha="center", va ="top", rotation_mode="anchor")
            plt.setp(self.ax.get_yticklabels(), ha="right", va ="bottom", rotation_mode="anchor")
            self.ax.set_title(f"{title} - species/functionality - from column {self.plot_range_values_list[m]} to {self.plot_range_values_list[m+1]}", fontsize=title_fontsize, fontweight = "bold", loc = 'left')
            self.legend_values = [Patch(color=self.cmap(0.9), label='Present'), Patch(color=self.cmap(0), label='Not Present')]  
            plt.legend(handles=self.legend_values, bbox_to_anchor=[1.0, 1.05], loc='right', fontsize=16, handlelength=.8)

            self.fig.tight_layout()
            
            
            for i in range(len(self.new_labels_list)): 
                for j in range(len(self.x_labels)): 
                    plt.annotate(str(self.sub_dataframe.T.iloc[i][j]), xy=(j, i), ha='center', va='center', color='black', rotation = 45, fontsize=9)
            plt.xlabel("Sample numbers", fontsize=18, fontweight = "bold")

            self.ax.figure.savefig(f"{SAVE_PATH}//{title}_matrix_species-functionality_heat_map_from_column_{self.plot_range_values_list[m]}_to_{self.plot_range_values_list[m+1]}.png", bbox_inches = 'tight')
            
            plt.show()
            self.new_labels_list = []

    '''
    It visualizes the itemset length and its frequency of all itemsets
    '''  
    def visualize_itemset_stats(self, output_name, output_name_2, **file_names):
        self.all_itemsets_stat_df = pd.DataFrame()
        self.closed_itemsets_stat_df = pd.DataFrame()
        self.max_frequent_itemsets_stat_df = pd.DataFrame()
        self.subset_dataframe = pd.DataFrame()
        self.subset_dataframe_2 = pd.DataFrame()
        self.final_dataframe = pd.DataFrame()

        for self.key, self.file in file_names.items(): 
            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'All itemsets stat')
                self.all_itemsets_stat_df = self.get_visualisation_dataframe()
                self.all_itemsets_stat_df["length"] = self.all_itemsets_stat_df.index.values
                self.all_itemsets_stat_df.reset_index(drop = True, inplace = True)
                self.all_itemsets_stat_df["Category I"] = self.key
                self.all_itemsets_stat_df["Category II"] = 'frequent_itemsets'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The All itemsets stat sheet is empty')
            except:
                print('The input file or input sheet is does not exist')

            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'Closed itemsets stat')
                self.closed_itemsets_stat_df = self.get_visualisation_dataframe()
                self.closed_itemsets_stat_df["length"] = self.closed_itemsets_stat_df.index.values
                self.closed_itemsets_stat_df.reset_index(drop = True, inplace = True)
                self.closed_itemsets_stat_df["Category I"] = self.key
                self.closed_itemsets_stat_df["Category II"] = 'closed_itemsets'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The Closed itemsets stat sheet is empty')
            except:
                print('The input file or input sheet is does not exist')

            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'Max frequent itemsets stat')
                self.max_frequent_itemsets_stat_df = self.get_visualisation_dataframe()
                self.max_frequent_itemsets_stat_df["length"] = self.max_frequent_itemsets_stat_df.index.values
                self.max_frequent_itemsets_stat_df.reset_index(drop = True, inplace = True)
                self.max_frequent_itemsets_stat_df["Category I"] = self.key
                self.max_frequent_itemsets_stat_df["Category II"] = 'max_frequent_itemsets'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The Max frequent itemsets stat sheet is empty')
            except:
                print('The input file or input sheet is does not exist')

            if self.get_itemset_stats_dataframe().shape[0] == 0:
                self.set_itemset_stats_dataframe(self.all_itemsets_stat_df)
            else:
                self.set_itemset_stats_dataframe(pd.merge(self.get_itemset_stats_dataframe(), self.all_itemsets_stat_df, left_index = False, right_index = False, how = 'outer'))
                
            if self.get_itemset_stats_dataframe().shape[0] == 0:
                self.set_itemset_stats_dataframe(self.closed_itemsets_stat_df)
            else:
                self.set_itemset_stats_dataframe(pd.merge(self.get_itemset_stats_dataframe(), self.closed_itemsets_stat_df, left_index = False, right_index = False, how = 'outer'))
            
            self.set_itemset_stats_dataframe(pd.merge(self.get_itemset_stats_dataframe(), self.max_frequent_itemsets_stat_df, left_index = False, right_index = False, how = 'outer'))

            self.all_itemsets_stat_df = pd.DataFrame()
            self.closed_itemsets_stat_df = pd.DataFrame()
            self.max_frequent_itemsets_stat_df = pd.DataFrame()
               
        for unique_item in self.get_itemset_stats_dataframe()["Category II"].unique():
            self.subset_dataframe = self.get_itemset_stats_dataframe().loc[self.get_itemset_stats_dataframe()["Category II"] == unique_item]
            self.subset_dataframe.reset_index(drop = True, inplace = True)
            
            self.unique_category_I = []
            self.unique_length = []
    
            for item in self.subset_dataframe["Category I"].unique():
                self.subset_dataframe_2 = self.subset_dataframe.loc[self.subset_dataframe["Category I"]== item]
                self.subset_dataframe_2.sort_values(by=['length'], inplace = True)
                for item in self.subset_dataframe_2['length'].unique():
                    if item not in self.unique_length:
                        self.unique_length.append(item)
                for item in self.subset_dataframe_2['Category I'].unique():
                    if item not in self.unique_category_I:
                        self.unique_category_I.append(item)                
            self.final_dataframe = pd.DataFrame(columns = self.unique_length, index = self.unique_category_I)
            
            self.unique_category_I = []
            self.unique_length = []

            for i, item in enumerate(self.subset_dataframe["Category I"]):
               self.final_dataframe.at[item, self.subset_dataframe.at[i, 'length']] = self.subset_dataframe.at[i, 'count']

            self.final_dataframe = self.final_dataframe[sorted(self.final_dataframe.columns)]
            self.final_dataframe.to_csv(f"{SAVE_PATH}//{output_name}_{unique_item}_stats_merged.csv")

            self.column_width = 0.15
            self.column_factor = 0
            fig, ax = plt.subplots(figsize=(25, 10), layout='constrained')
            for item in self.final_dataframe.index.values:
                self.offset = self.column_width * self.column_factor
                self.x_values = np.arange(len(self.final_dataframe.columns.values))
                rects = ax.bar(x = self.x_values + self.offset, width = self.column_width, height = self.final_dataframe.loc[item], label = item)
                ax.bar_label(rects, padding=3, fontsize = 14, rotation = 45)
                self.column_factor += 1

            ax.set_xlabel(f"{unique_item} length", fontsize=22, fontweight = "bold")
            ax.set_ylabel('Count numbers', fontsize=22, fontweight = "bold")
            ax.set_title(f"{output_name} - count numbers per {unique_item} length {output_name_2}", fontsize=28, fontweight = "bold")
            ax.set_xticks(self.x_values + self.column_width, self.final_dataframe.columns.values)
            ax.legend(loc='upper right', ncols=3, fontsize = 18)
            plt.tick_params(axis = 'both', which ='major', labelsize = 18)
            plt.show()

            ax.figure.savefig(f"{SAVE_PATH}//{output_name}_{unique_item}_stats_merged.png", bbox_inches = 'tight')
            

            self.subset_dataframe = pd.DataFrame()
            self.subset_dataframe_2 = pd.DataFrame()
            self.final_dataframe = pd.DataFrame()

        self.set_itemset_stats_dataframe(pd.DataFrame())
        
    '''
    It visualizes the frequency of items in closed itemsets.
    '''
    def visualise_by_item(self, output_name, file_name_species, file_name_functionalty, input_sheet):
        self.species_itemsets_by_item = pd.DataFrame()
        self.functionality_itemsets_by_item = pd.DataFrame()
        self.color_list = []
        
        try:
            self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = file_name_species, input_sheet = input_sheet)
            self.species_itemsets_by_item = copy.deepcopy(self.get_visualisation_dataframe()[['item', 'count']])
            self.species_itemsets_by_item['label'] = 'species'
            self.set_visualisation_dataframe(pd.DataFrame())

        except:
            print('The species input file or input sheet is does not exist')

        try:
            self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = file_name_functionalty, input_sheet = input_sheet)
            self.functionality_itemsets_by_item = copy.deepcopy(self.get_visualisation_dataframe()[['item', 'count']])
            self.functionality_itemsets_by_item['label'] = 'functionality'
            self.set_visualisation_dataframe(pd.DataFrame())

        except:
            print('The functionality input file or input sheet is does not exist')


        self.set_visualisation_dataframe(self.species_itemsets_by_item)
        self.set_visualisation_dataframe(pd.merge(self.get_visualisation_dataframe(), self.functionality_itemsets_by_item, left_index = False, right_index = False, how = 'outer'))
        
        for item in self.get_visualisation_dataframe()['label']:
            if item == 'species':
                self.color_list.append('b')
            else:
                self.color_list.append('r')

        self.get_visualisation_dataframe().to_csv(f"{SAVE_PATH}//{output_name}_visualised_by_item.csv")

        self.fig, self.ax = plt.subplots(figsize=(25, 10), layout='constrained')
        self.rects = self.ax.bar(self.get_visualisation_dataframe()['item'], self.get_visualisation_dataframe()['count'], label = self.get_visualisation_dataframe()['label'], color = self.color_list)
        self.ax.set_xlabel("Species/functionalities", fontsize=22, fontweight = "bold")
        self.ax.set_ylabel("Count numbers", fontsize=22, fontweight = "bold")
        self.ax.set_title(f"Count numbers of species/functionalities - {output_name}", fontsize=28, fontweight = "bold")
        plt.tick_params(axis = 'y', which ='major', labelsize = 18)
        plt.tick_params(axis = 'x', which ='major', labelsize = 18, rotation= 90)
        self.ax.bar_label(self.rects, padding=3, fontsize = 14)
        plt.show()
        
        self.color_list = []
        self.ax.figure.savefig(f"{SAVE_PATH}//{output_name}_visualised_by_item.png", bbox_inches = 'tight')
        
    '''
    It visualizes jaccard similarity of samples based on the items in their closed itemsets.
    '''
    def visualise_jaccard_similarity(self, extension, input_file, title, input_sheet = ""):
        self.final_dataframe = pd.DataFrame(columns = ['items'])
        self.plot_rows = 0
        self.plot_range_values_list = []
        self.temp_list = []

        if extension == 'csv':
            self.read_in_csv_for_visualisation(extension = extension, input_file = input_file)
            
        elif extension == 'xlsx':
            self.read_in_excel_for_visualisation(extension = extension, input_file = input_file, input_sheet = input_sheet)
                
        self.final_dataframe = pd.DataFrame(index = self.get_visualisation_dataframe().index.values)

        for i, item in enumerate(self.get_visualisation_dataframe().columns):
            self.get_visualisation_dataframe().columns.values[i] = item.replace('#', ' ')
            self.get_visualisation_dataframe().columns.values[i] = self.get_visualisation_dataframe().columns.values[i].replace('$', ' ')

        for i, member in enumerate(self.get_visualisation_dataframe().index.values):
            for item in self.get_visualisation_dataframe().columns:
                if self.get_visualisation_dataframe().at[member, item] == True:
                    self.split_item = item.split()
                    for subitem in self.split_item:
                        if subitem not in self.temp_list:
                            self.temp_list.append(item)
            self.final_dataframe.at[i, 'items'] = self.temp_list
            self.temp_list = []
            
        self.set_visualisation_dataframe(pd.DataFrame(columns = self.final_dataframe.index.values, index = self.final_dataframe.index.values))
        
        for i, item in enumerate(self.final_dataframe['items']):
            for j, member in enumerate(self.final_dataframe['items']):
                self.intersection = len(set(item).intersection(set(member)))
                self.union = len(set(item).union(set(member)))
                self.jaccard_similarity = self.intersection/self.union
                self.get_visualisation_dataframe().at[i, j] = round(self.jaccard_similarity,4)
        
        self.get_visualisation_dataframe().to_csv(f"{SAVE_PATH}//{title}_species-functionality_jaccard_similarity_matrix.csv")
        
        self.set_visualisation_dataframe(self.get_visualisation_dataframe().astype('float64'))
        self.fig, self.ax = plt.subplots(figsize=(15, 15), layout='constrained')
        self.ax = sns.heatmap(self.get_visualisation_dataframe(),  annot=True, fmt=".2f", vmin = 0, vmax = 1, annot_kws={"fontsize": 8}, cbar_kws={"shrink": 0.5})
        self.ax.set_xlabel(xlabel = 'Sample number', fontsize = 18)
        self.ax.set_ylabel(ylabel = 'Sample number', fontsize = 18)
        self.ax.set_title(label = 'Jaccard similarity of closed itemsets of species and functionalities', fontsize = 24)

        self.ax.figure.savefig(f"{SAVE_PATH}//{title}_species-functionality_jaccard_similarity_heatmap.png")

    '''
    It visualizes itemseth length and frequency for different confidence values
    '''
    def visualize_association_rules_stats(self, output_name, output_name_2, **file_names):
        self.all_association_rules_stat_df = pd.DataFrame()
        self.closed_association_rules_stat_df = pd.DataFrame()
        self.max_frequent_association_rules_stat_df = pd.DataFrame()
        self.subset_dataframe = pd.DataFrame()
        self.final_dataframe = pd.DataFrame()
        self.new_index_list = []
        self.new_index = ""
        

        for self.key, self.file in file_names.items(): 

            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'Association rules stat')
                self.all_association_rules_stat_df = self.get_visualisation_dataframe()

                for i, item in enumerate(self.all_association_rules_stat_df.index.values):
                    if np.isnan(item):
                        self.k = 1
                        while np.isnan(self.all_association_rules_stat_df.index.values[i-self.k]) == False:
                            self.new_index = int(self.all_association_rules_stat_df.index.values[int(i)-int(self.k)])
                            self.k += 1
                        self.new_index_list.append(self.new_index)
                    else:
                        self.new_index_list.append(item)
                

                self.all_association_rules_stat_df["length_antecedents"] = self.new_index_list
                self.all_association_rules_stat_df["total_length"] = self.all_association_rules_stat_df["length_antecedents"] + self.all_association_rules_stat_df["length_consequents"]
                self.new_index_list = []
                self.all_association_rules_stat_df.reset_index(drop = True, inplace = True)
                self.all_association_rules_stat_df["Category I"] = self.key
                self.all_association_rules_stat_df["Category II"] = 'all_association_rules'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The Association rules stat sheet is empty')
            except:
                print('The input file or input sheet does not exist')

        
            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'Closed assoc. rules stat')
                self.closed_association_rules_stat_df = self.get_visualisation_dataframe()

                for i, item in enumerate(self.closed_association_rules_stat_df.index.values):
                    if np.isnan(item):
                        self.k = 1
                        while np.isnan(self.closed_association_rules_stat_df.index.values[i-self.k]) == False:
                            self.new_index = int(self.closed_association_rules_stat_df.index.values[int(i)-int(self.k)])
                            self.k += 1
                        self.new_index_list.append(self.new_index)
                    else:
                        self.new_index_list.append(item)
                
                self.closed_association_rules_stat_df["length_antecedents"] = self.new_index_list
                self.closed_association_rules_stat_df["total_length"] = self.closed_association_rules_stat_df["length_antecedents"] + self.closed_association_rules_stat_df["length_consequents"]
                self.new_index_list = []
                self.closed_association_rules_stat_df.reset_index(drop = True, inplace = True)
                self.closed_association_rules_stat_df["Category I"] = self.key
                self.closed_association_rules_stat_df["Category II"] = 'closed_association_rules'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The Closed assoc. rules stat sheet is empty')
            except:
                print('The input file or input sheet does not exist')

            
            try:
                self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = self.file, input_sheet = 'Max freq. assoc. rules stat')
                self.max_frequent_association_rules_stat_df = self.get_visualisation_dataframe()

                for i, item in enumerate(self.max_frequent_association_rules_stat_df.index.values):
                    if np.isnan(item):
                        self.k = 1
                        while np.isnan(self.max_frequent_association_rules_stat_df.index.values[i-self.k]) == False:
                            self.new_index = int(self.max_frequent_association_rules_stat_df.index.values[int(i)-int(self.k)])
                            self.k += 1
                        self.new_index_list.append(self.new_index)
                    else:
                        self.new_index_list.append(item)
                
                self.max_frequent_association_rules_stat_df["length_antecedents"] = self.new_index_list
                self.max_frequent_association_rules_stat_df["total_length"] = self.max_frequent_association_rules_stat_df["length_antecedents"] + self.max_frequent_association_rules_stat_df["length_consequents"]
                self.new_index_list = []
                self.max_frequent_association_rules_stat_df.reset_index(drop = True, inplace = True)
                self.max_frequent_association_rules_stat_df["Category I"] = self.key
                self.max_frequent_association_rules_stat_df["Category II"] = 'max_frequent_association_rules'
                if self.get_visualisation_dataframe().shape[0] == 0:
                    print('The Max freq. assoc. rules stat sheet is empty')
            except:
                print('The input file or input sheet does not exist')

            


            if self.get_association_stats_dataframe().shape[0] == 0:
                self.set_association_stats_dataframe(self.all_association_rules_stat_df)
            else:
                self.set_association_stats_dataframe(pd.merge(self.get_association_stats_dataframe(), self.all_association_rules_stat_df, left_index = False, right_index = False, how = 'outer'))
                
            if self.get_association_stats_dataframe().shape[0] == 0:
                self.set_association_stats_dataframe(self.closed_association_rules_stat_df)
            else:
                self.set_association_stats_dataframe(pd.merge(self.get_association_stats_dataframe(), self.closed_association_rules_stat_df, left_index = False, right_index = False, how = 'outer'))
            
            try:
                self.set_association_stats_dataframe(pd.merge(self.get_association_stats_dataframe(), self.max_frequent_association_rules_stat_df, left_index = False, right_index = False, how = 'outer'))
            except:
                print('Max frequent stats sheet is empty')

            
            self.all_association_rules_stat_df = pd.DataFrame()
            self.closed_association_rules_stat_df = pd.DataFrame()
            self.max_frequent_association_rules_stat_df = pd.DataFrame()

        
        for unique_item in self.get_association_stats_dataframe()["Category II"].unique():
            self.subset_dataframe = self.get_association_stats_dataframe().loc[self.get_association_stats_dataframe()["Category II"] == unique_item]
            self.subset_dataframe.to_csv(f"{SAVE_PATH}//test_{unique_item}.csv")
            self.subset_dataframe.reset_index(drop = True, inplace = True)

            
            self.subset_dataframe.drop(['total_length','Category II'], axis = 1, inplace = True)
            self.final_dataframe = self.subset_dataframe.groupby(by=['Category I', 'length_consequents', 'length_antecedents']).sum()

            self.new_index_list = []
            self.colour_list = []
            self.colors_dict = {}

            for item in self.final_dataframe.index.values:
                self.colour_list.append(item[0])
            cmap = mpl.colormaps['tab20c']
            self.colors = cmap(np.linspace(0, 1, len(np.unique(self.colour_list))))
            for i, item in enumerate(self.colors):
                self.colors_dict[f'{np.unique(self.colour_list)[i]}'] = item
            self.colour_list = []
            
            
            for item in self.final_dataframe.index.values:
                self.label = item[0] + "_" + "conseq_" + str(item[1]) + "_" + "anteced_" + str(int(item[2]))
                self.new_index_list.append(self.label)
                self.colour_list.append(self.colors_dict.get(item[0]))
            self.final_dataframe.index = self.new_index_list

            self.final_dataframe = self.final_dataframe[sorted(self.final_dataframe.columns)]
            self.final_dataframe.to_csv(f"{SAVE_PATH}//{output_name}_{unique_item}_stats_merged.csv")

            self.column_width = 0.15
            self.column_factor = 0
            fig, ax = plt.subplots(figsize=(50, 20), layout='constrained')
            self.x_values = np.arange(len(self.final_dataframe['count']))
            for i, item in enumerate(self.final_dataframe.index.values):
                self.offset = 0
                rects = ax.bar(x = self.x_values[self.column_factor] + self.offset, width = self.column_width, height = self.final_dataframe.loc[item], label = item, color = self.colour_list[i])
                ax.bar_label(rects, padding=3, fontsize = 16, rotation = 45, fontweight = "bold")
                self.column_factor += 1
            ax.set_xlabel(f"{unique_item} length", fontsize=22, fontweight = "bold")
            ax.set_ylabel('Count numbers', fontsize=22, fontweight = "bold")
            ax.set_title(f"{output_name} - count numbers per {unique_item} total length {output_name_2}", fontsize=28, fontweight = "bold")
            ax.set_xticks(self.x_values + self.column_width, self.final_dataframe.index.values, rotation = 90, fontsize = 8)
            plt.tick_params(axis = 'both', which ='major', labelsize = 20)
            plt.tight_layout()
            plt.show()

            ax.figure.savefig(f"{SAVE_PATH}//{output_name}_{unique_item}_stats_merged.png", bbox_inches = 'tight')

            self.subset_dataframe = pd.DataFrame()
            self.final_dataframe = pd.DataFrame()
            
        self.set_association_stats_dataframe(pd.DataFrame())
        
    '''
    It visualizes support and confidence when all samples were mined together
    '''
    def visualize_support_confidence_all_mined(self, input_species_association_rules_file, input_species_association_rules_sheet,
                                      input_functinality_association_rules_file, input_functinality_association_rules_sheet):

        self.species_dataframe = pd.DataFrame()
        self.functionality_dataframe = pd.DataFrame()
        self.final_dataframe = pd.DataFrame()
        self.split_ant_item = ''
        self.split_con_item = ''
        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_species_association_rules_file, input_sheet = input_species_association_rules_sheet)
        self.species_dataframe = self.get_visualisation_dataframe()
        self.species_dataframe['closed_antecedents_consequents'] = "N/A"
        self.species_dataframe['numbers'] = np.arange(1, len(self.species_dataframe['closed_antecedents']) + 1)
        self.species_dataframe['category'] = 'species' 
        
        for i, self.ant_item in enumerate(self.species_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.species_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.species_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.species_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.species_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_functinality_association_rules_file, input_sheet = input_functinality_association_rules_sheet)
        self.functionality_dataframe = self.get_visualisation_dataframe()
        self.functionality_dataframe['closed_antecedents_consequents'] = "N/A"
        self.functionality_dataframe['numbers'] = np.arange(len(self.species_dataframe['closed_antecedents']), len(self.species_dataframe['closed_antecedents']) + len(self.functionality_dataframe['closed_antecedents'])) 
        self.functionality_dataframe['category'] = 'functionality'
        

        for i, self.ant_item in enumerate(self.functionality_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.functionality_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.functionality_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.functionality_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.functionality_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.functionality_dataframe['new_index'] = np.arange(len(self.species_dataframe['closed_antecedents']), len(self.species_dataframe['closed_antecedents']) + len(self.functionality_dataframe['closed_antecedents']))
        self.functionality_dataframe.set_index("new_index", inplace = True)
        
        self.final_dataframe = pd.concat([self.species_dataframe, self.functionality_dataframe])
        self.labels = self.final_dataframe['numbers']

        fig = plt.figure(figsize=(15, 15), layout='constrained')
        ax = plt.axes(projection='3d')


        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'species']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'species']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'species']['confidence']

        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, label = 'species',marker = MarkerStyle("o", fillstyle="top"), color = 'red')
        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'functionality']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'functionality']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'functionality']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, label = 'functionality',marker = MarkerStyle("D", fillstyle="bottom"), color = 'blue')


        self.x_values = self.final_dataframe['antecedent support']
        self.y_values = self.final_dataframe['consequent support']
        self.z_values = self.final_dataframe['confidence']

        self.final_dataframe.to_csv(f"{SAVE_PATH}//all_mined_support_lift_scatter_data.csv")

          
        ax.set_xlabel('Antecedent support', fontsize=18, fontweight = "bold")
        ax.set_ylabel('Consequent support', fontsize=18, fontweight = "bold")
        ax.set_zlabel('Confidence', fontsize=18, fontweight = "bold")
        ax.set_title('Antecedent support/Consequent support/Confidence - species+functionalities', fontsize=20, fontweight = "bold")

        #for i, item in enumerate(self.labels):
        #    ax.text(x = self.x_values[i], y = self.y_values[i], z = self.z_values[i], s = item, fontsize = '6', rotation = 'vertical', ha = 'right', va = 'bottom')
        
        ax.legend()
        plt.tight_layout()
        plt.show()
        ax.figure.savefig(f"{SAVE_PATH}//all_mined_support_lift_scatter.png", bbox_inches = 'tight')

    '''
    It visualizes support and confidence when healthy and ill samples were mined separately
    '''
    def visualize_support_confidence_healthy_IBD_mined(self, input_healthy_species_association_rules_file, input_healthy_species_association_rules_sheet,
                                                       input_ill_species_association_rules_file, input_ill_species_association_rules_sheet,
                                                       input_healthy_functinality_association_rules_file, input_healthy_functinality_association_rules_sheet,
                                                       input_ill_functinality_association_rules_file, input_ill_functinality_association_rules_sheet):
                                      

        self.healthy_species_dataframe = pd.DataFrame()
        self.ill_species_dataframe = pd.DataFrame()
        self.healthy_functionality_dataframe = pd.DataFrame()
        self.ill_functionality_dataframe = pd.DataFrame()
        self.species_dataframe = pd.DataFrame()
        self.functionality_dataframe = pd.DataFrame()
        self.final_dataframe = pd.DataFrame()
        self.split_ant_item = ''
        self.split_con_item = ''

        
        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_healthy_species_association_rules_file, input_sheet = input_healthy_species_association_rules_sheet)
        self.healthy_species_dataframe = self.get_visualisation_dataframe()
        self.healthy_species_dataframe['closed_antecedents_consequents'] = "N/A"
        self.healthy_species_dataframe['numbers'] = np.arange(1, len(self.healthy_species_dataframe['closed_antecedents']) + 1)
        self.healthy_species_dataframe['category'] = 'healthy sample species' 
        
        for i, self.ant_item in enumerate(self.healthy_species_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.healthy_species_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.healthy_species_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.healthy_species_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.healthy_species_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_ill_species_association_rules_file, input_sheet = input_ill_species_association_rules_sheet)
        self.ill_species_dataframe = self.get_visualisation_dataframe()
        self.ill_species_dataframe['closed_antecedents_consequents'] = "N/A"
        self.ill_species_dataframe['numbers'] = np.arange(len(self.healthy_species_dataframe['closed_antecedents']), len(self.healthy_species_dataframe['closed_antecedents']) + len(self.ill_species_dataframe['closed_antecedents']))
        self.ill_species_dataframe['category'] = 'ill sample species' 
        
        for i, self.ant_item in enumerate(self.ill_species_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.ill_species_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.ill_species_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.ill_species_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.ill_species_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.ill_species_dataframe['new_index'] = np.arange(len(self.healthy_species_dataframe['closed_antecedents']), len(self.healthy_species_dataframe['closed_antecedents']) + len(self.ill_species_dataframe['closed_antecedents']))
        self.ill_species_dataframe.set_index("new_index", inplace = True)

        self.species_dataframe = pd.concat([self.healthy_species_dataframe, self.ill_species_dataframe])
        self.temp_species_dataframe = copy.deepcopy(self.species_dataframe)
        for i, item in enumerate(self.temp_species_dataframe['closed_antecedents_consequents']):
            self.new_item = ''.join(str(x) for x in sorted(item))
            for j, subitem in enumerate(self.temp_species_dataframe['closed_antecedents_consequents']):
                self.new_subitem = ''.join(str(y) for y in sorted(subitem))
                if self.new_item == self.new_subitem:
                    if i != j:
                        self.species_dataframe.at[i, 'category'] = 'healthy ill sample species'
        
        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_healthy_functinality_association_rules_file, input_sheet = input_healthy_functinality_association_rules_sheet)
        self.healthy_functionality_dataframe = self.get_visualisation_dataframe()
        self.healthy_functionality_dataframe['closed_antecedents_consequents'] = "N/A"
        self.healthy_functionality_dataframe['numbers'] = np.arange(1, len(self.healthy_functionality_dataframe['closed_antecedents']) + 1)
        self.healthy_functionality_dataframe['category'] = 'healthy sample functionality'

        for i, self.ant_item in enumerate(self.healthy_functionality_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.healthy_functionality_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.healthy_functionality_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.healthy_functionality_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.healthy_functionality_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.read_in_excel_for_visualisation(extension = 'xlsx', input_file = input_ill_functinality_association_rules_file, input_sheet = input_ill_functinality_association_rules_sheet)
        self.ill_functionality_dataframe = self.get_visualisation_dataframe()
        self.ill_functionality_dataframe['closed_antecedents_consequents'] = "N/A"
        self.ill_functionality_dataframe['numbers'] = np.arange(len(self.healthy_functionality_dataframe['closed_antecedents']), len(self.healthy_functionality_dataframe['closed_antecedents']) + len(self.ill_functionality_dataframe['closed_antecedents']))
        self.ill_functionality_dataframe['category'] = 'ill sample functionality'

        for i, self.ant_item in enumerate(self.ill_functionality_dataframe['closed_antecedents']):
            self.temp_ant_con_list = []
            self.temp_ant_list = []
            self.temp_con_list = []
            
            self.ant_item = self.ant_item.replace("frozenset({", "")
            self.ant_item = self.ant_item.replace("})", "")
            self.ant_item = self.ant_item.replace(",", "")
            self.ant_item = self.ant_item.replace("'", "")
            self.split_ant_item = self.ant_item.split(' ')
            for self.sub_ant_item in self.split_ant_item:
                self.temp_ant_list.append('#ANT_' + self.sub_ant_item)
                self.temp_ant_con_list.append('#ANT_' + self.sub_ant_item)
                
            self.con_item = self.ill_functionality_dataframe.at[i, 'closed_consequents']
            self.con_item = self.con_item.replace("frozenset({", "")
            self.con_item = self.con_item.replace("})", "")
            self.con_item = self.con_item.replace(",", "")
            self.con_item = self.con_item.replace("'", "")
            self.split_con_item = self.con_item.split(' ')
            for self.sub_con_item in self.split_con_item:
                self.temp_con_list.append('#CON_' + self.sub_con_item)
                self.temp_ant_con_list.append('#CON_' + self.sub_con_item)
            self.ill_functionality_dataframe.at[i, 'closed_antecedents'] = self.temp_ant_list
            self.ill_functionality_dataframe.at[i, 'closed_consequents'] = self.temp_con_list
            self.ill_functionality_dataframe.at[i, 'closed_antecedents_consequents'] = self.temp_ant_con_list

        self.ill_functionality_dataframe['new_index'] = np.arange(len(self.healthy_functionality_dataframe['closed_antecedents']), len(self.healthy_functionality_dataframe['closed_antecedents']) + len(self.ill_functionality_dataframe['closed_antecedents']))
        self.ill_functionality_dataframe.set_index("new_index", inplace = True)
        
        self.functionality_dataframe = pd.concat([self.healthy_functionality_dataframe, self.ill_functionality_dataframe])
        self.functionality_dataframe['new_index'] = np.arange(len(self.species_dataframe['closed_antecedents']), len(self.species_dataframe['closed_antecedents']) + len(self.functionality_dataframe['closed_antecedents']))
        self.functionality_dataframe['numbers'] = np.arange(len(self.species_dataframe['closed_antecedents']), len(self.species_dataframe['closed_antecedents']) + len(self.functionality_dataframe['closed_antecedents']))
        self.functionality_dataframe.set_index("new_index", inplace = True)

        self.temp_functionality_dataframe = copy.deepcopy(self.functionality_dataframe)
        for i, item in enumerate(self.temp_functionality_dataframe['closed_antecedents_consequents']):
            self.new_item = ''.join(str(x) for x in sorted(item))
            for j, subitem in enumerate(self.temp_functionality_dataframe['closed_antecedents_consequents']):
                self.new_subitem = ''.join(str(y) for y in sorted(subitem))
                if self.new_item == self.new_subitem:
                    if i != j:
                        self.functionality_dataframe.at[len(self.species_dataframe['closed_antecedents_consequents']) + i, 'category'] = 'healthy ill sample functionality'
        
        self.final_dataframe = pd.concat([self.species_dataframe, self.functionality_dataframe])
        self.final_dataframe.to_csv(f"{SAVE_PATH}//healthy_ill_mined_support_lift_scatter_data.csv")
        
        self.labels = self.final_dataframe['numbers']

        fig = plt.figure(figsize=(15, 15), layout='constrained')
        ax = plt.axes(projection='3d')

        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample species']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample species']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample species']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("o", fillstyle="top"), label = 'healthy sample species', color = 'red')
        
        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample species']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample species']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample species']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("o", fillstyle="bottom"), label = 'ill sample species', color = 'green')

        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample species']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample species']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample species']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("o", fillstyle="left"), label = 'healthy ill sample species', color = 'blue')

        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample functionality']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample functionality']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy sample functionality']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("D", fillstyle="top"), label = 'healthy sample functionality', color = 'red')

        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample functionality']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample functionality']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'ill sample functionality']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("D", fillstyle="bottom"), label = 'ill sample functionalit', color = 'green')

        self.x_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample functionality']['antecedent support']
        self.y_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample functionality']['consequent support']
        self.z_values = self.final_dataframe.loc[self.final_dataframe['category'] == 'healthy ill sample functionality']['confidence']
        ax.scatter(self.x_values, self.y_values, self.z_values, s = 50, marker = MarkerStyle("D", fillstyle="left"), label = 'healthy ill sample functionality', color = 'blue')

        self.x_values = self.final_dataframe['antecedent support']
        self.y_values = self.final_dataframe['consequent support']
        self.z_values = self.final_dataframe['confidence']
        
        ax.set_xlabel('Antecedent support', fontsize=18, fontweight = "bold")
        ax.set_ylabel('Consequent support', fontsize=18, fontweight = "bold")
        ax.set_zlabel('Confidence', fontsize=18, fontweight = "bold")
        ax.set_title('Antecedent support/Consequent support/Confidence - healthy-ill species/functionalities', fontsize=20, fontweight = "bold")
        ax.figure.savefig(f"{SAVE_PATH}//healthy_ill_mined_support_lift_scatter.png", bbox_inches = 'tight')
        
        #for i, item in enumerate(self.labels):
        #    ax.text(x = self.x_values[i], y = self.y_values[i], z = self.z_values[i], s = item, rotation = 'vertical', fontsize = '6', ha = 'right', va = 'bottom')
        plt.legend()
        plt.tight_layout()
        plt.show()

vis = Visualisation()
try:
    input_commands_file = open(f"{SAVE_PATH}//visualisation_input_commands.txt", "r")
except:
    print("The visualisation_input_commands.txt file is missing")
input_commands_file_content = input_commands_file.readlines()
for line_number, input_commands_file_content_line in enumerate(input_commands_file_content):
    if input_commands_file_content_line[0] == "#":
        pass
    elif input_commands_file_content_line[0] == "\n":
        pass
    elif input_commands_file_content_line[0] == "":
        pass
    elif input_commands_file_content_line[0] == " ":
        print(f"A whitespace is present at line {line_number}, please delete it.")
    else:
        print(f"Command {input_commands_file_content_line} is running.")
        eval(f"vis.{input_commands_file_content_line}")
try:
    input_commands_file.close()
except:
    print("The input_commands_file can't be closed")