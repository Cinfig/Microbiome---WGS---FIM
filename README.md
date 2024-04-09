# Microbiome---WGS---FIM
This repository implements a frequent itemset mining tool to mine relative abundances of whole genome sequencing (WGS) studies from the MGnify database.

The following relevant files are use the MGnify API:

1. Connector_MGnify.py
2. Pull_all_projects_MGnify.py
3. Pull_selected_project_MGnify.py
4. Mine.py

1. Connector_Mgnify.py
This module sets up the connection with the MGnify API to be able to pull data.
   
2. Pull_all_projects_MGnify.py
   This modul pulls all project data based on the interactively selected human biome type and experiment type.
    - It saves all available human biome types to human_biomes_out.csv
    - It saves all available experiment types to all_sequence_methods_out.csv
    - It saves the final output based on our selection to selected_human_biomes_out.csv
   
   How to use it - step-by-step guide:
      a, Download 'Connector_Mgnify.py' and 'Pull_all_projects_MGnify.py' into the same folder. Files will be saved in the same folder.
      b, Go to that folder in the terminal.
      c, Run the Pull_all_projects_MGnify.py by entering 'python Pull_all_projects_MGnify.py' 
      d, Interactively select a human biome type, for example, 47 for root:Host-associated:Human:Skin) in the console. 
      e, Interactively select the experiment type, for example, 5 for metagenomic. Please note that the script was only tested with the 'metagenomic' experiment type as that    
         experiment type is in the main focus.

3. Pull_selected_project_MGnify.py
   This module pulls selected project data based on a project ID, and selected taxonomy levels and/or functionality categoryies.

   How to use it - step-by-step guide:
    
  
5. Mine.py




