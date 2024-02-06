#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 08:03:23 2023

@author: adamveszpremi
"""

import json
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

import Connector_MGnify as Conn

SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output"


    
class Apriori:
    
    def __init__(self):
        self.func_dataframe = pd.DataFrame()
        
       
    def run_transactional_database(self, abundance_threshold, min_support, input_file):
        #self.tax_dataframe = pd.read_csv(f'{SAVE_PATH}/transactional_db_functionalities_.csv')
        self.func_dataframe = pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_{input_file}.csv')
        #print(self.func_dataframe.shape)
        for item in self.func_dataframe.columns:
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] < abundance_threshold, f"{item}"] = None
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] >= abundance_threshold, f"{item}"] = True
        self.func_dataframe.dropna(axis=1, how='all', inplace = True)
        #print(self.func_dataframe.shape)
        for item in self.func_dataframe.columns:
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] != True, f"{item}"] = False
        self.func_dataframe.reset_index(drop = True, inplace=True)
        self.func_dataframe = self.func_dataframe.loc[:, ~self.func_dataframe.columns.str.contains('^Unnamed')]
        #print(self.func_dataframe.shape)
        #print(self.func_dataframe)
        
        
        self.non_unique_columns = self.func_dataframe.nunique()
        self.dropped_columns = self.non_unique_columns[self.non_unique_columns == 1].index
        self.func_dataframe.drop(self.dropped_columns, axis = 1, inplace = True)
        #print(self.func_dataframe.shape)
        
        
        self.func_dataframe.to_csv(f"{SAVE_PATH}/filtered_transaction_dataset_{input_file}_abundance_threshold_{abundance_threshold}.csv")
            #df.loc[ df[“column_name”] == “some_value”, “column_name”] = “value”
        
        
        frequent_itemsets = apriori(self.func_dataframe, min_support = min_support, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_csv(f"{SAVE_PATH}/apriori_mining_{input_file}_abundance_threshold_{abundance_threshold}_min_supprt_{min_support}.csv")
        print("\n Output file is saved")
        #frequent_itemsets.to_excel('test_mining.xlsx')


class FPGrowth:   

    def __init__(self):
        self.func_dataframe = pd.DataFrame()
        

    def run_transactional_database(self, abundance_threshold, min_support, input_file):
        self.func_dataframe = pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_{input_file}.csv')
        for item in self.func_dataframe.columns:
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] < abundance_threshold, f"{item}"] = None
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] >= abundance_threshold, f"{item}"] = True
        self.func_dataframe.dropna(axis=1, how='all', inplace = True)
        for item in self.func_dataframe.columns:
            self.func_dataframe.loc[self.func_dataframe[f"{item}"] != True, f"{item}"] = False
        self.func_dataframe.reset_index(drop = True, inplace=True)
        self.func_dataframe = self.func_dataframe.loc[:, ~self.func_dataframe.columns.str.contains('^Unnamed')]
        
        
        self.non_unique_columns = self.func_dataframe.nunique()
        self.dropped_columns = self.non_unique_columns[self.non_unique_columns == 1].index
        self.func_dataframe.drop(self.dropped_columns, axis = 1, inplace = True)
    
        frequent_itemsets = fpgrowth(self.func_dataframe, min_support = min_support, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_csv(f"{SAVE_PATH}/fpgrowth_mining_{input_file}_abundance_threshold_{abundance_threshold}_min_supprt_{min_support}.csv")
        print("\n Output file is saved")
 
class Association_rules:
    
    def __init__(self):
        self.input_dataframe = pd.DataFrame()
        self.association_dataframe = pd.DataFrame()
    
    def run_association_rules_mining(self, input_file, metric, metric_threshold):
        self.input_dataframe = pd.read_csv(f'{SAVE_PATH}/{input_file}')
        self.input_dataframe.drop(['length'], axis = 1, inplace = True)
        #print(type(self.input_dataframe))
        #self.input_dataframe = self.input_dataframe.astype(pd.SparseDtype(int, fill_value=0))
        #print(type(self.input_dataframe))
        #self.association_dataframe = association_rules(self.input_dataframe, support_only=True, min_threshold=0.6)
        #self.association_dataframe.to_csv(f"{SAVE_PATH}/association_rules_support_only_{input_file}")
        #print("\n Output file is saved with support only option")
        
        try:
            self.association_dataframe = association_rules(self.input_dataframe, metric = metric, min_threshold=metric_threshold)
            self.association_dataframe.to_csv(f"{SAVE_PATH}/association_rules_metric_{metric}_{input_file}")
            print("\n Output file is saved")
            
        except: 
            self.association_dataframe = association_rules(self.input_dataframe, support_only=True, min_threshold=0.6)
            self.association_dataframe.to_csv(f"{SAVE_PATH}/association_rules_support_only_{input_file}")
            print("\n Output file is saved with support only option")
    
ar = Association_rules()

'''
ap = Apriori()
ap.run_transactional_database(0.1, 0.6, 'go_slim')
ap.run_transactional_database(0.1, 0.6, 'go_terms')
ap.run_transactional_database(0.1, 0.6, 'interpro_identifiers')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_domain')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_class')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_order')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_phylum')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_family')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_genus')
ap.run_transactional_database(0.1, 0.6, 'taxonomy_species')
'''

'''
fp = FPGrowth()
fp.run_transactional_database(0.1, 0.6, 'go_slim')
fp.run_transactional_database(0.1, 0.6, 'go_terms')
fp.run_transactional_database(0.1, 0.6, 'interpro_identifiers')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_domain')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_class')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_order')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_phylum')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_family')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_genus')
fp.run_transactional_database(0.1, 0.6, 'taxonomy_species')
'''



#ar.run_association_rules_mining('fpgrowth_mining_go_slim_abundance_threshold_0.1_min_supprt_0.6.csv', 'confidence', 0.6)
#ar.run_association_rules_mining('fpgrowth_mining_go_slim_abundance_threshold_0.1_min_supprt_0.6.csv', 'lift', 1.2)
#ar.run_association_rules_mining('fpgrowth_mining_go_terms_abundance_threshold_0.1_min_supprt_0.6.csv', 'confidence', 0.6)
#ar.run_association_rules_mining('fpgrowth_mining_go_terms_abundance_threshold_0.1_min_supprt_0.6.csv', 'lift', 1.2)
ar.run_association_rules_mining('apriori_mining_taxonomy_phylum_abundance_threshold_0.1_min_supprt_0.6.csv', 'confidence', 0.6)











'''
def convert_to_sparse_pandas(df, exclude_columns=[]):
    df = df.copy()
    exclude_columns = set(exclude_columns)

    for (columnName, columnData) in df.iteritems():
        if columnName in exclude_columns:
            continue
        df[columnName] = pd.SparseArray(columnData.values, dtype='uint8')

    return df

func_df = pd.read_csv("//Users//adamveszpremi//Desktop//MSc project work//Code//function.csv")
print(type(func_df))
print(func_df.shape)
func_df = pd.get_dummies(func_df, sparse = True)
print(type(func_df))
print(func_df.shape)
dropped_func_df = func_df.drop(func_df.index[0:28])
dropped_func_df = dropped_func_df.drop(func_df.columns[0:20350], axis = 1)
print(type(dropped_func_df))
print(dropped_func_df.shape)
frequent_itemsets = apriori(dropped_func_df, min_support = 0.8)
print(frequent_itemsets)
'''

'''
class Generate_dummy_df:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        self.data = {}
        self.func_dataframe = pd.DataFrame()
        self.tax_dataframe = pd.DataFrame()
    
    
    
    def generate_df(self):
        with open("//Users//adamveszpremi//Downloads//mgm4989662.3.statistics.json") as openfile:
            self.data = json.load(openfile)
            print(type(self.data))
            print(self.data.keys())
            #print(self.data['function'][0])
            print(self.func_dataframe)
            self.func_dataframe = pd.DataFrame(self.data['function']).T
            self.func_dataframe.columns = self.func_dataframe.iloc[0]
            self.func_dataframe.drop(self.func_dataframe.index[[0,1]], inplace = True)
        
            print(self.func_dataframe.shape)
            
            #print(self.data['taxonomy'].keys())
            for key in self.data['taxonomy'].keys():
                self.tax_dataframe
                self.tax_dataframe.from_dict(self.data['taxonomy'][f'{key}'], orient = 'columns')
            #print(self.tax_dataframe)
            
            
            lost code
            
    
    # This implementatio runs into memory problem for real data     
    def apriori(self):
        func_df = pd.read_csv("//Users//adamveszpremi//Desktop//MSc project work//Code//function.csv")
        func_df = pd.get_dummies(func_df, sparse = True)
        dropped_func_df = func_df.drop(func_df.index[0:28])
        dropped_func_df = dropped_func_df.drop(func_df.columns[0:20380], axis = 1)
        frequent_itemsets = apriori(dropped_func_df, min_support = 0.8, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_excel('test_mining_apriori.xlsx')
        print(frequent_itemsets)
'''