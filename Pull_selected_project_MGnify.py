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
TAXONOMY_LEVELS_COUNTS = ['attributes.domain_count', 'attributes.hierarchy.phylum_count', 'attributes.hierarchy.class_count', 'attributes.hierarchy.order_count', 'attributes.hierarchy.family_count', 'attributes.hierarchy.genus_count', 'attributes.hierarchy.species_count']


class Pull_selected_project:
    
    def __init__(self):
        self.Connect = Conn.Connector()
        #self.get_projects = pull.Pull_all_projects()
        #self.get_projects.pull_selected_datasets()
        self.selected_project_id = ""
        self.metadata_response = ""
        self.sample_id_list = []
        self.taxonomy_response = ""
        self.functionality_response = ""
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
                self.get_functionality_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_functionality_{save_id}.csv")
                self.functionality_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/final_transaction_dataset_{save_id}.csv")
            else:
                pass

        self.set_functionality_dataframe_final(pd.DataFrame())
        self.set_functionality_dataframe_merged(pd.DataFrame())
        self.set_functionality_dataframe_transaction(pd.DataFrame())
        self.set_functionality_dataframe_transaction_final(pd.DataFrame())
    
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
                self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_{save_id}.csv")
                self.taxonomy_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/final_transaction_dataset_{save_id}.csv")
            else:
                pass
        
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        self.set_taxonomy_dataframe_transaction(pd.DataFrame())
        self.set_taxonomy_dataframe_transaction_final(pd.DataFrame())
                
                    
    def pull_selected_data(self):
        
        self.set_selected_project_id(str(input("Enter a study ID below:\n")))
        self.set_metadata_response(self.Connect.pull_data(f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{self.get_selected_project_id()}/analyses"))
    
        n = 0
        print(f"The total number of samples in this project is {len(self.get_metadata_response()['data'])}")
        while n < ((len(self.get_metadata_response()['data']))):
           self.get_sample_id_list().append(self.get_metadata_response()['data'][n]['id']) 
           
           print(f"Sample {n} of the selected project is: {self.get_metadata_response()['data'][n]['id']}")
           n = n + 1
        
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_domain', 'attributes.domain', 'attributes.domain_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_phylum', 'attributes.hierarchy.phylum', 'attributes.hierarchy.phylum_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_class', 'attributes.hierarchy.class', 'attributes.hierarchy.class_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_order', 'attributes.hierarchy.order', 'attributes.hierarchy.order_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_family', 'attributes.hierarchy.family', 'attributes.hierarchy.family_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_genus', 'attributes.hierarchy.genus', 'attributes.hierarchy.genus_relative_abundance')
        self.create_taxonomy_transaction_databases('taxonomy', 'taxonomy_species', 'attributes.hierarchy.species', 'attributes.hierarchy.species_relative_abundance')
        #self.create_functionality_transacation_databases('go-slim', 'go_slim')
        #self.create_functionality_transacation_databases('go-terms', 'go_terms')
        #self.create_functionality_transacation_databases('antismash-gene-clusters', 'antismash_gene_clusters')
        #self.create_functionality_transacation_databases('genome-properties', 'genome_properties')
        #self.create_functionality_transacation_databases('interpro-identifiers', 'interpro_identifiers')
        

    

    '''
    Pull counts of selected project samples
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
                self.get_taxonomy_dataframe_merged().to_csv(f"{SAVE_PATH}/counts_of_{save_name}_{sample_id}.csv")
        except:
            pass


    
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
                self.get_functionality_dataframe_merged().to_csv(f"{SAVE_PATH}/counts_of_{name}_functionalities_{sample_id}.csv")
        except:
            pass
    
    
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
    
    def create_taxonomy_transaction_dataframes(self, sample_id, input_dataframe, output_dataframe, name, level, level_abundance):
        output_dataframe = copy.deepcopy(input_dataframe)
        output_dataframe.dropna(subset=[f'{level}'], inplace = True)
        output_dataframe.drop_duplicates(f'{level}', inplace = True)
        
        try:
            output_dataframe.set_index(f'{level}', inplace = True)
        except:
            return
        
        print(level)
        output_dataframe = output_dataframe[[f'{level_abundance}']]
        output_dataframe = output_dataframe.transpose()
        output_dataframe['Sample_id'] = f"{sample_id}"
        output_dataframe.set_index('Sample_id', inplace = True)
        output_dataframe.to_csv(f"{SAVE_PATH}/counts_of_{name}_taxonomy_transactional_{sample_id}.csv")
        self.set_taxonomy_dataframe_transaction(output_dataframe)
            
    
    
    def calculate_relative_abundance(self, input_dataframe, sample_id, name):
        self.count_sums_df = input_dataframe['attributes.count'].sum()
        for item in input_dataframe['attributes.accession'].unique():
            input_dataframe.loc[input_dataframe['attributes.accession'] == f"{item}", 'attributes.relative_abundance'] = ((input_dataframe['attributes.count'] / self.count_sums_df) * 100).round(10)
        input_dataframe.to_csv(f"{SAVE_PATH}/relative_abundance_of_{name}_{sample_id}.csv")
        return input_dataframe
    
    def calculate_relative_abundance_multilevel(self, input_dataframe, sample_id, name):
        input_dataframe.rename(columns={'attributes.count':'attributes_count'}, inplace = True)
        for level in TAXONOMY_LEVELS:
            if level in input_dataframe.columns:
                for item in input_dataframe[f'{level}'].unique():
                    try:
                        input_dataframe.loc[input_dataframe[f'{level}'] == f"{item}", f'{level}_count'] = input_dataframe.groupby([f'{level}']).attributes_count.sum()[f'{item}']
                    except:
                        print('The taxon is unassigned or the values is missing')
                self.count_sums_df = input_dataframe.groupby([f'{level}']).attributes_count.sum()
                print(self.count_sums_df)
                for item in input_dataframe[f'{level}'].unique():
                    input_dataframe.loc[input_dataframe[f'{level}'] == f"{item}", f'{level}_relative_abundance'] = ((input_dataframe[f'{level}_count'] / self.count_sums_df.sum()) * 100).round(10)
                    
            else:
                pass
        input_dataframe.to_csv(f"{SAVE_PATH}/relative_abundance_of_{name}_{sample_id}.csv")
        return input_dataframe
    
    '''
    def merge_functionality_transaction_dataframes(self, input_dataframe, output_dataframe, name):
        print(input_dataframe.shape)
        print(input_dataframe.T.columns)
        print(output_dataframe.shape)
        output_dataframe = output_dataframe.merge(input_dataframe.T, how = 'outer')
        output_dataframe.to_csv(f"{SAVE_PATH}/merged_counts_of{name}.csv")
    '''
        
      

instance_2 = Pull_selected_project()
instance_2.pull_selected_data()
        
        









'''
        
        #MGYS00000518
        for item in self.get_sample_id_list():
            # Get all taxonomy data from all samples.
            self.pull_profile_taxonomy(item, 'taxonomy', 'taxonomy')
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            #Placeholder for create_taxonomy_transaction_dataframes()
        
        if self.get_taxonomy_dataframe_final().shape[0] != 0:
            self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy.csv")
            #Placeholder to calculate relative abundance
        else:
            pass
        
        
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        
        
        
        for item in self.get_sample_id_list():
            # Get all taxonomy ssu data from all samples.
            self.pull_profile_taxonomy(item, 'taxonomy/ssu', 'taxonomy_ssu')
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            #Placeholder for create_taxonomy_transaction_dataframes()

        if self.get_taxonomy_dataframe_final().shape[0] != 0:
            self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_ssu.csv")
            #Placeholder to calculate relative abundance
        else:
            pass
        
            
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        
        
        
        for item in self.get_sample_id_list():
            # Get all taxonomy lsu data from all samples.
            self.pull_profile_taxonomy(item, 'taxonomy/lsu', 'taxonomy_lsu')
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            #Placeholder for create_taxonomy_transaction_dataframes()
            
        if self.get_taxonomy_dataframe_final().shape[0] != 0:
            self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_lsu.csv")
            #Placeholder to calculate relative abundance
        else:
            pass
        
        
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        
        
            
        for item in self.get_sample_id_list():
            # Get all taxonomy unite data from all samples.
            self.pull_profile_taxonomy(item, 'taxonomy/unite', 'taxonomy_unite')
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            #Placeholder for create_taxonomy_transaction_dataframes()

        if self.get_taxonomy_dataframe_final().shape[0] != 0:
            self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_unite.csv")
            #Placeholder to calculate relative abundance
        else:
            pass
        
            
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        
        
        
        for item in self.get_sample_id_list():
            # Get all itsonedb data from all samples.
            self.pull_profile_functionality(item, 'taxonomy/itsonedb', 'taxonomy_itsonedb')
            self.set_taxonomy_dataframe_final(pd.concat([self.get_taxonomy_dataframe_final(), self.get_taxonomy_dataframe_merged()]))
            self.get_taxonomy_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_taxonomy_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            #Placeholder for create_taxonomy_transaction_dataframes()

        if self.get_taxonomy_dataframe_final().shape[0] != 0:
            self.get_taxonomy_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_taxonomy_itsonedb.csv")
            #Placeholder to calculate relative abundance
        else:
            pass
            
        self.set_taxonomy_dataframe_final(pd.DataFrame())
        self.set_taxonomy_dataframe_merged(pd.DataFrame())
        
    
        
        for item in self.get_sample_id_list():
            # Get all go-slim data from all samples.
            self.pull_profile_functionality(item, 'go-slim', 'go_slim')
            self.set_functionality_dataframe_final(pd.concat([self.get_functionality_dataframe_final(), self.get_functionality_dataframe_merged()]))
            self.get_functionality_dataframe_final().reset_index(drop = True, inplace=True)
            if self.get_functionality_dataframe_final().shape[0] == 0:
                break
            else:
                pass
            self.set_functionality_dataframe_merged(self.calculate_relative_abundance(self.get_functionality_dataframe_merged(), item, 'go-slim'))
            #print(self.get_functionality_dataframe_merged()['attributes.relative_abundance'])
            #self.create_functionality_transaction_dataframes(item, self.get_functionality_dataframe_merged(), self.get_functionality_dataframe_transaction(), 'go_slim') # may go under else
            self.create_functionality_transaction_dataframes(item, self.get_functionality_dataframe_merged(), self.get_functionality_dataframe_transaction(), 'go_slim')
            if self.functionality_dataframe_transaction_final.shape[0] == 0:
                self.functionality_dataframe_transaction_final = self.get_functionality_dataframe_transaction()
                #print(self.functionality_dataframe_transaction_final.shape)
                #print(self.functionality_dataframe_transaction.shape)
            else:
                self.functionality_dataframe_transaction_final = self.functionality_dataframe_transaction_final.merge(self.get_functionality_dataframe_transaction(), how = 'outer')
                #print(self.functionality_dataframe_transaction_final.shape)
            
        if self.get_functionality_dataframe_final().shape[0] != 0:
            #self.calculate_relative_abundance(self.get_functionality_dataframe_merged(), self.get_functionality_dataframe_merged_final(), 'go_slim')
            #self.calculate_relative_abundance(self.get_functionality_dataframe_final(), 'go_slim')
            self.get_functionality_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_functionality_go_slim.csv") #swapped order
            self.functionality_dataframe_transaction_final.to_csv(f"{SAVE_PATH}/final_transaction_dataset_go_slim.csv")
            
        else:
            pass
        
        self.set_functionality_dataframe_final(pd.DataFrame())
        self.set_functionality_dataframe_merged(pd.DataFrame())
        self.set_functionality_dataframe_transaction(pd.DataFrame())
        self.set_functionality_dataframe_transaction_final(pd.DataFrame())
        

        self.calculate_relative_abundance(self.get_taxonomy_dataframe_merged(), self.get_taxonomy_dataframe_merged_final(), 'taxonomy')
        self.calculate_relative_abundance(self.get_functionality_dataframe_merged(), self.get_functionality_dataframe_merged_final(), 'interpro_identifier')



        
        #self.get_taxonomy_dataframe_merged_final().to_csv(f"{SAVE_PATH}/relative_abundance_of_taxonomy.csv")
        
        try:
            self.get_functionality_dataframe_final().to_csv(f"{SAVE_PATH}/counts_of_functionalities.csv")
        except:
            pass
        
        #self.get_functionality_dataframe_merged_final().to_csv(f"{SAVE_PATH}/relative_abundance_of_functionalities.csv")
        
        try:
            self.get_functionality_dataframe_transaction_final().to_csv(f"{SAVE_PATH}/transactional_db_functionalities.csv")
        except:
            pass
'''
