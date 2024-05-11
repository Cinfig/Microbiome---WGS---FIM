#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 05:22:35 2023

@author: adamveszpremi
"""

import Connector_MGnify as Conn
import pandas as pd
import copy
import sys
import os


SAVE_PATH = "/Users/adamveszpremi/Desktop/MSc project work/Output_safety_copy"
#SAVE_PATH = os.getcwd()
TAXONOMY_LEVELS = ['attributes.domain', 'attributes.hierarchy.phylum', 'attributes.hierarchy.class', 'attributes.hierarchy.order', 'attributes.hierarchy.family', 'attributes.hierarchy.genus', 'attributes.hierarchy.species']
TAXONOMY_LEVELS_COUNTS = ['attributes.domain_count', 'attributes.hierarchy.phylum_count', 'attributes.hierarchy.class_count', 'attributes.hierarchy.order_count', 'attributes.hierarchy.family_count', 'attributes.hierarchy.genus_count', 'attributes.hierarchy.species_count']
TAXONOMY_LEVEL_NAMES = ['domain','kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
FUNCTIONALITY_NAMES = ['go-slim', 'go-terms', 'antismash-gene-clusters', 'genome-properties', 'interpro-identifiers']
ANSWER_LIST = ['y', 'n']

class Pull_selected_project:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        self.user_input = ""
        self.user_input_second = ""
        self.user_input_list = []
        self.selected_project_id = ""
        self.metadata_response = ""
        self.sample_id_list = []
        self.taxonomy_response = ""
        self.functionality_response = ""
        self.missing_or_unassigned_taxon = ""
        self.taxonomy_dataframe = pd.DataFrame()
        self.taxonomy_dataframe_merged = pd.DataFrame()
        self.taxonomy_dataframe_merged_final = pd.DataFrame()
        self.taxonomy_dataframe_final = pd.DataFrame()
        self.taxonomy_dataframe_transaction = pd.DataFrame()
        self.taxonomy_dataframe_transaction_final = pd.DataFrame()       
        self.functionality_dataframe = pd.DataFrame()
        self.functionality_dataframe_merged = pd.DataFrame()
        self.functionality_dataframe_merged_final = pd.DataFrame()
        self.functionality_dataframe_final = pd.DataFrame()
        self.functionality_dataframe_transaction = pd.DataFrame()
        self.functionality_dataframe_transaction_final = pd.DataFrame()
        self.count_sums_df = pd.DataFrame()
        self.unique_sample_ids = []
        

    '''
    Get and set methods to access variables
    '''
    def set_user_input(self, assign):
        self.user_input = str(assign).lower()
    
    def get_user_input(self):
        return self.user_input
    
    def set_user_input_second(self, assign):
        self.user_input_second = str(assign).lower()
    
    def get_user_input_second(self):
        return self.user_input_second
    
    def set_user_input_list(self, entry):
        self.user_input_list.append(entry)
    
    def get_user_input_list(self):
        return self.user_input_list
    
    def get_selected_project_id(self):
        return self.selected_project_id
    
    def set_selected_project_id(self, assign):
        self.selected_project_id = assign
    
    def get_metadata_response(self):
        return self.metadata_response
    
    def set_metadata_response(self, assign):
        self.metadata_response = assign

    def get_taxonomy_response(self):
        return self.taxonomy_response
        
    def set_taxonomy_response(self, assign):
        self.taxonomy_response = assign
    
    def get_functionality_response(self):
        return self.functionality_response
        
    def set_functionality_response(self, assign):
        self.functionality_response = assign
        
    def get_sample_id_list(self):
        return self.sample_id_list 

    def get_taxonomy_dataframe(self):
        return self.taxonomy_dataframe
      
    def set_taxonomy_dataframe(self, assign):
        self.taxonomy_dataframe = assign
        
    def get_taxonomy_dataframe_final(self):
        return self.taxonomy_dataframe_final
    
    def set_taxonomy_dataframe_final(self, assign):
        self.taxonomy_dataframe_final = assign
    
    def get_taxonomy_dataframe_merged(self):
        return self.taxonomy_dataframe_merged
    
    def set_taxonomy_dataframe_merged(self, assign):
        self.taxonomy_dataframe_merged = assign
    
    def get_taxonomy_dataframe_merged_final(self):
        return self.taxonomy_dataframe_merged_final
    
    def get_taxonomy_dataframe_transaction(self):
        return self.taxonomy_dataframe_transaction
    
    def set_taxonomy_dataframe_transaction(self, assign):
        self.taxonomy_dataframe_transaction = assign
    
    def get_taxonomy_dataframe_transaction_final(self):
        return self.taxonomy_dataframe_transaction_final
    
    def set_taxonomy_dataframe_transaction_final(self, assign):
        self.taxonomy_dataframe_transaction_final = assign
    
    def get_functionality_dataframe(self):
        return self.functionality_dataframe
      
    def set_functionality_dataframe(self, assign):
        self.functionality_dataframe = assign
    
    def get_functionality_dataframe_final(self):
        return self.functionality_dataframe_final
    
    def set_functionality_dataframe_final(self, assign):
        self.functionality_dataframe_final = assign
    
    def get_functionality_dataframe_merged(self):
        return self.functionality_dataframe_merged
    
    def set_functionality_dataframe_merged(self, assign):
        self.functionality_dataframe_merged = assign
    
    def get_functionality_dataframe_merged_final(self):
        return self.functionality_dataframe_merged_final
    
    def get_functionality_dataframe_transaction(self):
        return self.functionality_dataframe_transaction
    
    def set_functionality_dataframe_transaction(self, assign):
        self.functionality_dataframe_transaction = assign
    
    def get_functionality_dataframe_transaction_final(self):
        return self.functionality_dataframe_transaction_final
    
    def set_functionality_dataframe_transaction_final(self, assign):
        self.functionality_dataframe_transaction_final = assign

    '''
    It creates a functionality transaction database
    '''
    def create_functionality_transacation_databases(self, URL_id, save_id):
        for item in self.get_sample_id_list():
            self.pull_profile_functionality(item, URL_id, save_id)
            self.set_functionality_dataframe_final(pd.concat([self.get_functionality_dataframe_final(), self.get_functionality_dataframe_merged()]))
            self.get_functionality_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_functionality_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            self.set_functionality_dataframe_merged(self.calculate_relative_abundance(self.get_functionality_dataframe_merged(), item, URL_id))
            self.create_functionality_transaction_dataframes(item, self.get_functionality_dataframe_merged(), self.get_functionality_dataframe_transaction(), save_id)
            if self.functionality_dataframe_transaction_final.shape[0] == 0:
                self.functionality_dataframe_transaction_final = self.get_functionality_dataframe_transaction()
            else:
                self.functionality_dataframe_transaction_final = self.functionality_dataframe_transaction_final.merge(self.get_functionality_dataframe_transaction(), how = 'outer')
                    
            if self.get_functionality_dataframe_final().shape[0] != 0:
                #self.get_functionality_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_functionality_{save_id}.csv")
                self.functionality_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/final_transaction_dataset_{save_id}.csv")
            else:
                pass

        self.set_functionality_dataframe_final(pd.DataFrame())
        self.set_functionality_dataframe_merged(pd.DataFrame())
        self.set_functionality_dataframe_transaction(pd.DataFrame())
        self.set_functionality_dataframe_transaction_final(pd.DataFrame())
    
    '''
    It creates a taxonomy transaction database and saves it.
    '''
    def create_taxonomy_transaction_databases(self, URL_id, save_id, level, level_abundance):
        for item in self.get_sample_id_list():
            self.pull_profile_taxonomy(item, URL_id, save_id)
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            self.set_taxonomy_dataframe_merged(self.calculate_relative_abundance_multilevel(self.get_taxonomy_dataframe_merged(), item, URL_id))
            self.create_taxonomy_transaction_dataframes(item, self.get_taxonomy_dataframe_merged(), self.get_taxonomy_dataframe_transaction(), save_id, level, level_abundance)
            if self.taxonomy_dataframe_transaction_final.shape[0] == 0:
                self.taxonomy_dataframe_transaction_final = self.get_taxonomy_dataframe_transaction()
            else:
                self.taxonomy_dataframe_transaction_final = self.taxonomy_dataframe_transaction_final.merge(self.get_taxonomy_dataframe_transaction(), how = 'outer')
                
            if self.get_taxonomy_dataframe_final().shape[0] != 0:
                #self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_{save_id}.csv")
                self.taxonomy_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/final_transaction_dataset_{save_id}.csv")
            else:
                pass
        
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        self.set_taxonomy_dataframe_transaction(pd.DataFrame())
        self.set_taxonomy_dataframe_transaction_final(pd.DataFrame())
    
    '''
    It calculates relative abundance for taxonmy counts.
    '''
    def calculate_relative_abundance_multilevel(self, input_dataframe, sample_id, name):
        self.missing_or_unassigned_taxon = 0
        input_dataframe.rename(columns={'attributes.count':'attributes_count'}, inplace = True)
        for level in TAXONOMY_LEVELS:
            if level in input_dataframe.columns:
                for item in input_dataframe[f'{level}'].unique():
                    try:
                        input_dataframe.loc[input_dataframe[f'{level}'] == f"{item}", f'{level}_count'] = input_dataframe.groupby([f'{level}']).attributes_count.sum()[f'{item}']
                    except:
                        self.missing_or_unassigned_taxon += 1
                self.count_sums_df = input_dataframe.groupby([f'{level}']).attributes_count.sum()
                #print(self.count_sums_df)
                for item in input_dataframe[f'{level}'].unique():
                    input_dataframe.loc[input_dataframe[f'{level}'] == f"{item}", f'{level}_relative_abundance'] = ((input_dataframe[f'{level}_count'] / self.count_sums_df.sum()) * 100).round(10)
            else:
                pass
            print(f'The total number of unassigned taxon and taxon without a value is {self.missing_or_unassigned_taxon}')  
        input_dataframe.to_csv(f"{SAVE_PATH}/relative_abundance_of_{name}_{sample_id}.csv")
        return input_dataframe
    
    
    '''
    It calculates relative abundance for functionality counts.
    '''
    def calculate_relative_abundance(self, input_dataframe, sample_id, name):
        self.count_sums_df = input_dataframe['attributes.count'].sum()
        for item in input_dataframe['attributes.accession'].unique():
            input_dataframe.loc[input_dataframe['attributes.accession'] == f"{item}", 'attributes.relative_abundance'] = ((input_dataframe['attributes.count'] / self.count_sums_df) * 100).round(10)
        input_dataframe.to_csv(f"{SAVE_PATH}/relative_abundance_of_{name}_{sample_id}.csv")
        return input_dataframe    

            
    '''
    Pull selected axonomy and functionality data of the seleted study from MGnify API.
    '''                
    def pull_selected_data(self):
        
        self.set_selected_project_id(str(input("Enter a study ID below:\n")))
        self.set_metadata_response(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{self.get_selected_project_id()}/analyses"))
        
        print(f"\nTaxonomy level names are:\n {TAXONOMY_LEVEL_NAMES}\n")
        print(f"Functionality names are:\n {FUNCTIONALITY_NAMES}\n")
        self.set_user_input(str(input("Enter a taxonomy level or a functionality type below.\nAvailable options are found above.\n\n")))
        while (self.get_user_input() not in TAXONOMY_LEVEL_NAMES) & (self.get_user_input() not in FUNCTIONALITY_NAMES):
            self.set_user_input(str(input("Enter valid taxonomy levels and\or functionality types below.\n\n")))
        
        self.set_user_input_list(self.get_user_input())
        
        self.set_user_input_second(str(input("Would you like to add an additional taxonomy level or a functionality type?\n Enter 'y' for yes or 'n' for no.\n\n")))
        while self.get_user_input_second() not in  ANSWER_LIST:
            self.set_user_input_second(str(input("Enter a valid answer: 'y' for yes or 'n' for no.\n\n")))
            if self.get_user_input_second() == 'n':
                break
            self.set_user_input(str(input("Enter a taxonomy level or a functionality type below.\nAvailable options are found above.\n\n")))
            while (self.get_user_input() not in TAXONOMY_LEVEL_NAMES) & (self.get_user_input() not in FUNCTIONALITY_NAMES):
                self.set_user_input(str(input("Enter valid taxonomy levels and\or functionality types below.\n\n")))
            self.set_user_input_list(self.get_user_input()) 
            self.set_user_input_second(str(input("Would you like to add an additional taxonomy level or a functionality type?\nEnter 'y' for yes or 'n' for no.\n\n")))
        
        
        
        self.n = 0
        print(f"The total number of samples in this project is {len(self.get_metadata_response()['data'])}")
        while self.n < ((len(self.get_metadata_response()['data']))):
           self.get_sample_id_list().append(self.get_metadata_response()['data'][self.n]['id']) 
           
           print(f"Sample {self.n} of the selected project is: {self.get_metadata_response()['data'][self.n]['id']}")
           self.n = self.n + 1
        
        
        if len(self.get_user_input_list()) == 1:
            if str(self.get_user_input_list()[0]) in TAXONOMY_LEVEL_NAMES:
                self.create_taxonomy_transaction_databases('taxonomy', f'taxonomy_{str(self.get_user_input_list()[0]).lower()}', f'attributes.hierarchy.{str(self.get_user_input_list()[0]).lower()}', f'attributes.hierarchy.{str(self.get_user_input_list()[0]).lower()}_relative_abundance')
            elif str(self.get_user_input_list()[0]) in FUNCTIONALITY_NAMES:
                self.create_functionality_transacation_databases(f"{self.get_user_input_list()[0]}", f"{self.get_user_input_list()[0]}")
            else:
                sys.exit(0)
                
        if len(self.get_user_input_list()) > 1:
            for self.item in self.get_user_input_list():
                if str(self.item) in TAXONOMY_LEVEL_NAMES:
                    self.create_taxonomy_transaction_databases('taxonomy', f'taxonomy_{self.item}', f'attributes.hierarchy.{self.item}', f'attributes.hierarchy.{self.item}_relative_abundance')
                elif str(self.item) in FUNCTIONALITY_NAMES:
                    self.create_functionality_transacation_databases(f"{self.item}", f"{self.item}")
                else:
                    sys.exit(0)       
    

    '''
    Pull taxonomy counts of selected project samples and saves them per sample ID.
    '''
    def pull_profile_taxonomy(self, sample_id, name, save_name):
        try:
            self.set_taxonomy_dataframe_merged(pd.DataFrame())
            self.set_taxonomy_response(self.Connect.pull_data(f" https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{sample_id}/{name}"))
            self.set_taxonomy_dataframe_merged(pd.json_normalize(self.get_taxonomy_response()['data']))
            if self.get_taxonomy_dataframe_merged().shape[0] == 0:
                print(f"The {save_name} json file is empty")
            else:
                while self.get_taxonomy_response()['links']['next'] is not None:
                    self.set_taxonomy_response(self.Connect.pull_data(self.get_taxonomy_response()['links']['next']))
                    self.set_taxonomy_dataframe(pd.json_normalize(self.get_taxonomy_response()['data']))
                    self.set_taxonomy_dataframe_merged(pd.concat([self.get_taxonomy_dataframe_merged(), self.get_taxonomy_dataframe()]))
                self.get_taxonomy_dataframe_merged()['Sample_id'] = f"{sample_id}"
                self.get_taxonomy_dataframe_merged().reset_index(drop = True, inplace=True)
                #self.get_taxonomy_dataframe_merged().to_csv(f"{SAVE_PATH}/counts_of_{save_name}_{sample_id}.csv")
        except:
            pass

    '''
    Pull functionality counts of selected project samples and saves them per sample ID.
    '''  
    def pull_profile_functionality(self, sample_id, name, save_name):
        try:
            self.set_functionality_dataframe_merged(pd.DataFrame())
            self.set_functionality_response(self.Connect.pull_data(f" https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{sample_id}/{name}"))
            self.set_functionality_dataframe_merged(pd.json_normalize(self.get_functionality_response()['data']))
            if self.get_functionality_dataframe_merged().shape[0] == 0:
                print(f"The {save_name} json file is empty")
            else:    
                while self.get_functionality_response()['links']['next'] is not None:
                    self.set_functionality_response(self.Connect.pull_data(self.get_functionality_response()['links']['next']))
                    self.set_functionality_dataframe(pd.json_normalize(self.get_functionality_response()['data']))
                    self.set_functionality_dataframe_merged(pd.concat([self.get_functionality_dataframe_merged(), self.get_functionality_dataframe()]))
                self.get_functionality_dataframe_merged().reset_index(drop = True, inplace=True)
                self.get_functionality_dataframe_merged()['Sample_id'] = f"{sample_id}"
                #self.get_functionality_dataframe_merged().to_csv(f"{SAVE_PATH}/counts_of_{name}_functionalities_{sample_id}.csv")
        except:
            pass
    
    '''
    It creates functionality transaction database for selected sample IDs and saves them.
    '''
    def create_functionality_transaction_dataframes(self, sample_id, input_dataframe, output_dataframe, name):
        output_dataframe = copy.deepcopy(input_dataframe)
        try:
            output_dataframe.set_index('attributes.accession', inplace = True)
        except:
            print(f"No column with the title of attributes.relative_abundance in {name}")
            return

        output_dataframe = output_dataframe[['attributes.relative_abundance']]
        output_dataframe = output_dataframe.transpose()
        output_dataframe['Sample_id'] = f"{sample_id}"
        output_dataframe.set_index('Sample_id', inplace = True)
        output_dataframe.to_csv(f"{SAVE_PATH}/counts_of_{name}_functionalities_transactional_{sample_id}.csv")
        self.set_functionality_dataframe_transaction(output_dataframe)
    
    '''
    It creates taxonomy transaction database for selected sample IDs and taxonomy levels and saves them.
    '''
    def create_taxonomy_transaction_dataframes(self, sample_id, input_dataframe, output_dataframe, name, level, level_abundance):
        output_dataframe = copy.deepcopy(input_dataframe)
        output_dataframe.dropna(subset=[f'{level}'], inplace = True)
        output_dataframe.drop_duplicates(f'{level}', inplace = True)
        
        if level == "attributes.hierarchy.species":
            for i, item in enumerate(output_dataframe[f"{level}"]):
                output_dataframe.at[output_dataframe.index[i], f"{level}"] = str(output_dataframe.at[output_dataframe.index[i], "attributes.hierarchy.genus"] + " " + str(item))      
        
        try:
            output_dataframe.set_index(f'{level}', inplace = True)
        except:
            return
        
        output_dataframe = output_dataframe[[f'{level_abundance}']]
        output_dataframe = output_dataframe.transpose()
        output_dataframe['Sample_id'] = f"{sample_id}"
        output_dataframe.set_index('Sample_id', inplace = True)
        output_dataframe.to_csv(f"{SAVE_PATH}/counts_of_{name}_taxonomy_transactional_{sample_id}.csv")
        self.set_taxonomy_dataframe_transaction(output_dataframe)
            


pull_instance = Pull_selected_project()
pull_instance.pull_selected_data()




        
#MGYS00000465