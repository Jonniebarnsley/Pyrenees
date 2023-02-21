# Pyrenees in CORDEX

Collaborative codebase to investigate the present and future Pyrenees climate in the Coordinated Regional climate Downscaling Experiment (CORDEX).

## Introduction

CORDEX is an internationally coordinated effort to produce high-resolution regional climate model data for several of the world's key regions. Boundary conditions for the regions are provided by an ensemble of General Circulation Models (GCMs), with high-resolution Regional Climate Models (RCMs) handling the dynamics within the region. The project has standardised a number of experiments for each GCM-RCM pair to run, including a historical run and one for each Representative Concentration Pathway (RCP). The full dataset can be browsed manually at https://esgf-data.dkrz.de/search/cordex-dkrz/. For the Pyrenees, the region of interest has the code 'EUR-11'.

This codebase includes instructions on how to access, download, and analyse CORDEX data, allowing the user to reproduce figures from the 2023 London NERC DTP Field Trip field guide.

## Setup

- Clone the repositry directly from github:

        $ git clone https://github.com/Jonniebarnsley/Pyrenees
        $ cd Pyrenees

- Create new conda environment with all required dependencies using cordex.yml

        $ conda env create -f cordex.yml
        $ conda activate cordex
    
- Create an ESGF account with the German Climate Computing Centre (https://esgf-data.dkrz.de/user/add/?next=http://esgf-data.dkrz.de/projects/esgf-dkrz/).
- Apply for CORDEX access (https://esg-dn1.nsc.liu.se/ac/subscribe/CORDEX_Research) – you may need to try this multiple times before your account is flagged for access.

- Set some environment variables for your ESGF username, password, and the directory in which you want to store the CORDEX data:

        $ export ESGF_USERNAME=some_username
        $ export ESGF_PASSWORD=some_password
        $ export DATA_HOME=/path/to/data

## Data

To download tas and pr data for the historical, rcp26 and rcp85 experiments, simply use:

        $ python download.py
        
Or, to access different datasets, follow the instructions in download_tutorial.ipynb to customise your download.

NB: Some datasets are likely to be unavailable at any given time due to maintenance of the ESGF data nodes. If you encounter an error downloading the data, try again a day or two later to see if the problem has resolved. Running ESGF_download.py again will skip any datasets already downloaded and continue with any missing datasets.