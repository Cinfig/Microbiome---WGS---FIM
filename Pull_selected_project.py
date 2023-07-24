#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 01:37:32 2023

@author: adamveszpremi
"""

import Connector as Conn
import Pull_all_projects as pull
import pandas as pd


class Pull_selected_project:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        self.get_projects = pull.Pull_all_projects()
        self.get_projects.pull_selected_datasets()
        self.selected_project_id = ""
        self.metadata_response = ""
        self.profile_response = ""
        self.metadata_dataframe = pd.DataFrame()
        self.profile_dataframe = pd.DataFrame()
        self.profile_dataframe_merged = pd.DataFrame()

    '''
    Get and set methods to access variables
    '''
    def get_selected_project_id(self):
        return self.selected_project_id
    
    def set_selected_project_id(self, assign):
        self.selected_project_id = assign
    
    def get_metadata_response(self):
        return self.metadata_response
    
    def set_metadata_response(self, assign):
        self.metadata_response = assign

    def get_profile_response(self):
        return self.profile_response
        
    def set_profile_response(self, assign):
        self.profile_response = assign
    
    def get_metadata_dataframe(self):
        return self.metadata_dataframe
      
    def set_metadata_dataframe(self, assign):
        self.metadata_dataframe = assign

    def get_profile_dataframe(self):
        return self.profile_dataframe
      
    def set_profile_dataframe(self, assign):
        self.profile_dataframe = assign
    
    def get_profile_dataframe_merged(self):
        return self.profile_dataframe_merged
    
    def set_profile_dataframe_merged(self, assign):
        self.profile_dataframe_merged = assign

    '''
    Pull metadata of the selected project id
    '''
    def pull_project_metadata(self):
        
        self.set_selected_project_id(self.get_projects.get_user_termination_response())
        
        try:
            with pd.ExcelWriter(f"{self.get_selected_project_id()}_metadata_{self.get_projects.DATETIME_FORMAT}.xlsx") as writer:
                self.set_metadata_response(self.Connect.pull_data(f"https://api.mg-rast.org/metadata/export/{self.get_selected_project_id()}"))
                self.set_metadata_dataframe(pd.json_normalize(self.get_metadata_response()["samples"], record_path=["libraries"]))
                self.get_metadata_dataframe().drop(list(self.get_metadata_dataframe().filter(regex = ".*required.*|.*mixs.*|.*definition.*|.*unit.*|.*aliases.*|.*type.*|.*libraries.*")), axis = 1, inplace = True)
                self.get_metadata_dataframe().dropna(how="all", axis=1, inplace=True)
                self.set_metadata_dataframe(self.get_metadata_dataframe().T.drop_duplicates(keep = "first").T)
                self.get_metadata_dataframe().to_excel(writer, sheet_name = "samples_libraries")
        except:
            pass

    '''
    Pull abundaces of selected metagenome_id
    '''
    def pull_profile_datasets(self):
        for item in self.get_metadata_dataframe()["data.metagenome_id.value"]:
            print(f"{item}")
            try:
                with pd.ExcelWriter(f"{self.get_selected_project_id()}_profile_{self.get_metadata_dataframe()['data.metagenome_id.value']}_{self.get_projects.DATETIME_FORMAT}.xlsx") as writer:
                    self.set_profile_response(self.Connect.pull_data(f"https://api.mg-rast.org/annotation/sequence/{item}?type=organism&source=SwissProt"))
                    #self.set_profile_response(self.Connect.pull_data(f"https://api.mg-rast.org/profile{item}"))
                    print(type(self.get_profile_response()))
                    print(self.get_profile_response())
                    self.set_profile_dataframe_merged(pd.json_normalize(self.get_profile_response()["samples"]))
                    self.get_profile_dataframe_merged().to_excel(writer, sheet_name = f"{item}")
            except:
                print(f"Item {item} was skipped.")
                pass
        
instance = Pull_selected_project()
instance.pull_project_metadata()
instance.pull_profile_datasets()









'''
        for item in self.get_projects.get_unique_projects_df()['project_id']:
            try:
                self.set_metadata_response(self.Connect.pull_data(f"https://api.mg-rast.org/metadata/export/{item}"))

                with pd.ExcelWriter(f"{item}_metadata_{self.get_projects.DATETIME_FORMAT}.xlsx") as writer:
                    #self.set_metadata_dataframe_merged(pd.json_normalize(self.get_metadata_response()["samples"]))
                    #self.set_metadata_dataframe(pd.json_normalize(self.get_metadata_response()["samples"], record_path=["libraries"]))
                    #self.get_metadata_dataframe_merged().to_excel(writer, sheet_name = "samples") #####
                    #self.get_metadata_dataframe().to_excel(writer, sheet_name = "libraries") #####
                    #self.set_metadata_dataframe_merged(self.get_metadata_dataframe_merged().merge(self.get_metadata_dataframe(), how = 'outer'))
                    self.set_metadata_dataframe_merged(pd.json_normalize(self.get_metadata_response()["samples"], record_path=["libraries"]))
                    self.get_metadata_dataframe_merged().drop(list(self.get_metadata_dataframe_merged().filter(regex = ".*required.*|.*mixs.*|.*definition.*|.*unit.*|.*aliases.*|.*type.*|.*libraries.*")), axis = 1, inplace = True)
                    self.get_metadata_dataframe_merged().dropna(how="all", axis=1, inplace=True)
                    self.set_metadata_dataframe_merged(self.get_metadata_dataframe_merged().T.drop_duplicates(keep = "first").T)
                    self.get_metadata_dataframe_merged().to_excel(writer, sheet_name = "samples_libraries")
            except:
                pass
'''

