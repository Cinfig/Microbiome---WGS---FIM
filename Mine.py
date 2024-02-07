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
        
        
        self.func_dataframe.to_csv(f"{SAVE_PATH}/filtered_transaction_dataset_{input_file}_abundance_threshold_{abundance_threshold}.csv")
        
        
        frequent_itemsets = apriori(self.func_dataframe, min_support = min_support, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_csv(f"{SAVE_PATH}/apriori_mining_{input_file}_abundance_threshold_{abundance_threshold}_min_supprt_{min_support}.csv")
        print("\n Output file is saved")


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
        
        try:
            self.association_dataframe = association_rules(self.input_dataframe, metric = metric, min_threshold=metric_threshold)
            self.association_dataframe.to_csv(f"{SAVE_PATH}/association_rules_metric_{metric}_{input_file}")
            print("\n Output file is saved")
            
        except: 
            self.association_dataframe = association_rules(self.input_dataframe, support_only=True, min_threshold=0.6)
            self.association_dataframe.to_csv(f"{SAVE_PATH}/association_rules_support_only_{input_file}")
            print("\n Output file is saved with support only option")
    
ar = Association_rules()
