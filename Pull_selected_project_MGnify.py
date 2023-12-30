#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 05:22:35 2023

@author: adamveszpremi
"""

import Connector_MGnify as Conn
#import Pull_all_projects_MGnify as pull
import pandas as pd
#from functools import reduce
#import pyspark.sql.functions as F
#from pyspark.sql import SparkSession
import copy

SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output"
TAXONOMY_LEVELS = ['attributes.domain', 'attributes.hierarchy.phylum', 'attributes.hierarchy.class', 'attributes.hierarchy.order', 'attributes.hierarchy.family', 'attributes.hierarchy.genus', 'attributes.hierarchy.species']


class Pull_selected_project:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        #self.get_projects = pull.Pull_all_projects()
        #self.get_projects.pull_selected_datasets()
        self.selected_project_id = ""
        self.metadata_response = ""
        self.sample_id_list = []
        self.profile_response = ""
        self.functionality_response = ""
        self.profile_dataframe = pd.DataFrame()
        self.profile_dataframe_merged = pd.DataFrame()
        self.profile_dataframe_merged_final = pd.DataFrame()
        self.profile_dataframe_final = pd.DataFrame()
        self.profile_dataframe_transaction = pd.DataFrame()
        self.profile_dataframe_transaction_final = pd.DataFrame()
        
        self.functionality_dataframe = pd.DataFrame()
        self.functionality_dataframe_merged = pd.DataFrame()
        self.functionality_dataframe_merged_final = pd.DataFrame()
        self.functionality_dataframe_final = pd.DataFrame()
        self.functionality_dataframe_transaction = pd.DataFrame()
        self.functionality_dataframe_transaction_final = pd.DataFrame()
        self.unique_sample_ids = []
        self.count_sums_df = pd.DataFrame()

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
    
    def get_functionality_response(self):
        return self.functionality_response
        
    def set_functionality_response(self, assign):
        self.functionality_response = assign

    def get_profile_dataframe(self):
        return self.profile_dataframe
      
    def set_profile_dataframe(self, assign):
        self.profile_dataframe = assign
    
    def get_profile_dataframe_merged(self):
        return self.profile_dataframe_merged
    
    def set_profile_dataframe_merged(self, assign):
        self.profile_dataframe_merged = assign
    
    
    def get_functionality_dataframe(self):
        return self.functionality_dataframe
      
    def set_functionality_dataframe(self, assign):
        self.functionality_dataframe = assign
    
    def get_functionality_dataframe_merged(self):
        return self.functionality_dataframe_merged
    
    def set_functionality_dataframe_merged(self, assign):
        self.functionality_dataframe_merged = assign   

    
    
    
    def pull_selected_data(self):
        
        self.set_selected_project_id(str(input("Enter a study ID below:\n")))
        self.set_metadata_response(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{self.get_selected_project_id()}/analyses"))
    
        n = 0
        print(f"The total number of samples in this project is {len(self.get_metadata_response()['data'])}")
        while n < ((len(self.get_metadata_response()['data']))):
           self.sample_id_list.append(self.get_metadata_response()['data'][n]['id']) 
           
           print(f"Sample {n} of the selected project is: {self.get_metadata_response()['data'][n]['id']}")
           n = n + 1
        
        for item in self.sample_id_list:
            # Get all taxonomy data from all samples.
            self.pull_profile_taxonomy(item)
            self.profile_dataframe_final = pd.concat([self.profile_dataframe_final, self.profile_dataframe_merged])
            self.profile_dataframe_final.reset_index(drop = True, inplace=True)
            
            # Get all interpro_identifiers data from all samples.
            self.pull_profile_functionality(item, 'interpro_identifier')
            self.functionality_dataframe_final = pd.concat([self.functionality_dataframe_final, self.functionality_dataframe_merged])
            self.functionality_dataframe_final.reset_index(drop = True, inplace=True)
            
            #self.create_transaction_dataframes(item, self.get_profile_dataframe_merged(), self.profile_dataframe_transaction, 'taxonomy') # species names are often missing
            self.create_transaction_dataframes(item, self.get_functionality_dataframe_merged(), self.functionality_dataframe_transaction, 'interpro_identifier')
            
            
        
        self.calculate_relative_abundance(self.profile_dataframe_merged, self.profile_dataframe_merged_final, 'taxonomy')
        self.calculate_relative_abundance(self.functionality_dataframe_merged, self.functionality_dataframe_merged_final, 'interpro_identifier')
        
        
        self.profile_dataframe_final.to_csv(f"{SAVE_PATH}/counts_of_taxonomy.csv")
        #self.functionality_dataframe_merged_final.to_csv(f"{SAVE_PATH}/relative_abundance_of_taxonomy.csv")
        self.functionality_dataframe_final.to_csv(f"{SAVE_PATH}/counts_of_functionalities.csv")
        #self.functionality_dataframe_merged_final.to_csv(f"{SAVE_PATH}/relative_abundance_of_functionalities.csv")
        self.functionality_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/transactional_db_functionalities.csv")
        
    

    '''
    Pull counts of selected project samples
    '''
    def pull_profile_taxonomy(self, sample_id):
        self.set_profile_response(self.Connect.pull_data(f" https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{sample_id}/taxonomy"))
        self.set_profile_dataframe_merged(pd.json_normalize(self.get_profile_response()['data']))
        while self.get_profile_response()['links']['next'] is not None:
            self.set_profile_response(self.Connect.pull_data(self.get_profile_response()['links']['next']))
            self.set_profile_dataframe(pd.json_normalize(self.get_profile_response()['data']))
            self.profile_dataframe_merged = pd.concat([self.get_profile_dataframe_merged(), self.get_profile_dataframe()])
        self.get_profile_dataframe_merged()['Sample id'] = f"{sample_id}"
        self.get_profile_dataframe_merged().reset_index(drop = True, inplace=True)
        self.profile_dataframe_merged.to_csv(f"{SAVE_PATH}/counts_of_taxonomy_{sample_id}.csv")

    
    def pull_profile_functionality(self, sample_id, name):
        self.set_functionality_response(self.Connect.pull_data(f" https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{sample_id}/interpro-identifiers"))
        self.set_functionality_dataframe_merged(pd.json_normalize(self.get_functionality_response()['data']))
        while self.get_functionality_response()['links']['next'] is not None:
            self.set_functionality_response(self.Connect.pull_data(self.get_functionality_response()['links']['next']))
            self.set_functionality_dataframe(pd.json_normalize(self.get_functionality_response()['data']))
            self.functionality_dataframe_merged = pd.concat([self.get_functionality_dataframe_merged(), self.get_functionality_dataframe()])
        self.get_functionality_dataframe_merged().reset_index(drop = True, inplace=True)
        self.get_functionality_dataframe_merged()['Sample_id'] = f"{sample_id}"
        self.functionality_dataframe_merged.to_csv(f"{SAVE_PATH}/counts_of_{name}_functionalities_{sample_id}.csv")
        
    def create_transaction_dataframes(self, sample_id, input_dataframe, output_dataframe, name):
        output_dataframe = copy.deepcopy(input_dataframe)
        output_dataframe.set_index('attributes.accession', inplace = True)
        output_dataframe = output_dataframe[['attributes.count']]
        output_dataframe = output_dataframe.transpose()
        output_dataframe['Sample_id'] = f"{sample_id}"
        output_dataframe.set_index('Sample_id', inplace = True)
        output_dataframe.to_csv(f"{SAVE_PATH}/counts_of_{name}functionalities_transactional_{sample_id}.csv")

        

    def calculate_relative_abundance(self, input_dataframe, output_dataframe, name):
        #self.functionality_dataframe_merged = pd.read_csv('/Users/adamveszpremi/Desktop/MSc project work/Output/counts_of_functionalities.csv', index_col = [0])
        print(input_dataframe.columns)
        self.count_sums_df = input_dataframe.groupby(['Sample_id']).sum()
        for item in input_dataframe['Sample_id'].unique():
            input_dataframe.loc[input_dataframe['Sample_id'] == f"{item}", 'attributes.relative_abundance'] = ((input_dataframe['attributes.count'] / self.count_sums_df['attributes.count'].loc[f"{item}"]) * 100).round(10)
        output_dataframe = input_dataframe
        return output_dataframe
        self.input_dataframe.to_csv(f"{SAVE_PATH}/relative_abundance_of_{name}.csv")
        
      
                    
#3187281 
#151073

instance_2 = Pull_selected_project()
#instance_2.calculate_relative_abundance()
instance_2.pull_selected_data()
        
        
        
        
        
  
        
  
    
  
    

        
            #https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00010232/taxonomy
            #https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00010232/interpro-identifiers
            
        
'''
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
    '''
    

'''
    Pull metadata of the selected project id
    '''
'''
    def pull_project_metadata(self):
        
        #self.set_selected_project_id(self.get_projects.get_user_termination_response())
        self.set_selected_project_id('mgp87968')

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
        
        
        
        
        #self.loop = asyncio.get_event_loop()
        #self.profile_response = await self.Connect.pull_asynch_data("https://api.mg-rast.org/profile/mgm4447943.3?source=RefSeq&format=biom")
        
        #await self.set_profile_response(self.Connect.pull_asynch_data("https://api.mg-rast.org/profile/mgm4447943.3?source=RefSeq&format=biom"))
        
        
        
        #self.loop.run_until_complete(self.Connect.pull_asynch_data("https://api.mg-rast.org/profile/mgm4447943.3?source=RefSeq&format=biom"))   
        
'''
        for item in self.get_metadata_dataframe()["data.metagenome_id.value"]:
            print(f"{item}")
            try:
                with pd.ExcelWriter(f"{self.get_selected_project_id()}_profile_{self.get_metadata_dataframe()['data.metagenome_id.value']}_{self.get_projects.DATETIME_FORMAT}.xlsx") as writer:
                    #self.set_profile_response(self.Connect.pull_data(f"https://api.mg-rast.org/annotation/sequence/{item}?type=function"))
                    #self.set_profile_response(self.Connect.pull_asynch_data(f"https://api.mg-rast.org/profile/{item}?source=RefSeq&format=biom"))
                    #print(type(self.get_profile_response()))
                    #print(self.get_profile_response())
                    self.set_profile_dataframe_merged(pd.json_normalize(self.get_profile_response()["samples"]))
                    self.get_profile_dataframe_merged().to_excel(writer, sheet_name = f"{item}")
            except:
                print(f"Item {item} was skipped.")
                pass
'''
            
'''
    Load abundaces of a given metagenome_id
'''
             
#instance = Pull_selected_project()
#instance.pull_project_metadata()
#instance.pull_profile_datasets()
#print('finished')










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
