#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 17:49:12 2024

@author: adamveszpremi
"""

import Connector_MGnify as Conn
import pandas as pd
import os
import numpy as np
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
SAVE_PATH = os.getcwd()
ANSWER_LIST = ['1', '2', '3', 'q']

class Connect_species_functionality:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        self.species_db_dataframe = pd.DataFrame()
        self.final_transaction_dataset_taxonomy_species = pd.DataFrame()
        self.species_and_id_df = pd.DataFrame()
        self.species_transactional_df = pd.DataFrame()
        self.go_slim_transactional_df = pd.DataFrame()
        self.new_column_list = []
        self.taxon_functionality_matrix = pd.DataFrame()
        self.goname_goid_df = pd.DataFrame()
        self.goid_list = []
        self.goname_list = []
        self.metadata_response = ""
        self.goid = ""
        self.goname = ""
        self.splitted_species = ""
        self.user_response = ""
        self.species_list = []
        self.species_list_final = []
        self.functionality_list = []
        self.functionality_list_final = []
        self.species_functionality_combination = []
        self.species_functionality_combination_final = []
        self.taxon_functionality_matrix_columns_list = []
        self.taxon_functionality_matrix_final = pd.DataFrame()
        self.temp_list = []
        
    
    def get_metadata_response(self):
        return self.metadata_response
    
    def set_metadata_response(self, assign):
        self.metadata_response = assign
    
    def set_species_db_dataframe(self, assign):
        self.species_db_dataframe = assign
    
    def get_species_db_dataframe(self):
        return self.species_db_dataframe
        
    def set_final_transaction_dataset_taxonomy_species(self, assign):
        self.final_transaction_dataset_taxonomy_species = assign
    
    def get_final_transaction_dataset_taxonomy_species(self):
        return self.final_transaction_dataset_taxonomy_species

    def set_species_and_id_df(self, assign):
        self.species_and_id_df = assign
    
    def get_species_and_id_df(self):
        return self.species_and_id_df
    
    def set_species_and_id_df_column(self, assign, column_name):
        self.species_and_id_df[f"{column_name}"] = assign
    
    def get_species_transactional_df(self):
        return self.species_transactional_df
    
    def set_species_transactional_df(self, assign):
        self.species_transactional_df = assign

    def get_go_slim_transactional_df(self):
        return self.go_slim_transactional_df
    
    def set_go_slim_transactional_df(self, assign):
        self.go_slim_transactional_df = assign
    
    def append_new_column_list(self, to_append):
        self.new_column_list.append(to_append)
    
    def get_new_column_list(self):
        return self.new_column_list
    
    def get_taxon_functionality_matrix(self):
        return self.taxon_functionality_matrix
    
    def set_taxon_functionality_matrix(self, assign):
        self.taxon_functionality_matrix = assign

    def get_goname_goid_df(self):
        return self.goname_goid_df
    
    def set_goname_goid_df(self, assign):
        self.goname_goid_df = assign
    
    def set_goname_goid_df_column(self, assign, column_name):
        self.goname_goid_df[f"{column_name}"] = assign

    def get_goid(self):
        return self.goid 
    
    def set_goid(self, assign):
        self.goid  = assign

    def get_goname(self):
        return self.goname 
    
    def set_goname(self, assign):
        self.goname  = assign

    def get_goid_list(self):
        return self.goid_list

    def append_goid_list(self, to_append):
        self.goid_list.append(to_append)
    
    def get_goname_list(self):
        return self.goname_list

    def append_goname_list(self, to_append):
        self.goname_list.append(to_append)

    def get_splitted_species(self):
        return self.splitted_species
    
    def set_splitted_species(self, assign):
        self.splitted_species = assign
    
    #def set_user_response(self, assign):
    #    self.user_response = assign
    
    #def get_user_response(self):
    #    return self.user_response

    
    '''
    It finds the taxon ID of sepcies based on their name utilizing data dump from NCBI.
    '''
    def find_species_id(self):
        try:
            self.species_db_dataframe = pd.read_csv(f'{SAVE_PATH}/names.csv', delimiter = "\t")
        except:
            print("The names.csv is not in the folder")
            
        self.set_species_db_dataframe(self.get_species_db_dataframe()[['1','all', 'synonym']])
        self.set_species_db_dataframe(self.get_species_db_dataframe().convert_dtypes(convert_string=True))
        self.get_species_db_dataframe().rename(columns = {'1':'species_id', 'all':'species', 'synonym':'tag'}, inplace = True)
        
        try:
            self.set_final_transaction_dataset_taxonomy_species(pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_taxonomy_species.csv'))
        except:
            print("The final_transaction_dataset_taxonomy_species.csv is not in the folder")

        self.set_species_and_id_df(pd.DataFrame(columns=['species_id', 'species', 'species_found', 'comment']))
        self.set_species_and_id_df_column(self.final_transaction_dataset_taxonomy_species.columns, 'species')
        self.get_species_and_id_df().drop(index = 0, inplace = True)
        self.get_species_and_id_df().reset_index(drop = True, inplace = True)
        
        for self.i, self.item in enumerate(self.get_species_and_id_df()["species"]):
            for self.j, self.species in enumerate(self.get_species_db_dataframe()["species"]):
                if str(self.item) == str(self.species):
                    self.get_species_and_id_df().at[self.i, 'species_id'] = self.get_species_db_dataframe().at[self.j, 'species_id']
                    self.get_species_and_id_df().at[self.i, 'species_found'] = self.get_species_db_dataframe().at[self.j, 'species']
                    self.get_species_and_id_df().at[self.i, 'comment'] = "Exact match"
                    print(f"The exact match ID was filled in for {self.item}")
                    break

        
        for self.i, self.item in enumerate(self.get_species_and_id_df()["species_id"]):
            if str(self.item) == 'nan':
                self.set_splitted_species(str(self.get_species_and_id_df().at[self.i, 'species']).split(' '))
                for self.j, self.species in enumerate(self.get_species_db_dataframe()["species"]):
                    if (str(self.get_splitted_species()[0]) + " " + "sp.") in str(self.species):
                        self.get_species_and_id_df().at[self.i, 'species_id'] = self.get_species_db_dataframe().at[self.j, 'species_id']
                        self.get_species_and_id_df().at[self.i, 'species_found'] = self.get_species_db_dataframe().at[self.j, 'species']
                        self.get_species_and_id_df().at[self.i, 'comment'] = "Not exact match"
                        print(f"The not exact match ID was filled in for {self.species}")
                        break
        
        for self.i, self.item in enumerate(self.get_species_and_id_df()["species_id"]):
            if str(self.item) == 'nan':
                for self.j, self.species in enumerate(self.get_species_db_dataframe()["species"]):
                    if str(self.get_species_and_id_df().at[self.i, 'species']) in str(self.species):
                        self.get_species_and_id_df().at[self.i, 'species_id'] = self.get_species_db_dataframe().at[self.j, 'species_id']
                        self.get_species_and_id_df().at[self.i, 'species_found'] = self.get_species_db_dataframe().at[self.j, 'species']
                        self.get_species_and_id_df().at[self.i, 'comment'] = "Not exact match"
                        print(f"The not exact match ID was filled in for {self.species}")
                        break

        self.get_species_and_id_df().to_csv(f"{SAVE_PATH}/species_and_id_df.csv")
        #self.set_user_input(str(input("Would you like to move to the next step to create the valid combination of taxonomy and functionality IDs? Be aware of the long runtime. Enter 'y' for yes or 'n' for no.")))
    
    
    '''
    It connects taxon ID and functionalit go-slim ID based on historical data.
    '''
    def connect_taxon_id_and_functionality_id(self):
        try:
            self.set_species_and_id_df(pd.read_csv(f'{SAVE_PATH}/species_and_id_df.csv'))
        except:
            print("The species_and_id_df.csv is not in the folder")
        
        try:
            self.set_species_transactional_df(pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_taxonomy_species.csv'))
        except:
            print("The final_transaction_dataset_taxonomy_species.csv is not in the folder")
        
        try:
            self.set_go_slim_transactional_df(pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_go-slim.csv'))
        except:
            print("The final_transaction_dataset_go-slim.csv is not in the folder")
    
        self.set_species_and_id_df(self.get_species_and_id_df().loc[:, ~self.get_species_and_id_df().columns.str.contains('^Unnamed')])
        self.set_species_transactional_df(self.get_species_transactional_df().loc[:, ~self.get_species_transactional_df().columns.str.contains('^Unnamed')])
        self.set_go_slim_transactional_df(self.get_go_slim_transactional_df().loc[:, ~self.get_go_slim_transactional_df().columns.str.contains('^Unnamed')])
        
        for self.i, self.item in enumerate(self.get_species_transactional_df().columns):
            for self.j, self.thing in enumerate(self.species_and_id_df['species']):
                if str(self.item) in str(self.thing):
                    self.append_new_column_list(self.item + '_' + str(int(self.get_species_and_id_df().at[self.j, "species_id"])))
        self.get_species_transactional_df().columns = self.get_new_column_list()
        print(self.get_species_transactional_df().columns)
        
        self.set_taxon_functionality_matrix(pd.DataFrame(columns=self.get_species_transactional_df().columns, index = self.get_go_slim_transactional_df().columns))
        
        self.set_goname_goid_df(pd.DataFrame(columns=['goid', 'goname']))
        
        for self.species in self.get_taxon_functionality_matrix().columns:
            self.set_splitted_species(str(self.species).split('_'))
            for self.function in self.get_taxon_functionality_matrix().index:
                try:
                    self.set_metadata_response(self.Connect.pull_data(f"https://www.ebi.ac.uk/QuickGO/services/annotation/search?assignedBy=InterPro&includeFields=goName&includeFields=taxonName&includeFields=name&includeFields=synonyms&goId={self.function[0:2]}%3A{self.function[3:]}&taxonId={self.get_splitted_species()[-1]}&limit=200&page=1"))
                    print(self.get_metadata_response()['numberOfHits'])
                    if self.get_metadata_response()['numberOfHits'] == 0:
                        self.get_taxon_functionality_matrix().at[self.function, f'{self.species}'] = False
                    else:
                        print(self.get_metadata_response()['results'][0]['goId'])
                        print(self.get_metadata_response()['results'][0]['goName'])
                        
                        self.set_goid(self.get_metadata_response()['results'][0]['goId'])
                        self.set_goname(self.get_metadata_response()['results'][0]['goName'])
                        if self.get_goid() not in self.get_goid_list():
                            self.append_goid_list(self.get_goid())
                        if self.get_goname() not in self.get_goname_list():
                            self.append_goname_list(self.get_goname())   
                        self.get_taxon_functionality_matrix().at[self.function, f'{self.species}'] = True
                except:
                    self.get_taxon_functionality_matrix().at[self.function, f'{self.species}'] = 'No response'
                    pass
            self.get_taxon_functionality_matrix().to_csv(f"{SAVE_PATH}/taxon_functionality_matrix.csv")
            
        self.set_goname_goid_df_column(self.get_goname_goid_df(), 'goid')
        self.set_goname_goid_df_column(self.get_goname_goid_df(), 'goname')
        self.get_goname_goid_df().to_csv(f"{SAVE_PATH}/goname_goid_df.csv")
        

        
    
    '''
    It creates a transactional database of species and functionlity combinations per sample based on the selected study.
    '''
    def create_taxonomy_and_functionality_transaction_dataframes(self):
        try:
            self.set_taxon_functionality_matrix(pd.read_csv(f'{SAVE_PATH}/taxon_functionality_matrix.csv', index_col = 0))
        except:
            print("The taxon_functionality_matrix.csv is not in the folder")
        try:
            self.set_species_transactional_df(pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_taxonomy_species.csv'))
        except:
            print("The final_transaction_dataset_taxonomy_species.csv is not in the folder")
        try:    
            self.set_go_slim_transactional_df(pd.read_csv(f'{SAVE_PATH}/final_transaction_dataset_go-slim.csv'))
        except:
            print("The final_transaction_dataset_go-slim.csv is not in the folder")
        try:
            self.set_species_and_id_df(pd.read_csv(f'{SAVE_PATH}/species_and_id_df.csv'))
        except:
            print("The species_and_id_df.csv is not in the folder")
        
        
        self.set_taxon_functionality_matrix(self.get_taxon_functionality_matrix().loc[:, ~self.get_taxon_functionality_matrix().columns.str.contains('^Unnamed')])
        self.set_species_transactional_df(self.get_species_transactional_df().loc[:, ~self.get_species_transactional_df().columns.str.contains('^Unnamed')])
        self.set_go_slim_transactional_df(self.get_go_slim_transactional_df().loc[:, ~self.get_go_slim_transactional_df().columns.str.contains('^Unnamed')])
        self.set_species_and_id_df(self.get_species_and_id_df().loc[:, ~self.get_species_and_id_df().columns.str.contains('^Unnamed')])
        
        for self.i, self.item in enumerate(self.get_taxon_functionality_matrix().columns):
            if len(self.item.split('_')) == 2:
                self.item = self.item.split('_')[0]
            elif len(self.item.split('_')) > 2:
                self.temp_item = self.item.split('_')[0]
                self.n = 1
                while (self.n + 2) <= len(self.item.split('_')):
                    self.temp_item = self.temp_item + '_' + self.item.split('_')[self.n]              
                    self.n += 1
                self.item = self.temp_item
            else:
                print("Something went wrong")
            self.taxon_functionality_matrix_columns_list.append(self.item)
            
        self.get_taxon_functionality_matrix().columns = self.taxon_functionality_matrix_columns_list

        for self.i, self.item in enumerate(self.get_species_transactional_df().index):
            self.species_list = self.get_species_transactional_df().loc[self.item,:].values.flatten().tolist()
            self.functionality_list = self.get_go_slim_transactional_df().loc[self.item,:].values.flatten().tolist()

            self.species_list_final = []
            self.functionality_list_final = []
            for self.j, self.specie in enumerate(self.species_list):
                if np.isnan(self.specie):
                    pass
                else:
                    if self.get_species_transactional_df().columns[self.j] not in self.species_list_final:
                        self.species_list_final.append(self.get_species_transactional_df().columns[self.j])
                        
            for self.k, self.func in enumerate(self.functionality_list):
                if self.func == 0.0:
                    pass
                else:
                    if self.get_go_slim_transactional_df().columns[self.k] not in self.functionality_list_final:
                        self.functionality_list_final.append(self.get_go_slim_transactional_df().columns[self.k])
            
            for self.j in range(len(self.species_list_final)):
                for self.k in range(len(self.functionality_list_final)):
                    if (self.species_list_final[self.j],self.functionality_list_final[self.k]) not in self.species_functionality_combination:
                        self.species_functionality_combination.append((self.species_list_final[self.j],self.functionality_list_final[self.k]))
            self.species_functionality_combination_final.append(self.species_functionality_combination)
            self.species_functionality_combination = []
        self.unique_combinations=[]
        for self.item in self.species_functionality_combination_final:
            for self.sub_item in self.item:
                if self.sub_item not in self.unique_combinations:
                    self.unique_combinations.append(self.sub_item)
        self.taxon_functionality_matrix_final = pd.DataFrame(columns = self.unique_combinations)
        
        for self.i, self.lists in enumerate(self.species_functionality_combination_final):
            for self.item in self.lists:
                if self.get_taxon_functionality_matrix().at[self.item[1], f"{self.item[0]}"] == 'True':
                    self.taxon_functionality_matrix_final.at[self.i, f"{self.item}"] = 'True'
                elif self.get_taxon_functionality_matrix().at[self.item[1], f"{self.item[0]}"] == 'False':
                    self.taxon_functionality_matrix_final.at[self.i, f"{self.item}"] = 'False'
                else:
                    self.taxon_functionality_matrix_final.at[self.i, f"{self.item}"] = 'False'
            
            print(f"Sample {self.i} is processed")
        
        self.taxon_functionality_matrix_final.to_csv(f"{SAVE_PATH}/taxon_functionality_matrix_final.csv")
        
            

connect_instance = Connect_species_functionality()
user_reply = (str(input("Please enter the number/letter of the function you would like to run:\n\n \
1 to match up species names with species ID\n \
2 to establish all proved species and functionalities combinations present in our selected study\n \
3 to create a transactional database considering species and functionalities present in each sample of the study\n \
q to quit\n\n")))
                        
while user_reply not in ANSWER_LIST:
    user_reply = (str(input("Please enter a valid number: '1', '2','3' or the letter 'q' to quit\n")))
    if user_reply == 'q':
        break
if user_reply == '1':
    connect_instance.find_species_id()
if user_reply == '2':
    connect_instance.connect_taxon_id_and_functionality_id()
if user_reply == '3':
    connect_instance.create_taxonomy_and_functionality_transaction_dataframes()
