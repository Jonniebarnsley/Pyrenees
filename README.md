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
    
- Create an ESGF account with the German Climate Computing Centre (https://esgf-data.dkrz.de/user/add/?next=http://esgf-data.dkrz.de/projects/esgf-dkrz/), taking note of your OpenID and password as you do so.
- Apply for CORDEX access (https://esg-dn1.nsc.liu.se/ac/subscribe/CORDEX_Research) – you may need to try this multiple times before your account is flagged for access.

- Set some environment variables for your ESGF username, password, and the directory in which you want to store the CORDEX data:

    export ESGF_USERNAME=some_username
    export ESGF_PASSWORD=some_password
    export DATA_HOME=/path/to/data

## Data

Follow the code in ESGF_download.ipynb to download CORDEX data from the ESGF data servers to your local data directory.
