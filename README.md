# Microbiome---WGS---FIM
This repository implements a frequent itemset mining tool to mine relative abundances of whole genome sequencing (WGS) studies from the MGnify database.

The following relevant files are use the MGnify and other API:

- Connector_MGnify.py
- Pull_all_projects_MGnify.py
- Pull_selected_project_MGnify.py
- Connect_species_with_functionality.py
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
   
         One file per selected category containing the merged relative abundance numbers of all samples:
   
            In case the "genus" and "species" taxonomy level was selected:
               "final_transaction_dataset_taxonomy_genus.csv"
               "final_transaction_dataset_taxonomy_species.csv"
   
            In case "go-slim" functionality was selected:
               "final_transaction_dataset_go-slim.csv"

4. Connect_species_with_functionality.py
   
      This python module has 3 functions and after launching the script the user need to select which function to run.
   
         -'1' find_species_id(): This function connects the species names of the species data exported from MGnify to the species ID. Firstly, the script looks for exact name match,                                       secondly it looks for the '.sp' not exact name match, and ifnally it looks for the not exact match based on the species' genus name.
   
               Input files:
   
                     'names.csv': This file is a database dump of the species_names-species_ID pairs from NCBI. This file can be to be obtained the following way:
                           Download the taxdump.tar.Z from 'https://ftp.ncbi.nih.gov/pub/taxonomy/'.
                           Rename the file 'names.dmp' to 'names.csv'.
                           Copy 'names.csv' and paste it into the folder of this script.

                     'final_transaction_dataset_taxonomy_species.csv': This is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the two input files need to be in the same folder.

               Output files:

                     'species_and_id_df.csv': This file contains the species name and ID pairs and the type of the match: exact or not exact.

         -'2' connect_taxon_id_and_functionality_id(): This function establishes all possible species and functionalities combinations based on species/functionalities present in the                                                         selected study. The runtime of the function can be extremely long due to multiple API requests.The following QucikGO API is used:

                                                       https://www.ebi.ac.uk/QuickGO/api/index.html#!/annotations/annotationLookupUsingGET

               Input files:

                     'species_and_id_df.csv': This file is the output of the above-mentioned function.

                     'final_transaction_dataset_taxonomy_species.csv': This file is the output of step 3.

                     'final_transaction_dataset_go-slim.csv': This file is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the three input files need to be in the same folder.

               Output files:

                     'goname_goid_df.csv': This file contains go functionality ID and go functionality name pairs. 

                     'taxon_functionality_matrix.csv': This file contains the all possible species ID and functionality combinations.
   
         -'3' create_taxonomy_and_functionality_transaction_dataframes(): This function creates a transactional database considering species and functionalities present in each sample.

               Input files:

                     'species_and_id_df.csv': This file is the output of the first function.

                     'taxon_functionality_matrix.csv': This file is the output of the above-mentioned function.

                     'final_transaction_dataset_taxonomy_species.csv': This file is the output of step 3.

                     'final_transaction_dataset_go-slim.csv': This file is the output of step 3.

               Output files:

                      'taxon_functionality_matrix_final.csv': 

                     
8. Mine.py




