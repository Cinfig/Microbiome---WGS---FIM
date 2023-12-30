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
import Connector_MGnify as Conn

SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output"

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
            
            '''
            lost code
            '''
    
    # This implementatio runs into memory problem for real data     
    def apriori(self):
        func_df = pd.read_csv("//Users//adamveszpremi//Desktop//MSc project work//Code//function.csv")
        func_df = pd.get_dummies(func_df, sparse = True)
        dropped_func_df = func_df.drop(func_df.index[0:28])
        dropped_func_df = dropped_func_df.drop(func_df.columns[0:20380], axis = 1)
        frequent_itemsets = apriori(dropped_func_df, min_support = 0.6, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_excel('test_mining.xlsx')
        print(frequent_itemsets)
    
class Apriori:
       
    def run_transactional_database(self):
        self.tax_dataframe = pd.read_csv(f'{SAVE_PATH}/transactional_db_functionalities_.csv')
        frequent_itemsets = apriori(self.tax_dataframe, min_support = 0.6, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        frequent_itemsets.to_excel('test_mining.xlsx')
        
        

#generate = Generate_dummy_df()
#generate.generate_df()
#generate.apriori()

ap = Apriori()
ap.run_transactional_database()



















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