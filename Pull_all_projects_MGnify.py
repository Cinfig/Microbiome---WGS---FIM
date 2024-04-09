#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:02:03 2023

@author: adamveszpremi
"""

import pandas as pd
import re
from datetime import datetime
import copy
import sys
import Connector_MGnify as Conn
from pprint import pprint
import os


SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output_safety_copy"
SAVE_PATH = os.getcwd()
BIOMES = "https://www.ebi.ac.uk/metagenomics/api/v1/biomes"
SEQ_METHOD = "https://www.ebi.ac.uk/metagenomics/api/v1/experiment-types"
STUDY_LIST = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 280)
pd.set_option('display.width', 560)


'''
This class is used to pull all human-associated study data from the MGnify API based on the user's selection.
'''
class Pull_all_projects:
    
    def __init__(self):
        self.DATETIME_FORMAT = datetime.now().strftime("%m-%d-%Y %H-%M-%S %p")
        self.biomes_df = pd.DataFrame()
        self.biomes_temp_df = pd.DataFrame()
        self.human_biomes_df = pd.DataFrame()
        self.seq_methods_df  = pd.DataFrame()
        self.matched_index_list = []
        self.project_metadata_dict = {}
        self.project_metadata_df_temp = pd.DataFrame()
        self.project_metadata_df_merged = pd.DataFrame()
        self.project_metadata_df_merged_droplist = []
        self.check_selected_seq_method_dict = {}
        self.unique_projects_df = pd.DataFrame()
        self.env_packages = {}
        self.seq_methods = {}
        self.user_env_package_response = ""
        self.user_env_package_response_list = []
        self.user_seq_method_response = ""
        self.user_seq_method_response_list = []
        self.user_termination_response = ""
        self.seq_methods_list = []
        self.Connect = Conn.Connector()
        
    
    '''
    Get and set methods for initialised variables.
    '''
    def get_env_packages(self):
        return self.env_packages
    
    def set_env_packages(self, assign):
        self.env_packages = assign
    
    def set_seq_methods(self, key):
        self.seq_methods = key
    
    def get_seq_methods(self):
        return self.seq_methods

    def get_user_env_package_response(self):
        return self.user_env_package_response

    def set_user_env_package_response(self, assign):
        self.user_env_package_response = assign
    
    def get_user_env_package_response_list(self):
        return self.user_env_package_response_list
    
    def set_user_env_package_response_list(self, assign):
        self.user_env_package_response_list = assign

    def get_user_seq_method_response(self):
        return self.user_seq_method_response

    def set_user_seq_method_response(self, assign):
        self.user_seq_method_response = assign

    def get_user_seq_method_response_list(self):
        return self.user_seq_method_response_list
    
    def set_user_seq_method_response_list(self, assign):
        self.user_seq_method_response_list = assign
    
    def set_project_metadata_dict(self, assign):
        self.project_metadata_dict = assign
    
    def get_project_metadata_dict(self):
        return self.project_metadata_dict
    
    def get_a_key_of_project_metadata_dict(self, key):
        return self.project_metadata_dict[f'{key}']
    
    def get_project_metadata_df_temp(self):
        return self.project_metadata_df_temp
    
    def set_project_metadata_df_temp(self, assign):
        self.project_metadata_df_temp = assign
    
    def get_project_metadata_df_merged(self):
        return self.project_metadata_df_merged

    def set_project_metadata_df_merged(self, assign):
        self.project_metadata_df_merged = assign
        
    def get_project_metadata_df_merged_droplist(self):
        return self.project_metadata_df_merged_droplist

    def set_check_selected_seq_method_dict(self, assign):
        self.check_selected_seq_method_dict = assign
    
    def get_check_selected_seq_method_dict(self):
        return self.check_selected_seq_method_dict
    
    def get_unique_projects_df(self):
        return self.unique_projects_df
        
    def set_unique_projects_df(self, assign):
        self.unique_projects_df = assign
    
    def get_user_termination_response(self):
        return self.user_termination_response
    
    def set_user_termination_response(self, assign):
        self.user_termination_response = assign
    
    def set_biomes_df(self, assign):
        self.biomes_df = assign
    
    def get_biomes_df(self):
        return self.biomes_df 
    
    def set_biomes_temp_df(self, assign):
        self.biomes_temp_df = assign
    
    def get_biomes_temp_df(self):
        return self.biomes_temp_df 
    
    def set_human_biomes_df(self, assign):
        self.human_biomes_df = assign
    
    def get_human_biomes_df(self):
        return self.human_biomes_df
    
    def set_seq_methods_df(self, assign):
        self.seq_methods_df = assign

    def get_seq_methods_df(self):
        return self.seq_methods_df
    
    def get_matched_index_list(self):
        return self.matched_index_list
    
    
    '''
    Pull all unique biome categories from the MGnify API
    '''
    def pull_env_packages(self):
        print('Pulling information from the MGnify API, it may take some time.\n')
        self.set_env_packages(self.Connect.pull_data(BIOMES))
        self.set_biomes_df(pd.json_normalize(self.get_env_packages()['data']))
        while self.get_env_packages()['links']['next'] is not None:
            self.set_env_packages(self.Connect.pull_data(self.get_env_packages()['links']['next']))
            self.set_biomes_temp_df(pd.json_normalize(self.get_env_packages()['data']))
            self.set_biomes_df(pd.concat([self.get_biomes_df(), self.get_biomes_temp_df()]))
        self.get_biomes_df().reset_index(drop = True, inplace=True)
        #self.get_biomes_df().to_csv(f"{SAVE_PATH}/all_biomes_out.csv")
        #print("All biomes are saved. \n")
        self.filter_all_env_packages()
    
    '''
    Filter for human-associated biome categories
    '''
    def filter_all_env_packages(self):
        for i, item in enumerate(self.biomes_df['id']):
            if re.search("human", f"({item.lower()}"):
                self.get_matched_index_list().append(i)
        self.set_human_biomes_df(copy.deepcopy(self.get_biomes_df().iloc[self.get_matched_index_list()]))
        self.get_human_biomes_df().reset_index(drop = True, inplace = True)
        self.get_human_biomes_df().to_csv(f"{SAVE_PATH}/human_biomes_out.csv")
        print("\nAll human-associated biomes are saved. \n")
        #print("All human-associated biomes are the following: \n")
        #print(self.get_human_biomes_df()[['attributes.biome-name', 'attributes.samples-count']])
    
    
        
    '''
    Pull all unique sequence method values from the server
    '''
    def pull_sequence_methods(self):
        self.set_seq_methods(self.Connect.pull_data(SEQ_METHOD))
        self.set_seq_methods_df(pd.json_normalize(self.get_seq_methods()['data']))
        self.get_seq_methods_df().to_csv(f"{SAVE_PATH}/all_sequence_methods_out.csv")
        print("\nAll sequence methods are saved. \n")
        #print("All sequence methods are the following: \n")
        #print(self.seq_methods_df[['id', 'attributes.runs-count']])

    
    '''
    Ask user to input the selected env_package and seq_method value/s. 
    '''
    def select_env_package_and_sequence_method(self):
        self.pull_sequence_methods()
        self.pull_env_packages()
        
        print("\nAvailable human-associated biomes are:\n")
        for i, item in enumerate(self.get_human_biomes_df()['attributes.lineage']):
            print(i, format(str(item), '>25'))
        
        self.set_user_env_package_response(int(input("\nEnter a human-associated biome's number\n")))
        while self.get_user_env_package_response() not in self.get_human_biomes_df().index.values.tolist():
            self.set_user_env_package_response(int(input("Enter a valid number \n")))
        self.get_user_env_package_response_list().append(self.get_human_biomes_df().at[self.get_user_env_package_response(), 'attributes.lineage'])
        
        print("\nAvailable seq_methods are: \n")
        for i, item in enumerate(self.seq_methods_df['attributes.experiment-type']):
            print(i, format(str(item), '>25'))
        
        self.set_user_seq_method_response(int(input("\nEnter a seq_method's number\n")))
        while self.get_user_seq_method_response() not in self.get_seq_methods_df().index.values.tolist():
            self.set_user_seq_method_response(int(input("Enter a valid number \n")))
        self.get_user_seq_method_response_list().append(self.get_seq_methods_df().at[self.get_user_seq_method_response(), 'id'])
        print('\nPulling more information, it may take some time.\n')
        
    
    '''
    Clean save and print merged dataframes.
    '''
    def clean_save_and_print_merged_dataframes(self):
        self.set_project_metadata_df_merged(self.get_project_metadata_df_merged().drop_duplicates(subset=['library_id']))
        self.set_project_metadata_df_merged(self.get_project_metadata_df_merged()[self.get_project_metadata_df_merged().investigation_type == 'metagenome'])
        self.get_project_metadata_df_merged().to_excel(f"All_selected_projects_with_datasets_{self.DATETIME_FORMAT}.xlsx")
        print("\nProjects with dataset information based on previous selection are saved as 'All_unique_projects.date.xlsx' \n")
        self.set_unique_projects_df(self.get_project_metadata_df_merged().drop_duplicates(subset=['project_id']))
        self.set_unique_projects_df(self.get_unique_projects_df()[['project_id', 'project_name', 'sequence_type', 'env_package', 'investigation_type']])
        self.get_unique_projects_df().reset_index(drop = True, inplace=True)
        self.get_unique_projects_df().to_excel(f"All_unique_projects_{self.DATETIME_FORMAT}.xlsx")
        print("All unique projects based on previous selection are saved as 'All_unique_projects.date.xlsx' \n")
        print("All unique projects are the following: \n ")
        pprint(self.get_unique_projects_df(), width = 1000)
        
            
    '''
    It pulls all metadata based on the user's previous input'
    '''
    def pull_all_selected_datasets(self):
        
        self.select_env_package_and_sequence_method()
        for package in self.get_user_env_package_response_list():
            self.set_project_metadata_dict(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/biomes/{package}/studies"))
            
            self.set_project_metadata_df_merged(pd.json_normalize(self.get_project_metadata_dict()['data']))

            
            while self.get_project_metadata_dict()['links']['next'] is not None:                        
                self.set_project_metadata_dict(self.Connect.pull_data(self.get_project_metadata_dict()['links']['next']))
                self.set_project_metadata_df_temp(pd.json_normalize(self.get_project_metadata_dict()['data']))
                self.set_project_metadata_df_merged(pd.concat([self.get_project_metadata_df_merged(), self.get_project_metadata_df_temp()]))
            self.get_project_metadata_df_merged().reset_index(drop = True, inplace=True)

            
            if len(self.get_project_metadata_df_merged().columns) == 0:
                   print(f"The combination of {self.get_user_env_package_response_list()[0]} and {self.get_user_seq_method_response_list()[0]} has no result.")
                   print("Try a different biome and sequencing method combination")
                   sys.exit(0)
            
            n = 0     
            while n < len(self.get_project_metadata_df_merged()['id']):
                print(f"\nProject ID: {self.get_project_metadata_df_merged()['id'][n]}")
                try:
                    self.set_check_selected_seq_method_dict(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{self.project_metadata_df_merged['id'][n]}/analyses"))
                    print(f"Experiment type: {self.get_check_selected_seq_method_dict()['data'][0]['attributes']['experiment-type']}\n")
                    if self.get_check_selected_seq_method_dict()['data'][0]['attributes']['experiment-type'] == 'metagenomic':
                        pass
                    else:
                        self.get_project_metadata_df_merged_droplist().append(self.get_project_metadata_df_merged().index[n])
                except:
                    self.get_project_metadata_df_merged_droplist().append(self.get_project_metadata_df_merged().index[n])
                    pass
                n = n + 1
            self.get_project_metadata_df_merged().drop(self.get_project_metadata_df_merged_droplist(), inplace = True)
            self.get_project_metadata_df_merged().reset_index(drop = True, inplace=True)
            self.get_project_metadata_df_merged().to_csv(f"{SAVE_PATH}/selected_human_biomes_out.csv")
            if self.get_project_metadata_df_merged().shape[0] == 0:
                print('The saved dataframe is empty, there is no study which fulfills the selected criteria')
            else:
                print(f"The following projects are available wih biome '{self.get_user_env_package_response_list()[0]}' and experiment type '{self.get_user_seq_method_response_list()[0]}':\n")
                for item in self.get_project_metadata_df_merged().index:
                    print(self.get_project_metadata_df_merged().at[item, 'id'], format(self.get_project_metadata_df_merged().at[item, 'attributes.study-name'], '>5'))
            
           
   
instance = Pull_all_projects()
instance.pull_all_selected_datasets()