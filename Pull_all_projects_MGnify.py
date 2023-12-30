#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:02:03 2023

@author: adamveszpremi
"""

import pandas as pd
import re
from datetime import datetime
import time
import copy
import Connector_MGnify as Conn
import sys
from pprint import pprint


SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output"
BIOMES = "https://www.ebi.ac.uk/metagenomics/api/v1/biomes"
SEQ_METHOD = "https://www.ebi.ac.uk/metagenomics/api/v1/experiment-types"
STUDY_LIST = "https://www.ebi.ac.uk/metagenomics/api/v1/studies"
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 280)
pd.set_option('display.width', 560)


class Pull_all_projects:
    
    def __init__(self):
        self.DATETIME_FORMAT = datetime.now().strftime("%m-%d-%Y %H-%M-%S %p")
        self.biomes_df = pd.DataFrame()
        self.human_biomes_df = pd.DataFrame()
        self.seq_methods_df  = pd.DataFrame()
        self.project_metadata_dict = {}
        self.project_metadata_df_temp = pd.DataFrame()
        self.project_metadata_df_merged = pd.DataFrame()
        self.project_metadata_df_merged_droplist = []
        self.check_selected_seq_method_dict = {}
        self.unique_projects_df = pd.DataFrame()
        self.human_env_packages = {}
        self.human_env_packages_temp_list = []
        self.env_packages = {}
        self.seq_methods = {}
        self.user_env_package_response = ""
        self.user_env_package_response_list = []
        self.user_seq_method_response = ""
        self.user_seq_method_response_list = []
        self.user_termination_response = ""
        self.seq_methods_list = []
        self.Connect = Conn.Connector()
        
        self.study_analysis_call = ""
    
    '''
    Get and set methods for initialised variables.
    '''
    def get_env_packages(self):
        return self.env_packages
    
    def get_a_key_of_env_packages(self, key):
        return self.env_packages[f'{key}']
    
    def set_env_packages(self, assign):
        self.env_packages = assign
        
    def get_a_key_of_human_env_packages(self, key):
        return self.human_env_packages[f'{key}']        
    
    def set_human_env_packages(self, assign):
        self.human_env_packages = assign
    
    def set_a_key_of_human_env_packages(self, key, assign):
        self.human_env_packages[f'{key}'] = assign
    
    def get_human_env_packages_temp_list(self):
        return self.human_env_packages_temp_list
    
    def set_human_env_packages_temp_list(self, assign):
        self.human_env_packages_temp_list = assign

    def get_a_key_of_sequence_methods(self, key):
        return self.seq_methods[f'{key}']
    
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
        self.check_selected_seq_method_dict = assign
        
    def get_project_metadata_df_merged_droplist(self):
        return self.project_metadata_df_merged_temp

    
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
    
    
    def set_study_analysis_call(self, assign):
        self.study_analysis_call = assign
    
    def get_study_analysis_call(self):
        return self.study_analysis_call
    
    '''
    Pull all unique env_package values from the erver
    '''
    def pull_env_packages(self):
        print('Pulling information, it may take some time.\n')
        self.set_env_packages(self.Connect.pull_data(BIOMES))
        
        self.biomes_df = pd.json_normalize(self.get_env_packages()['data'])
        while self.get_env_packages()['links']['next'] is not None:
            self.set_env_packages(self.Connect.pull_data(self.get_env_packages()['links']['next']))
            self.biomes_temp_df = pd.json_normalize(self.get_env_packages()['data'])
            self.biomes_df = pd.concat([self.biomes_df, self.biomes_temp_df])
        self.biomes_df.reset_index(drop = True, inplace=True)
        self.biomes_df.to_csv(f"{SAVE_PATH}/all_biomes_out.csv")
        self.filter_all_env_packages()
    
    '''
    Filter for human-associated env_packages.
    '''
    def filter_all_env_packages(self):
        self.matched_index_list = []
        for i, item in enumerate(self.biomes_df['id']):
            if re.search("human", f"({item.lower()}"):
                self.matched_index_list.append(i)
        self.human_biomes_df = copy.deepcopy(self.biomes_df.iloc[self.matched_index_list])
        self.human_biomes_df.to_csv(f"{SAVE_PATH}/human_biomes_out.csv")
        print(self.human_biomes_df[['attributes.biome-name', 'attributes.samples-count']])
    
    
        
    '''
    Pull all unique sequence method values from the server
    '''
    def pull_sequence_methods(self):
        self.set_seq_methods(self.Connect.pull_data(SEQ_METHOD))
        self.seq_methods_df = pd.json_normalize(self.get_seq_methods()['data'])
        self.seq_methods_df.to_csv(f"{SAVE_PATH}/all_sequence_methods_out.csv")
        print(self.seq_methods_df[['id', 'attributes.runs-count']])
    
    '''
    Ask user to input the selected env_package and seq_method value/s. 
    '''
    def select_env_package_and_sequence_method(self):
        self.pull_env_packages()
        self.pull_sequence_methods()
        
        #print(f"\nAvailable human-associated env_packages are: {self.human_biomes_df[['attributes.lineage']]} \n")
        print("\nAvailable human-associated env_packages are:\n")
        pprint(self.human_biomes_df['attributes.lineage'], width = 1000)
        time.sleep(2)
        self.set_user_env_package_response(str(input("\nEnter a human-associated env_package name \n")))
        while self.get_user_env_package_response() not in self.human_biomes_df['attributes.lineage'].values.tolist():
            self.set_user_env_package_response(str(input("Enter a valid human-associated env_package name \n")))
        self.get_user_env_package_response_list().append(self.get_user_env_package_response())
        
        print(f"\nAvailable seq_methods are: {self.seq_methods_df[['attributes.experiment-type']]} \n")
        time.sleep(2)
        self.set_user_seq_method_response(str(input("Enter a seq_method name\n")))
        while self.get_user_seq_method_response() not in self.seq_methods_df['attributes.experiment-type'].values.tolist():
            self.set_user_seq_method_response(str(input("Enter a valid seq_method name \n")))
        self.get_user_seq_method_response_list().append(self.get_user_seq_method_response())
        print('\nPulling more information, it may take some time.\n')
    
    '''
    Convert dictionary to dataframe and merge dataframes
    '''
    def convert_and_merge_responses(self):
        self.set_project_metadata_df_temp(pd.DataFrame.from_dict(self.get_a_key_of_project_metadata_dict('data')))
        if self.get_project_metadata_df_merged().shape == (0,0):
            self.set_project_metadata_df_merged(self.get_project_metadata_df_temp())
        elif self.get_project_metadata_df_temp().shape == (0,0):
            pass
        else:
            self.set_project_metadata_df_merged(self.get_project_metadata_df_merged().merge(self.get_project_metadata_df_temp(), how="outer"))

    
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
    Ask user to terminate or select a project for FIM
    '''
    def ask_for_script_termination(self):
        self.user_termination_response = str(input("\nIf you would you like to terminate this script, enter 'y' enter a project_id to select a project for FIM: \n"))
        while (self.get_user_termination_response().lower() not in self.get_unique_projects_df()['project_id'].tolist()) and (self.get_user_termination_response().lower() != "y"):
            self.user_termination_response = str(input("Please enter a valid input: 'y' or a 'project_id': \n"))
        if self.get_user_termination_response().lower() == "y":
            print("\nScript is terminated\n")
            sys.exit(0)
        elif self.get_user_termination_response().lower() in self.get_unique_projects_df()['project_id'].tolist():
            pass
        else:
            pass
            
    '''
    It pulls all metadata based on the user's previous input'
    '''
    def pull_selected_datasets(self):
        
        self.select_env_package_and_sequence_method()
        for package in self.get_user_env_package_response_list():
            print(package)
            self.set_project_metadata_dict(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/biomes/{package}/studies"))
            
            #print(self.get_project_metadata_dict())
            self.project_metadata_df_merged = pd.json_normalize(self.get_project_metadata_dict()['data'])    
            #print(self.project_metadata_df_merged)
            
            while self.get_project_metadata_dict()['links']['next'] is not None:                        
                self.set_project_metadata_dict(self.Connect.pull_data(self.get_project_metadata_dict()['links']['next']))
                self.project_metadata_df_temp = pd.json_normalize(self.get_project_metadata_dict()['data'])
                self.project_metadata_df_merged = pd.concat([self.project_metadata_df_merged, self.project_metadata_df_temp])
            self.project_metadata_df_merged.reset_index(drop = True, inplace=True)
            #self.project_metadata_df_merged.to_csv(f"{SAVE_PATH}/selected_human_biomes_out_before drop.csv")
            
            n = 0
            print(len(self.project_metadata_df_merged['id']))
            #print(self.project_metadata_df_merged[['id', 'attributes.samples-count', 'attributes.study-name']])
            while n < len(self.project_metadata_df_merged['id']):
                print(self.project_metadata_df_merged['id'][n])
                self.project_metadata_df_merged
                try:
                    self.set_check_selected_seq_method_dict(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{self.project_metadata_df_merged['id'][n]}/analyses"))
                    print(self.get_check_selected_seq_method_dict()['data'][0]['attributes']['experiment-type'])
                    #print(self.project_metadata_df_merged.index[n])
                    if self.get_check_selected_seq_method_dict()['data'][0]['attributes']['experiment-type'] == 'metagenomic':
                        pass
                    else:
                        self.project_metadata_df_merged_droplist.append(self.project_metadata_df_merged.index[n])
                except:
                    self.project_metadata_df_merged_droplist.append(self.project_metadata_df_merged.index[n])
                    pass

                    #self.project_metadata_df_merged.drop(self.project_metadata_df_merged.index[n], inplace = True)
                n = n + 1
            self.project_metadata_df_merged.drop(self.project_metadata_df_merged_droplist, inplace = True)
        

            self.project_metadata_df_merged.to_csv(f"{SAVE_PATH}/selected_human_biomes_out.csv")
            #print(self.project_metadata_df_merged[['id', 'attributes.samples-count', 'attributes.study-name']])
            print(self.project_metadata_df_merged[['id', 'attributes.study-name']])
            
           
   
instance = Pull_all_projects()
instance.pull_selected_datasets()         
           
            
           
           
            
           
            
'''
            #https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Host-associated:Human:Excretory%20system:Urethra:Urine/studies
            for method in self.get_user_seq_method_response_list():
                if len(self.get_user_seq_method_response_list()) != 1:
                    self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}"))
                    print(f"The total datasets count of the current page is : {self.get_a_key_of_project_metadata_dict('total_count')}\n")
                    self.convert_and_merge_responses()
                    for n in range(int(self.get_a_key_of_project_metadata_dict('total_count')/1000)):
                        self.set_project_metadata_dict(self.Connect.pull_data(f"{self.get_a_key_of_project_metadata_dict('next')}\n"))
                        self.convert_and_merge_responses()
                    
                    
                else:
                    self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}&seq_meth={method}"))
                    print(f"The total datasets count of the current page is :  {self.get_a_key_of_project_metadata_dict('total_count')}")
                    self.convert_and_merge_responses()
                    for n in range(int(self.get_a_key_of_project_metadata_dict('total_count')/1000)):
                        self.set_project_metadata_dict(self.Connect.pull_data(f"{self.get_a_key_of_project_metadata_dict('next')}\n"))
                        self.convert_and_merge_responses()

                break
        self.clean_save_and_print_merged_dataframes()
        self.ask_for_script_termination()
'''
        
'''
        
        self.start_time = time.time()
        #self.set_project_metadata_dict(self.Connect.pull_data("https://www.ebi.ac.uk/metagenomics/api/v1/studies"))
        self.set_project_metadata_dict(self.Connect.pull_data("https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Host-associated:Human:Digestive%20system/studies"))
        while self.get_project_metadata_dict()["links"]["next"] is not None:
            for n in range(len(self.get_project_metadata_dict()["data"])):
                try:
                    self.set_study_analysis_call(self.Connect.pull_data(self.get_project_metadata_dict()["data"][n]["relationships"]["analyses"]["links"]["related"]))
                    if self.get_study_analysis_call()["data"][0]["attributes"]["experiment-type"] == "metagenomic":
                        print("metagenomic")
                        print(self.get_project_metadata_dict()["data"][n]["attributes"]["study-name"])
                except:
                    print("Value is missing from the dictionary")
                    pass
            self.set_project_metadata_dict(self.Connect.pull_data(self.get_project_metadata_dict()["links"]["next"]))    
        
        self.end_time = time.time()
        print(f"Elapsed time is {self.end_time - self.start_time} seconds")
        
'''
        
'''
        #for n in range(len(self.get_project_metadata_dict()["data"])):
        #    self.get_project_metadata_dict()["data"][n]["data"]
        print(len(self.get_project_metadata_dict()["data"]["id"]))
        print(self.get_project_metadata_dict()["data"]["attributes"]["study-abstract"])
        print(self.get_project_metadata_dict()["data"]["attributes"]["study-name"])
        #print(self.get_project_metadata_dict()["data"][0]["relationships"]["biomes"]["data"])
        #print("\n")
        print(self.get_project_metadata_dict()["data"])
'''
