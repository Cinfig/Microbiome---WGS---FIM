#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 08:12:08 2023

@author: adamveszpremi
"""

import pandas as pd
import re
from datetime import datetime
import time
import copy
import Connector as Conn
import sys
from pprint import pprint

#URL = "https://api.mg-rast.org/metadata/export/mgp385"

ENV_PACKAGE_URL = "https://api.mg-rast.org/metadata/view/env_package"
SEQ_METHOD_URL = "https://api.mg-rast.org/metadata/view/seq_meth"
CONTINENTS_URL = "https://api.mg-rast.org/metadata/view/continent"
DATETIME_FORMAT = datetime.now().strftime("%m-%d-%Y %H-%M-%S %p")
pd.set_option('expand_frame_repr', False)

class Pull_all_projects:
    
    def __init__(self):
        self.project_metadata_dict = {}
        self.project_metadata_df_temp = pd.DataFrame()
        self.project_metadata_df_merged = pd.DataFrame()
        self.unique_projects_df = pd.DataFrame()
        self.human_env_packages = {}
        self.human_env_packages_temp_list = []
        self.env_packages = {}
        self.seq_methods = {}
        self.continents = {}
        self.important_continents = {}
        self.important_continents_temp_list = []
        self.user_env_package_response = ""
        self.user_env_package_response_list = []
        self.user_seq_method_response = ""
        self.user_seq_method_response_list = []
        self.user_termination_response = ""
        self.seq_methods_list = []
        self.Connect = Conn.Connector()
    
    '''
    def get_human_wgs_project(self, json_dic):
        for item in json_dic['data']:
            #if item['sequence_type'] == 'WGS' and item['project_id'] not in self.human_project_id_list:
            if item['project_id'] not in self.human_project_id_list:
                self.human_project_id_list.append(item['project_id'])
                print(f"Project ID {item['project_id']} is added to the list")
    '''
    
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
    
    def get_a_key_of_project_metadata_dict(self, key):
        return self.project_metadata_dict[f'{key}']
    
    def set_continents(self, assign):
        self.continents = assign
    
    def get_continents(self):
        return self.continents
    
    def get_a_key_of_continents(self, key):
        return self.continents[f'{key}']
    
    def get_project_metadata_df_temp(self):
        return self.project_metadata_df_temp
    
    def set_project_metadata_df_temp(self, assign):
        self.project_metadata_df_temp = assign
    
    def get_project_metadata_df_merged(self):
        return self.project_metadata_df_merged

    def set_project_metadata_df_merged(self, assign):
        self.project_metadata_df_merged = assign
    
    def get_a_key_of_important_continents(self, key):
        return self.important_continents[f'{key}']
    
    def set_important_continents(self, assign):
        self.important_continents = assign
    
    def set_a_key_of_important_continents(self, key, assign):
        self.important_continents[f'{key}'] = assign
    
    def get_important_continents_temp_list(self):
        return self.important_continents_temp_list
    
    def set_important_continents_temp_list(self, assign):
        self.important_continents_temp_list = assign
    
    def get_unique_projects_df(self):
        return self.unique_projects_df
        
    def set_unique_projects_df(self, assign):
        self.unique_projects_df = assign
    
    '''
    Pull all unique env_package values from the erver
    '''
    def pull_env_packages(self):
        print('Pulling information, it may take some time.\n')
        self.set_env_packages(self.Connect.pull_data(ENV_PACKAGE_URL))
        self.filter_all_env_packages()
    
    '''
    Filter for human-associated env_packages.
    '''
    def filter_all_env_packages(self):
        self.set_human_env_packages(copy.deepcopy(self.get_env_packages()))
        self.set_a_key_of_human_env_packages('values', "")
        for item in self.get_a_key_of_env_packages('values'):
            if re.search(".*human.*", item):
                self.get_human_env_packages_temp_list().append(item)
        self.set_a_key_of_human_env_packages('values', self.get_human_env_packages_temp_list())
        self.set_a_key_of_human_env_packages('total', str(len(self.get_human_env_packages_temp_list())))
        self.set_human_env_packages_temp_list([])
    
    '''
    Filter for important_continents.
    '''
    def filter_continents(self):
        self.set_important_continents(copy.deepcopy(self.get_continents()))
        self.set_a_key_of_important_continents('values', "")
        for item in self.get_a_key_of_continents('values'):
            if re.search("(.*north.*|.*North.*|.*Asia.*|.*asia.*|.*Europe.*|.*europe.*)", item):
                self.get_important_continents_temp_list().append(item)
        self.set_a_key_of_important_continents('values', self.get_important_continents_temp_list())
        self.set_a_key_of_important_continents('total', str(len(self.get_important_continents_temp_list())))
        self.set_important_continents_temp_list([])
        
    '''
    Pull all unique sequence method values from the server
    '''
    def pull_sequence_methods(self):
        self.set_seq_methods(self.Connect.pull_data(SEQ_METHOD_URL))
        
    '''
    Pull all unique continent name from the server
    '''    
    def pull_continents(self):
        self.set_continents(self.Connect.pull_data(CONTINENTS_URL))
    
    '''
    Ask user to input the selected env_package and seq_method value/s. 
    '''
    def select_env_package_and_sequence_method(self):
        self.pull_env_packages()
        self.pull_sequence_methods()
        self.pull_continents()
        self.filter_continents()
        
        print(f"\nAvailable human-associated env_packages are: {self.get_a_key_of_human_env_packages('values')} \n")
        time.sleep(2)
        self.set_user_env_package_response(str(input("Enter a human-associated env_package name or enter 'all' for all human-associated env_packages: \n")))
        while (self.get_user_env_package_response() not in self.get_a_key_of_human_env_packages('values')) and (self.get_user_env_package_response() != 'all'):
            self.set_user_env_package_response(str(input("Enter a valid human-associated env_package name or enter 'all' for all human-associated env_package: \n")))
        if self.get_user_env_package_response() == 'all':
            self.set_user_env_package_response_list(self.get_a_key_of_human_env_packages('values'))
        else:
            self.get_user_env_package_response_list().append(self.get_user_env_package_response())
        
        print(f"\nAvailable seq_methods are: {self.get_a_key_of_sequence_methods('values')} \n")
        time.sleep(2)
        self.set_user_seq_method_response(str(input("Enter a seq_method name or enter 'all' for all seq_methods: \n")))
        while (self.get_user_seq_method_response() not in self.get_a_key_of_sequence_methods('values')) and (self.get_user_seq_method_response() != 'all'):
            self.set_user_seq_method_response(str(input("Enter a valid seq_method name or enter 'all' for all methods: \n")))
        if self.get_user_seq_method_response() == 'all':
            self.set_user_seq_method_response_list(self.get_a_key_of_sequence_methods('values'))
        else:
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
        self.get_project_metadata_df_merged().to_excel(f"All_selected_projects_with_datasets_{DATETIME_FORMAT}.xlsx")
        print("\nProjects with dataset information based on previous selection are saved as 'All_unique_projects.date.xlsx' \n")
        self.set_unique_projects_df(self.get_project_metadata_df_merged().drop_duplicates(subset=['project_id']))
        self.set_unique_projects_df(self.get_unique_projects_df()[['project_id', 'project_name', 'sequence_type', 'env_package', 'investigation_type']])
        self.get_unique_projects_df().reset_index(drop = True, inplace=True)
        self.get_unique_projects_df().to_excel(f"All_unique_projects_{DATETIME_FORMAT}.xlsx")
        print("All unique projects based on previous selection are saved as 'All_unique_projects.date.xlsx' \n")
        print("All unique projects are the following: \n ")
        pprint(self.get_unique_projects_df(), width = 600)
        
    '''
    
    '''
    def ask_for_script_termination(self):
        self.user_termination_response = str(input("\nIf you would you like to terminate this script, enter 'y' enter a project_id to select a project and move to the next step: \n"))
        while (self.user_termination_response.lower() not in self.get_unique_projects_df()['project_id']) and (self.user_termination_response.lower() != "y"):
            str(input("Please enter a valid input: 'y' or a 'project_id': \n"))
        if self.user_termination_response.lower() == "y":
            print("Script is terminated")
            sys.exit(0)
        elif self.user_termination_response.lower() in self.get_unique_projects_df()['project_id']:
            pass
        else:
            pass
            
    '''
    It pulls all metadata based on the user's previous input'
    '''
    def pull_selected_metadata(self):
        self.select_env_package_and_sequence_method()
        for package in self.get_user_env_package_response_list():
            for method in self.get_user_seq_method_response_list():
                if len(self.get_user_seq_method_response_list()) != 1:
                    self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}"))
                    print(f"The total datasets count of this category is : {self.get_a_key_of_project_metadata_dict('total_count')}")
                    if self.get_a_key_of_project_metadata_dict('total_count') > 1000:
                        for continent in self.get_a_key_of_important_continents('values'):
                            self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}&continent={continent}"))
                            print(f"The total datasets count of this category is : {self.get_a_key_of_project_metadata_dict('total_count')}")
                            self.convert_and_merge_responses()
                    else:
                        self.convert_and_merge_responses()
                        break
                    
                    
                else:
                    self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}&seq_meth={method}"))
                    print(f"The total datasets count of this category is : {self.get_a_key_of_project_metadata_dict('total_count')}")
                    if self.get_a_key_of_project_metadata_dict('total_count') > 1000:
                        for continent in self.get_a_key_of_important_continents('values'):
                            self.set_project_metadata_dict(self.Connect.pull_data(f"https://api.mg-rast.org/search?limit=1000&sequence_type=WGS&env_package={package}&seq_meth={method}&continent={continent}"))
                            print(f"The total datasets count of this category is : {self.get_a_key_of_project_metadata_dict('total_count')}")
                            self.convert_and_merge_responses()
                    else:
                        self.convert_and_merge_responses()
                        break
                break
        self.clean_save_and_print_merged_dataframes()
        self.ask_for_script_termination()
    
    
get_projects = Pull_all_projects()
get_projects.pull_selected_metadata()