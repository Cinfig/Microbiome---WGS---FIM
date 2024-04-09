# Microbiome---WGS---FIM
This repository implements a frequent itemset mining tool to mine relative abundances of whole genome sequencing (WGS) studies from the MGnify database.

Relevant files are using the MGnify API:

Connector_MGnify.py
Pull_all_projects_MGnify.py
Pull_selected_project_MGnify.py
Mine.py

1. Connector_Mgnify.py
This module sets up the connection with the MGnify API to be able to pull data.
   
2. Pull_all_projects_MGnify.py
This modul pulls project data based on the interactively selected human biome type and experiment type.
    - It saves all available human biome types to human_biomes_out.csv
    - It saves all available experiment types to all_sequence_methods_out.csv
    - It saves the final output based on our selection to selected_human_biomes_out.csv
    - 
How to use it - step-by-step guide:

First, run the Pull_all_projects_MGnify.py in the console. 
Interactively select a human biome type (for example: 47 - root:Host-associated:Human:Skin) in the console. 
Similarily, interactively select the experiment type (for example: 5 - metagenomic). 
Please note that the script was only tested with the 'metagenomic' experiment type as that experiment type is in the focus.

3. Pull_selected_project_MGnify.py
This module pulls selected project data based on a project ID.
    
  
5. Mine.py




