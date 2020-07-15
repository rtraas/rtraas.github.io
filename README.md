# turboCLOUD
Doppler Drift Searches for Radio Technosignatures in Breakthrough Listen's Follow-Up Observations of TESS Targets

A repo of my work during my 10-week internship with Breakthrough Listen @UCBerkeleySETI

## Project Objectives
1. Port turbo_seti (https://github.com/UCBerkeleySETI/turbo_seti) to a GCP instance
2. Use GCP to perform doppler drift searches for radio technosignatures in TESS targets

## Getting Started

`turbo_seti_docker_tutorial.ipynb` --- A tutorial on using Docker to get your hands on turbo_seti

`docker_run_template.txt` --- A text file containing a template of the command to build a container based off the turbo_seti docker image 

`GettingStarted.md` --- Where you should start if you're looking to get started with turboCLOUD.  It explains how to use all of the different functions as well as the ins and outs of turboCLOUD

## Python Scripts

`superseti.py` --- Used for performing turbo_seti on a batch of files

`make_lst.py`  --- Used for creating properly ordered cadence lists



## Bash Scripts
All bash scripts are modified scripts from /datax/scratch/karenp/turbo_event at the Breakthrough Listen Data Center at UC-Berkeley

`L_BandFDoppSearch.sh` --- Used to run turboSETI on all L_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`S_BandFDoppSearch.sh` --- Used to run turboSETI on all S_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`X_BandFDoppSearch.sh` --- Used to run turboSETI on all X_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance

`C_BandFDoppSearch.sh` --- Used to run turboSETI on all C_band files from the GCS bucket "bl_tess" mounted to the directory "/home/raffytraas14/seti_tess/" on the Google Compute Engine Instance
