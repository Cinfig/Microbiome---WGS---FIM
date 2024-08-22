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
   
   This modul pulls the names of all projects based on the interactively selected human biome type and experiment type.
    - It saves all available human biome types to human_biomes_out.csv
    - It saves all available experiment types to all_sequence_methods_out.csv
    - It saves the final output based on our selection to selected_human_biomes_out.csv

   The runtime to pull data and save the human_biomes_out.csv and all_sequence_methods_out.csv files is 2 minutes.
   The runtime, for example, to pull the Human skin biom associated studies with metagenomic experiment type (4 out of 35 Human skin biom
   associated studies studies), and save the selected_human_biomes_out.csv is 3.5 minutes.
   
   How to use it - step-by-step guide:
   
      a, Download 'Connector_Mgnify.py' and 'Pull_all_projects_MGnify.py' into the same folder. Files will be saved in the same folder.
   
      b, Go to that folder in the terminal.
   
      c, Run the Pull_all_projects_MGnify.py by entering 'python Pull_all_projects_MGnify.py'
   
      d, Interactively select a human biome type, for example, 47 for root:Host-associated:Human:Skin) in the console.
         ![image](https://github.com/user-attachments/assets/999761aa-1236-4796-832a-37ee6a82fb95)

   
      e, Interactively select the experiment type, for example, 5 for metagenomic. Please note that the script was only tested with the    
         'metagenomic' experiment type as that experiment type is in the main focus.
         ![image](https://github.com/user-attachments/assets/2ff9a78c-d122-4daf-8878-82407f02f4ae)


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

      f, The script prints the sample number in the selected study and the unique ID of each sample.
         ![image](https://github.com/user-attachments/assets/838835bf-bb92-475d-8696-dc2183fe4057)

   
      g, While the script is running, multiple csv files are saved. For example, the above mentioned MGYS00000465 study has 40 samples.

         The runtime of the script to pull species and go-slim composition data of the 40 samples and save the .csv output files is 8
         minutes.
   
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

         One file with sample id details "final_sample_ids.csv":
   
            "Sample_id" (MGYA00005291 - MGYA00005330)
            "Secondary_sample_id" (ERS625306 - ERS625345)
   
            There additional empty columns where sample catgories must be manually populated the folllowing way, for example:
               Category I (Healthy_1_1, Healthy_1_2, Healthy_2_1, etc.) to indicate duplicate samples per person. Populate with "-" if not
               available.
               Category II (Healthy_1, Healthy_1, Healthy_2, etc.) without duplicate sample details. Populate with "-" if not
               available.
               Category III (Healthy, IBD) to indicate the highest level of binary categories. It must be available and populated for the
               later steps.

         One file with go-slim related details "counts_of_functionality_df.csv":
            id - GO:0030031
            attributes.description - cell projection assembly
            attributes.lineage - biological_process
            Sample_id - MGYA00005291

         It is important to manually populate the Categroy I, Category II and Cattegory III columns with actual data or either nan in the
         final_sample_ids.csv, final_transaction_dataset_taxonomy_species.csv and final_transaction_dataset_go-slim.csv. The uploaded files
         are populated with this data.
               
5. Exploratory_data_analysis.py

      This python module has multiple functions to calculate Alpha diversity (richness), Beta diversity (Bray-Curtis), Jaccard similarity, Kruskal-Wallis test.
      Values are visualised by bar chart, box plot or heatmap. To run this module, download the Exploratory_data_analysis.py python module and the
      eda_input_commands.txt file. When the Exploratory_data_analysis.py is executed in command line, the functions in the .txt file will be executed.
      Update the .txt file if you want to control which function to run, to change the input file name, to change an input parameter of a function, etc.

      Functions:

         -'1' calculate_alpha_diversity(input .csv file name, name for visualisation label):

               calculate_alpha_diversity('final_transaction_dataset_taxonomy_species', 'species')
               calculate_alpha_diversity('final_transaction_dataset_go-slim', 'go-lims-functionalities')
   
         -'2' calculate_beta_diversity(input .csv file name, name for visualisation label):

               calculate_beta_diversity('final_transaction_dataset_taxonomy_species', 'species')
               calculate_beta_diversity('final_transaction_dataset_go-slim', 'go-lims-functionalities')
   
         -'3' calculate_jaccard_similarity(input .csv file name, name for visualisation label):

               calculate_jaccard_similarity('final_transaction_dataset_taxonomy_species', 'species')
               calculate_jaccard_similarity('final_transaction_dataset_go-slim', 'go-lims-functionalities')

         -'4' calculate_kruskal_wallis_group_test(input .csv file name, name for visualisation label and output file, the greatest row index (sample number) of the first group):
               My samples were ordered in a specific order. The first 20 samples (row index 0-19) belong to the first group (healthy individuals), and the last 20
               samples (row index 20-39) belong to the second group (ill individuals). 19 is the greatest row number of the first group.

               calculate_kruskal_wallis_group_test('final_transaction_dataset_taxonomy_species', 'species', 19)
               calculate_kruskal_wallis_group_test('final_transaction_dataset_go-slim', 'go-slim', 19)
      

      Input files:

         'final_transaction_dataset_taxonomy_species.csv' and 'final_transaction_dataset_go-slim' are the outputs of the Pull_selected_project_MGnify.py.

      Output files:

         The files names depend on the entered parameters of the function. In my case the file names with the 'species' parameter were the following:

               EDA - alpha diversity - species.csv
               EDA - alpha diversity - richness - species.png
               EDA - alpha diversity - data summary - species.png
               EDA - beta_diversity - species.csv
               EDA - beta diversity - Bray-Curtis - species.png
               EDA - Jaccard similarity - species.csv
               EDA - Jaccard similarity - species.png
               EDA - Kruskal wallis group test - species.csv
   
6. Connect_species_with_functionality.py
   
      This python module has 4 functions and after launching the script the user need to select which function to run.
   
         -'1' find_species_id_offline(): This function connects the species names of the species data exported from MGnify to the species ID. It
         runs offline using an exported NCBI data dump. Firstly, the script looks for exact name match, secondly it looks for the '.sp' not exact
         name match, and finally it looks for the not exact match based on the species' genus name.
   
               Input files:
   
                     'names.csv': This file is a database dump of the species_names-species_ID pairs from NCBI. This file can be to be obtained the
                     following way:
                           Download the taxdump.tar.Z from 'https://ftp.ncbi.nih.gov/pub/taxonomy/'.
                           Rename the file 'names.dmp' to 'names.csv'.
                           Copy 'names.csv' and paste it into the folder of this script.

                     'final_transaction_dataset_taxonomy_species.csv': This is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the two input files need to be in the same folder.

               Output files:

                     'species_and_id_df_offline.csv': This file contains the species name and ID pairs and the type of the match: exact or not exact.
   
         -'2' find_species_id_online(): This function connects the species names of the species data exported from MGnify to the species ID. It runs
         online utilising NCBI's EDirect access. Firstly, the script looks for exact name match, secondly it looks for the '.sp' not exact name
         match, and finally it looks for the not exact match based on the species' genus name. First, the package of NCBI's EDirect access needs to
         be installed: https://www.ncbi.nlm.nih.gov/books/NBK179288/
         Before you run this function, the export PATH=${HOME}/edirect:${PATH} needs to be run in the CLI to activate the EDirect access.

               Input files:

                     'final_transaction_dataset_taxonomy_species.csv': This is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the input file need to be in the same folder.

               Output files:

                     'species_and_id_df_online.csv': This file contains the species name and ID pairs and the type of the match: exact or not exact.
            
         -'3' connect_taxon_id_and_functionality_id(category = 'offline'): This function establishes all possible species and
         functionalities combinations based on species/functionalities present in the selected study. The runtime of the
         function can be extremely long due to multiple API requests.The following QucikGO API is used:

               https://www.ebi.ac.uk/QuickGO/api/index.html#!/annotations/annotationLookupUsingGET

               Input files:

                     'species_and_id_df_offline.csv': This file is the output of the find_species_id_offline() function.

                     'final_transaction_dataset_taxonomy_species.csv': This file is the output of step 3.

                     'final_transaction_dataset_go-slim.csv': This file is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the three input files need to be in the same folder.

               Output file:

                     'taxon_functionality_matrix.csv': This file contains the all possible species ID and functionality combinations.

         -'4' connect_taxon_id_and_functionality_id(category = 'online'): This function establishes all possible species and
         functionalities combinations based on species/functionalities present in the selected study. The runtime of the
         function can be extremely long due to multiple API requests.The following QucikGO API is used:

               https://www.ebi.ac.uk/QuickGO/api/index.html#!/annotations/annotationLookupUsingGET

               Input files:

                     'species_and_id_df_online.csv': This file is the output of the find_species_id_online() function.

                     'final_transaction_dataset_taxonomy_species.csv': This file is the output of step 3.

                     'final_transaction_dataset_go-slim.csv': This file is the output of step 3.

                     The 'Connect_species_with_functionality.py' python module and the three input files need to be in the same folder.

               Output file:

                     'taxon_functionality_matrix.csv': This file contains the all possible species ID and functionality combinations.
   
         -'5' create_taxonomy_and_functionality_transaction_dataframes(): This function creates a transactional database considering
         species and functionalities present in each sample.

               Input files:

                     'species_and_id_df_online.csv' or 'species_and_id_df_offline.csv': First, it tries to load in the 'online'
                     file and then the 'offline' file.

                     'taxon_functionality_matrix.csv': This file is the output of the above-mentioned function.

                     'final_transaction_dataset_taxonomy_species.csv': This file is the output of step 3.

                     'final_transaction_dataset_go-slim.csv': This file is the output of step 3.

               Output files:

                     'final_taxon_functionality_transaction_dataset.csv': This file is the transactional database of species and
                     functionlity combinations per sample. 

                     
7. Mining.py

      The mining_input_commands.txt file is populated with all necessary functions. In this .txt file it is possible to control what to execute when the Mining.py module is run. Donwload the Mining.py module,
      mining_input_commands.txt and the required input files
   
      -'1' The update_dataframes() function only need to be executed once per transactional dataset to transform it to the correct format. The input file is the output file of step 4. Ensure that the Category I,
      Category II and Category III columns are populated in that file. Binary values in the Category III column will be used to split the transactional dataset. If a go-slim transaction dataste is updated, an
      additional parameter (update_functionality_ID_file) is required to transform GO Id-s GO Names. The input and output files are uploaded.

               update_dataframes(input_file = 'final_transaction_dataset_taxonomy_species')
               update_dataframes(input_file = 'final_transaction_dataset_go-slim', update_functionality_ID_file = 'counts_of_functionality_df')

      -'2' Investigating the effect of selected relative abundance threshold value on the number of species and go-slim functionalities. Run the functions in pairs (species and go-slim), otherwise the 'abund_cutoff',
      'abund_filtered', 'presence_absence_evaluation' output files will be overwritten. The abundance threshold values investigated are 0.01, 0.05 and 0.1. The 0.1 value was selected.  The input file is the output file
      of step 4. The input and output files are uploaded.

               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")

               FPGrowth(abundance_threshold = 0.05, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")
               FPGrowth(abundance_threshold = 0.05, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")

               FPGrowth(abundance_threshold = 0.01, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")
               FPGrowth(abundance_threshold = 0.01, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")

      -'3' Investigating the effect of minimum support value from 0.4 to 0.9 with 0.1 increment. The 0.6 value was selected. As only the 'fpgrowth_mining...' output files are required for the evaluation, all lines can
      be run together, but discard the 'abund_cutoff', 'abund_filtered', 'presence_absence_evaluation' output files due to being overwritten. Optionally run the functions in pairs. The input file is the output
      file of step 4. The input and output files are uploaded.

               FPGrowth(abundance_threshold = 0.1, min_support = 0.9, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.9, input_file = "final_transaction_dataset_go-slim_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.8, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.8, input_file = "final_transaction_dataset_go-slim_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.7, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.7, input_file = "final_transaction_dataset_go-slim_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.5, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.5, input_file = "final_transaction_dataset_go-slim_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.4, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.4, input_file = "final_transaction_dataset_go-slim_new_columns")

         -'4' Run the FPgrowth frequent itemset mining algorithm with the selected 0.6 minimum support value for species and functonality. The input file is the output file of step 4. The input and output files are
         uploaded. All functions can be run together. All samples, healthy samples, ill samples are mined separately.

               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_HEALTHY_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_IBD_new_columns")

               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_HEALTHY_new_columns")
               FPGrowth(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_IBD_new_columns")

         -'5' Apriori algorithm is also supported, it is optional. The input file is the output file of step 4. The input and output files are uploaded. All functions can be run together.  All samples, healthy samples,
         ill samples are mined separately.

               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_new_columns")
               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_HEALTHY_new_columns")
               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_taxonomy_species_IBD_new_columns")

               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_new_columns")
               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_HEALTHY_new_columns")
               Apriori(abundance_threshold = 0.1, min_support = 0.6, input_file = "final_transaction_dataset_go-slim_IBD_new_columns")

         -'6' The effect of minimum confidence value is investigated here. Ensure that the correct 'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered' file is used, which was generated with the
        'fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6' file. All lines can be run altogether. The input file is the output file of either the FPGrowth or Apriori algorithm.
         The input and output files are uploaded.

               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.4, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.4, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
        
               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.5, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.5, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
        
               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.6, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.6, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
        
               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
        
               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.8, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.8, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
        
               Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.9, 'taxonomy_all_species',
              'final_transaction_dataset_taxonomy_species_new_columns_abund_filtered')
               Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.9,'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')

         -'7' Run association rules mining with 0.7 confidence value. All lines can be run altogether.The input and output files are uploaded.

               #Association_rules_mining('fpgrowth_mining_taxonomy_species_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'taxonomy_all_species',
               'final_transaction_dataset_taxonomy_species_new_columns_C')
               #Association_rules_mining('fpgrowth_mining_taxonomy_species_HEALTHY_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7,
               'taxonomy_species_HEALTHY','final_transaction_dataset_taxonomy_species_HEALTHY_new_columns_abund_filtered')
#Association_rules_mining('fpgrowth_mining_taxonomy_species_IBD_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'taxonomy_species_IBD', #'final_transaction_dataset_taxonomy_species_IBD_new_columns_abund_filtered')

#Association_rules_mining('fpgrowth_mining_go-slim_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'go-slim_all', 'final_transaction_dataset_go-slim_new_columns_abund_filtered')
#Association_rules_mining('fpgrowth_mining_go-slim_HEALTHY_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7,'go-slim_HEALTHY', 'final_transaction_dataset_go-slim_HEALTHY_new_columns_abund_filtered')
#Association_rules_mining('fpgrowth_mining_go-slim_IBD_new_columns_abundance_threshold_0.1_min_support_0.6', 'confidence', 0.7, 'go-slim_IBD', 'final_transaction_dataset_go-slim_IBD_new_columns_abund_filtered')




