# Microbiome---WGS---FIM
This repository implements a frequent itemset mining tool to mine relative abundances of whole genome sequencing (WGS) studies from the MGnify database.

The following relevant files are use the MGnify API:

- Connector_MGnify.py
- Pull_all_projects_MGnify.py
- Pull_selected_project_MGnify.py
- Mine.py

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
      e, Interactively select the experiment type, for example, 5 for metagenomic. Please note that the script was only tested with the    
         'metagenomic' experiment type as that experiment type is in the main focus.

3. Pull_selected_project_MGnify.py
   This module pulls project data based on a selected project ID, a selected taxonomy levels and/or functionality categoryies.

   How to use it - step-by-step guide:
      a, Download 'Pull_selected_project_MGnify.py'.
      b, Download 'Connector_Mgnify.py' if you skipped point 2 above.
      c, Enter a study ID, for example, 'MGYS00000465'.
      d, Enter a taxonomy level or functionaltity from the printed options:

         Taxonomy level names are:
             ['domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

         Functionality names are:
             ['go-slim', 'go-terms', 'antismash-gene-clusters', 'genome-properties', 'interpro-identifiers']
   
      e, The script will ask if you would like to add another taxonomy level/functionality.
   
         Would you like to add an additional taxonomy level or a functionality type?
         Enter 'y' for yes or 'n' for no.

         Please note if the selected taxonomy level/functionality is not available in the selected study ID, no files will be downloaded.

      f, The scripts print the number samples in the selected study and the unique ID of each sample.
   
      g, While the script is running, multiple csv files are saved. For example, the above mentioned MGYS00000465 study has 25 samples.
   
         One csv file containing the relative abundance will be saved per unique sample ID:
            In case the "genus" and "species" taxonomy level was selected:
               "relative_abundance_of_taxonomy_genus_sample_ID.csv"
               "relative_abundance_of_taxonomy_species_sample_ID.csv"
               
            In case "go-slim" functionality was selected:
               "relative_abundance_of_go-slim_functionalities_sample_ID.csv"

         One csv file containing the count numbers will be saved per unique sample ID:
            In case the "genus" and "species" taxonomy level was selected:
               "counts_of_taxonomy_genus_taxonomy_transactional_sample_ID.csv"
               "counts_of_taxonomy_species_taxonomy_transactional_sample_ID.csv"

            In case "go-slim" functionality was selected:
               "counts_of_go-slim_functionalities_transactional_sample_ID.csv"
   
         One file per selected category containing the merged relative abundance numbers of all samples.
            In case the "genus" and "species" taxonomy level was selected:
               "final_transaction_dataset_taxonomy_genus.csv"
               "final_transaction_dataset_taxonomy_species.csv"
   
            In case "go-slim" functionality was selected:
               "final_transaction_dataset_go-slim.csv"
   
5. Mine.py




