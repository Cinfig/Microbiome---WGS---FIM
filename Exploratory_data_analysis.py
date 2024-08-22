import pandas as pd
import numpy as np
import itertools
import copy
import os
from matplotlib import pyplot as plt
from sklearn import preprocessing
from scipy.spatial import distance
from scipy import stats
import seaborn as sns

SAVE_PATH = os.getcwd()

class EDA:
    
    def __init__(self):
        self.input_df = pd.DataFrame()
        self.output_df = pd.DataFrame()
        self.extra_columns_df = pd.DataFrame()
        self.index_list = []
        self.index_combination_list = []
        self.combination_list = []
    
    def set_input_df(self, assign):
        self.input_df = assign
    
    def get_input_df(self):
        return self.input_df
    
    def set_output_df(self, assign):
        self.output_df = assign
    
    def get_output_df(self):
        return self.output_df
    
    def set_index_list(self, assign):
        self.index_list = assign
    
    def get_index_list(self):
        return self.index_list
    
    def set_index_combination_list(self, assign):
        self.index_combination_list = assign
    
    def get_index_combination_list(self):
        return self.index_combination_list
    
    def set_combination_list(self, assign):
        self.combination_list = assign
    
    def get_combination_list(self):
        return self.combination_list 
    
    def set_extra_columns_df(self, assign):
        self.extra_columns_df = assign
    
    def get_extra_columns_df(self):
        return self.extra_columns_df
    
        
    def empty_dataframes_lists(self):
        self.set_input_df(pd.DataFrame())
        self.set_output_df(pd.DataFrame())   
        self.set_index_list([])
        self.set_index_combination_list([])
        self.set_combination_list([])

    '''
    It calculates the Alpha diversity as count numbers.
    '''
    def calculate_alpha_diversity(self, input_file, title, category_split = None):
        self.sample_number = []        
        self.alpha_richness = pd.Series(dtype = "Float64")

        try:
            self.set_input_df(pd.read_csv(f'{SAVE_PATH}/{input_file}.csv'))
        except:
            print(f"Input file is not found")
        try:
            self.set_input_df(self.get_input_df().loc[:, ~self.get_input_df().columns.str.contains('^Unnamed')])
        except:
            pass

        self.set_extra_columns_df(copy.deepcopy(self.get_input_df()))
        self.set_extra_columns_df(self.get_extra_columns_df()[['Sample_id','Secondary_sample_id','Category I','Category II','Category III']])
        self.get_input_df().drop(columns=['Sample_id','Secondary_sample_id','Category I','Category II','Category III'], inplace = True)

        for item in self.get_input_df().columns:
            for i, subitem in enumerate(self.get_input_df()[f"{item}"]):
                if str(subitem) == "0.0":
                    self.get_input_df().at[i, f"{item}"] = np.nan
                elif str(subitem) == "0":
                    self.get_input_df().at[i, f"{item}"] = np.nan

        self.alpha_richness = self.get_input_df().count(axis=1)
        for i in range(len(self.alpha_richness)):
            self.sample_number.append(i)

        self.get_output_df()['Sample number'] = self.sample_number
        self.get_output_df()['Alpha diversity'] = self.alpha_richness
        self.get_output_df().to_csv(f"{SAVE_PATH}/EDA - alpha_diversity - {title}.csv")

        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.ax.set_xlabel("Sample number")
        self.ax.set_ylabel(f"Count of {title}")
        self.ax.set_title(f"Alpha diversity - richness - {title}")
        self.ax.set_xticks(self.alpha_richness.index)
        self.ax.set_xticklabels(self.alpha_richness.index, rotation = 90)
        self.height_bars = self.ax.bar(self.alpha_richness.index, self.alpha_richness.values, align='center')
        self.ax.bar_label(self.height_bars, rotation = 45)
        self.fig.savefig(f"{SAVE_PATH}/EDA - alpha diversity - richness - {title}.png", bbox_inches='tight')

        self.fig1, self.ax1 = plt.subplots(figsize=(12, 7))
        self.ax1.set_xlabel(f"Number of samples: {len(self.alpha_richness.index)}")
        self.ax1.set_ylabel(f"Count of {title}")
        self.ax1.set_title(f"Alpha diversity - data summary - {title}")
        self.ax1.boxplot(self.alpha_richness)
        self.fig1.savefig(f"{SAVE_PATH}/EDA - alpha diversity - data summary - {title}.png", bbox_inches='tight')
        self.empty_dataframes_lists()

    '''
    It calculates the Beta diversity as Bray-Curtis.
    '''
    def calculate_beta_diversity(self, input_file, title):
        self.input_df_subset = pd.DataFrame()
        self.normalised_row = np.empty(1)
        self.combination = np.empty(1)
        self.result = np.float64
        self.braycurtis_list = []
        self.braycurtis_df = pd.DataFrame()
        self.braycurtis_df_matrix = pd.DataFrame()
        
        try:
            self.set_input_df(pd.read_csv(f'{SAVE_PATH}/{input_file}.csv'))
        except:
            print(f"Input file is not found")
        try:
            self.set_input_df(self.get_input_df().loc[:, ~self.get_input_df().columns.str.contains('^Unnamed')])
        except:
            pass

        self.get_input_df().fillna(0, inplace = True)
        self.set_extra_columns_df(copy.deepcopy(self.get_input_df()))
        self.set_extra_columns_df(self.get_extra_columns_df()[['Sample_id','Secondary_sample_id','Category I','Category II','Category III']])
        self.get_input_df().drop(columns=['Sample_id','Secondary_sample_id','Category I','Category II','Category III'], inplace = True)


        for item in self.input_df.index.values:
            self.input_df_subset = self.get_input_df()[self.get_input_df().index.values == item]
            self.normalised_row = preprocessing.normalize(self.input_df_subset)
            self.get_input_df().loc[item] = self.normalised_row

        self.set_index_list(self.get_input_df().index.to_list())
        self.set_index_combination_list(list(itertools.combinations(self.get_index_list(), 2)))
        for item in self.get_index_combination_list():
            self.combination = self.get_input_df().iloc[[item[0],item[1]]].to_numpy()
            self.get_combination_list().append(self.combination)
        
        for i, item in enumerate(self.get_combination_list()):
            self.result = distance.braycurtis(item[0], item[1])
            self.braycurtis_list.append(self.result.round(2))
        
        self.braycurtis_df['Sample combination'] = self.get_index_combination_list()
        self.braycurtis_df['Bray_curtis_value'] = self.braycurtis_list
    
        self.braycurtis_df_matrix = pd.DataFrame(index = self.get_index_list(), columns = self.get_index_list())
        for i, item in enumerate(self.braycurtis_df['Sample combination']):
            self.braycurtis_df_matrix.at[item[1], item[0]] = self.braycurtis_df.at[i,'Bray_curtis_value']
        self.braycurtis_df_matrix.fillna(0, inplace = True)
        self.braycurtis_df.to_csv(f"{SAVE_PATH}/EDA - beta_diversity - {title}.csv")

        self.fig, self.ax = plt.subplots(figsize = (15,15), layout = "constrained")
        self.mask = np.triu(np.ones_like(self.braycurtis_df_matrix, dtype = bool))
        self.ax = sns.heatmap(self.braycurtis_df_matrix, mask = self.mask, annot = True, fmt = ".2f", vmin = 0, vmax = 1, annot_kws = {"fontsize": 8}, cbar_kws = {"shrink": 0.5})
        self.ax.set_xlabel(xlabel =  "Sample number", fontsize = 18)
        self.ax.set_ylabel(ylabel =  "Sample number", fontsize = 18)
        self.ax.set_title(label = f"Beta diversity - Bray-Curtis matrix - {title}", fontsize = 24)
        self.fig.savefig(f"{SAVE_PATH}/EDA - beta diversity - Bray-Curtis - {title}.png", bbox_inches='tight')
        self.empty_dataframes_lists()

    '''
    It calculates the Jaccard similarity values between two samples.
    '''
    def calculate_jaccard_similarity(self, input_file, title):
        self.combination = np.empty(1)
        self.result = np.float64
        self.jaccard_list = []
        self.jaccard_df = pd.DataFrame()
        self.jaccard_df_matrix = pd.DataFrame()
        
        try:
            self.set_input_df(pd.read_csv(f'{SAVE_PATH}/{input_file}.csv'))
        except:
            print(f"Input file is not found")
        try:
            self.set_input_df(self.get_input_df().loc[:, ~self.get_input_df().columns.str.contains('^Unnamed')])
        except:
            pass
        self.get_input_df().fillna(0, inplace = True)
        
        self.set_extra_columns_df(copy.deepcopy(self.get_input_df()))
        self.set_extra_columns_df(self.get_extra_columns_df()[['Sample_id','Secondary_sample_id','Category I','Category II','Category III']])
        self.get_input_df().drop(columns=['Sample_id','Secondary_sample_id','Category I','Category II','Category III'], inplace = True)
        
        for item in self.get_input_df().columns:
            self.get_input_df()[f"{item}"] = np.where(self.get_input_df()[f"{item}"] > 0, 1, 0)
            
        self.set_index_list(self.get_input_df().index.to_list())
        self.set_index_combination_list(list(itertools.combinations(self.get_index_list(), 2)))
        for item in self.get_index_combination_list():
            self.combination = self.get_input_df().iloc[[item[0],item[1]]].to_numpy()
            self.get_combination_list().append(self.combination)
        
        for i, item in enumerate(self.get_combination_list()):
            self.result = distance.jaccard(item[1], item[0])
            self.jaccard_list.append(self.result.round(2))
            
        
        self.jaccard_df['Sample combination'] = self.get_index_combination_list()
        self.jaccard_df['Jaccard_similarity_value'] = self.jaccard_list
        self.jaccard_df.to_csv(f"{SAVE_PATH}/EDA - Jaccard similarity - {title}.csv")
        
        self.jaccard_df_matrix = pd.DataFrame(index = self.get_index_list(), columns = self.get_index_list())
        for i, item in enumerate(self.jaccard_df['Sample combination']):
            self.jaccard_df_matrix.at[item[1], item[0]] = self.jaccard_df.at[i,'Jaccard_similarity_value']
        self.jaccard_df_matrix.fillna(0, inplace = True)
    
        self.fig, self.ax = plt.subplots(figsize = (15,15), layout = "constrained")
        self.mask = np.triu(np.ones_like(self.jaccard_df_matrix, dtype = bool))
        self.ax = sns.heatmap(self.jaccard_df_matrix, mask = self.mask, annot = True, fmt = ".2f", vmin = 0, vmax = 1, annot_kws = {"fontsize": 8}, cbar_kws = {"shrink": 0.5})
        self.ax.set_xlabel(xlabel =  "Sample number", fontsize = 18)
        self.ax.set_ylabel(ylabel =  "Sample number", fontsize = 18)
        self.ax.set_title(label = f"Jaccard similarity - matrix - {title}", fontsize = 24)
        self.fig.savefig(f"{SAVE_PATH}/EDA - Jaccard similarity - {title}.png", bbox_inches='tight')
        self.empty_dataframes_lists()
        
    '''
    It performs the kruskal_wallis_group_test. Null hipotezis: The central tendencies are equal between the two groups. p-value limit: 0.05
    '''
    def calculate_kruskal_wallis_group_test(self, input_file, title, category_split = None):
        self.sample_number = 0
        self.present_count = 0
        self.statistic_list = []
        self.pvalue_list = []
        self.scientific_pvalue_list = []
        self.kruskal_wallis_df = pd.DataFrame()
        self.kruskal_wallis_df_filtered_1 = pd.DataFrame()
        self.kruskal_wallis_df_filtered_2 = pd.DataFrame()
        self.kruskal_wallis_df_sorted = pd.DataFrame()
        
        try:
            self.set_input_df(pd.read_csv(f'{SAVE_PATH}/{input_file}.csv'))
        except:
            print(f"Input file is not found")
        try:
            self.set_input_df(self.get_input_df().loc[:, ~self.get_input_df().columns.str.contains('^Unnamed')])
        except:
            pass
        self.get_input_df().fillna(0, inplace = True)

        self.set_extra_columns_df(copy.deepcopy(self.get_input_df()))
        self.set_extra_columns_df(self.get_extra_columns_df()[['Sample_id','Secondary_sample_id','Category I','Category II','Category III']])
        self.get_input_df().drop(columns=['Sample_id','Secondary_sample_id','Category I','Category II','Category III'], inplace = True)
            
    
        for item in self.get_input_df().columns:
            self.get_input_df()[f"{item}"] = np.where(self.get_input_df()[f"{item}"] > 0, 1, 0)
        
        self.kruskal_wallis_df_filtered_1 = copy.deepcopy(self.get_input_df())
        self.kruskal_wallis_df_filtered_2 = copy.deepcopy(self.get_input_df())
        
        self.set_index_list(np.arange(category_split + 1, dtype=int))
        self.kruskal_wallis_df_filtered_1 = self.kruskal_wallis_df_filtered_1[self.kruskal_wallis_df_filtered_1.index.isin(self.get_index_list())]
        for item in self.kruskal_wallis_df_filtered_1.columns:
            for thing in self.kruskal_wallis_df_filtered_1[item]:
                if thing == 1:
                    self.present_count += 1
            if len(self.kruskal_wallis_df_filtered_1.index.values) % 2 == 0:
                if self.present_count >= len(self.kruskal_wallis_df_filtered_1.index.values) / 2:
                    self.kruskal_wallis_df_filtered_1[item] = 1
                else:
                    self.kruskal_wallis_df_filtered_1[item] = 0
            elif len(self.kruskal_wallis_df_filtered_1.index.values) % 2 != 0:
                if self.present_count >= (len(self.kruskal_wallis_df_filtered_1.index.values) / 2) + 1:
                    self.kruskal_wallis_df_filtered_1[item] = 1
                else:
                    self.kruskal_wallis_df_filtered_1[item] = 0
            self.present_count = 0
        
        self.set_index_list(np.arange(category_split + 1, self.kruskal_wallis_df_filtered_2.index.values[-1] + 1, dtype=int))
        self.kruskal_wallis_df_filtered_2 = self.kruskal_wallis_df_filtered_2[self.kruskal_wallis_df_filtered_2.index.isin(self.get_index_list())]
        for item in self.kruskal_wallis_df_filtered_2.columns:
            for thing in self.kruskal_wallis_df_filtered_2[item]:
                if thing == 1:
                    self.present_count += 1
            if len(self.kruskal_wallis_df_filtered_2.index.values) % 2 == 0:
                if self.present_count >= len(self.kruskal_wallis_df_filtered_2.index.values) / 2:
                    self.kruskal_wallis_df_filtered_2[item] = 1
                else:
                    self.kruskal_wallis_df_filtered_2[item] = 0
            elif len(self.kruskal_wallis_df_filtered_2.index.values) % 2 != 0:
                if self.present_count >= (len(self.kruskal_wallis_df_filtered_2.index.values) / 2) +1:
                    self.kruskal_wallis_df_filtered_2[item] = 1
                else:
                    self.kruskal_wallis_df_filtered_2[item] = 0
            self.present_count = 0
        
        self.result = stats.kruskal(self.kruskal_wallis_df_filtered_1.iloc[0], self.kruskal_wallis_df_filtered_2.iloc[0])
        self.statistic_list.append(self.result.statistic.round(3))
        self.pvalue_list.append(self.result.pvalue.round(3))
        
        self.set_output_df(pd.DataFrame(columns = [['Group I vs Group II p-value', 'Meaning of the Outcome']], index = [1]))
        self.output_df['Group I vs Group II p-value'] = self.pvalue_list[0]
        if float(self.pvalue_list[0]) < 0.05:
            self.output_df['Meaning of the Outcome'] = "The Null-hypothesis is rejected, the central tendencies are not equal."
        else:
            self.output_df['Meaning of the Outcome'] = "The Null-hypothesis is accepted, the central tendencies are equal."
        
        self.output_df.to_csv(f"{SAVE_PATH}/EDA - Kruskal wallis group test - {title}.csv")
        self.empty_dataframes_lists()

eda = EDA()
try:
    eda_input_commands_file = open(f"{SAVE_PATH}/eda_input_commands.txt")
except:
    print("The eda_input_commands.txt file is missing.")
eda_input_commands_file_content = eda_input_commands_file.readlines()
for line_number, eda_input_commands_file_content_line in enumerate(eda_input_commands_file_content):
    if eda_input_commands_file_content_line[0] == "#":
        pass
    elif eda_input_commands_file_content_line[0] == "\n":
        pass
    elif eda_input_commands_file_content_line[0] == "":
        pass
    elif eda_input_commands_file_content_line[0] == " ":
        print("A whitespace is present at line {line_number}, please delete it")
    else:
        print(f"Command {eda_input_commands_file_content_line} is running.")
        eval(f"eda.{eda_input_commands_file_content_line}")
try:
    eda_input_commands_file.close()
except:
    print("The eda_input_commands.txt file can't be closed.")