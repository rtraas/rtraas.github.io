#!/usr/bin/env python

'''
Front-facing script to find drifting, narrowband events in a set of generalized
cadences of ON-OFF radio SETI observations.
Part of the Breakthrough Listen software package turboSETI
In this code, the following terminology is used:
Hit = single strong narrowband signal in an observation
Event = a strong narrowband signal that is associated with multiple hits
        across ON observations

The main function contained in this file is *find_event_pipeline*
    Find_event_pipeline calls find_events from find_events.py to read a list
    of turboSETI .dat files. It then finds events within this group of files.

Usage (beta):
    import find_event_pipeline;
    find_event_pipeline.find_event_pipeline(dat_file_list_str,
                                            SNR_cut=10,
                                            check_zero_drift=False,
                                            filter_threshold=3,
                                            on_off_first='ON',
                                            number_in_cadence=6,
                                            on_source_complex_cadence=False,
                                            saving=True,
                                            user_validation=False)

    dat_file_list_str   The string name of a plaintext file ending in .lst
                        that contains the filenames of .dat files, each on a
                        new line, that were created with seti_event.py. The 
                        .lst should contain a set of cadences (ON observations
                        alternating with OFF observations). The cadence can be
                        of any length, given that the ON source is every other
                        file. This includes Breakthrough Listen standard ABACAD
                        as well as OFF first cadences like BACADA. Minimum
                        cadence length is 2, maximum cadence length is
                        unspecified (currently tested up to 6).

                        Example: ABACAD|ABACAD|ABACAD

    SNR_cut             The threshold SNR below which hits in the ON source
                        will be disregarded. For the least strict thresholding,
                        set this parameter equal to the minimum-searched SNR
                        that you used to create the .dat files from
                        seti_event.py. Recommendation (and default) is 10.

    check_zero_drift    A True/False flag that tells the program whether to
                        include hits that have a drift rate of 0 Hz/s. Earth-
                        based RFI tends to have no drift rate, while signals
                        from the sky are expected to have non-zero drift rates.
                        Default is False.

    filter_threshold    Specification for how strict the hit filtering will be.
                        There are 3 different levels of filtering, specified by
                        the integers 1, 2, and 3. Filter_threshold = 1
                        returns hits above an SNR cut, taking into account the
                        check_zero_drift parameter, but without an ON-OFF check.
                        Filter_threshold = 2 returns hits that passed level 1
                        AND that are in at least one ON but no OFFs.
                        Filter_threshold = 3 returns events that passed level 2
                        AND that are present in *ALL* ONs. Default is 3.

    on_off_first        Tells the code whether the .dat sequence starts with
                        the ON or the OFF observation. Valid entries are 'ON'
                        and 'OFF' only. Default is 'ON'.

    number_in_cadence   The number of files in a single ON-OFF cadence.
                        Default is 6 for ABACAD.

    on_source_complex_cadence

                        If using a complex cadence (i.e. ons and offs not
                        alternating), this variable should be the string
                        target name used in the .dat filenames. The code will
                        then determine which files in your dat_file_list_str
                        cadence are ons and which are offs. Default is false.

    saving              A True/False flag that tells the program whether to
                        save the output array as a .csv. Default is True.

    user_validation     A True/False flag that, when set to True, asks if the
                        user wishes to continue with their input parameters
                        (and requires a 'y' or 'n' typed as confirmation)
                        before beginning to run the program. Recommended when
                        first learning the program, not recommended for
                        automated scripts. Default is False.

author:
    Version 3.0 - Raffy Traas (raffytraas14@gmail.com)
    Version 2.0 - Sofia Sheikh (ssheikhmsa@gmail.com),
    Version 1.0 - Emilio Enriquez (jeenriquez@gmail.com)

Last updated: 06/23/2020
***
NOTE: This code works for .dat files that were produced by seti_event.py
after turboSETI version 0.8.2, and blimpy version 1.1.7 (~mid 2019). The
drift rates *before* that version were recorded with the incorrect sign
and thus the drift rate sign would need to be flipped in the make_table
function.
***


Update notes: Updated support for files not beginning with 'spliced'.

NOTE: No support for spliced/non-spliced option select for when
'on_off_first' is 'TRUE'.
'''

#required packages and programs
import find_event
import pandas as pd
import refactor_find_event

#required for find_event and refactor_find_event
import time
import numpy as np

#import helper functions and utilities
import compartmentalizing
from compartmentalizing import *





def refactor_find_event_pipeline(dat_file_list_str,
                        SNR_cut=10,
                        check_zero_drift=False,
                        filter_threshold=3,
                        on_off_first='ON',
                        number_in_cadence=6,
                        on_source_complex_cadence=False,
                        saving=True,
                        user_validation=False):

        
        
    print()
    print("************   BEGINNING FIND_EVENT PIPELINE   **************")
    print()

    
        
    #Informs user of whether the first observation in the cadence is an "ON" or "OFF" observation
    if on_source_complex_cadence == False:
        print("Assuming the first observation is an " + on_off_first)

    if on_source_complex_cadence != False:
        print("Assuming a complex cadence for the following on source: " + on_source_complex_cadence)

        
    
    #Opens the file list
    #Creates a list of files
    dat_file_list, n_files = compartmentalizing.opener(dat_file_list_str, is_test=True)



    #Extracts source names from the created list of files
    source_name_list = compartmentalizing.get_source_names(dat_file_list)



    
    #Creates a list of 
    #This will be skipped because, by default, "on_source_complex_cadence" is set to "False"
    complex_cadence = compartmentalizing.get_complex_cadence(on_source_complex_cadence, source_name_list)



    print("There are " + str(len(dat_file_list)) + " total files in the filelist " + dat_file_list_str)
    print("therefore, looking for events in " + str(int(n_files/number_in_cadence)) + " on-off set(s)")
    print("with a minimum SNR of " + str(SNR_cut))



    #Informing user of filter-search type based on user input configuration
    compartmentalizing.filter_threshold_statements(filter_threshold)



    #Informing user of whether zero drift signals will be included in the search
    compartmentalizing.check_zero_drift_statements(check_zero_drift)



    #Informing user of whether the output file will be saved
    compartmentalizing.save_statements(saving)


    
    #Used for debugging purposes
    #If checkpoint displays, all code is functional before checkpoint
    #Checkpoints need not be placed in exact positions as presented here
    ##compartmentalizing.checkpoint(1)
        
      
    #If "user_validation" = "True" (specified as a parameter in "refactor_find_event_pipeline" call),
    #   queries user input of "Y/N" for validation of inputted parameters
    #Really only useful for debugging purposes
    compartmentalizing.validation(user_validation)


    
    #Used for debugging purposes
    #If checkpoint displays, all code is functional before checkpoint
    #Checkpoints need not be placed in exact positions as presented here
    ##compartmentalizing.checkpoint(2)
        
        
        
    #Looping over as many chunks as specified in "number_in_cadence".
    #Creates a list of candidate events that will be converted into a pandas DataFrame
    #Returns the names and ID's of the elements in the list of candidate events
    candidate_list, name, id_num = compartmentalizing.get_candidates(n_files, number_in_cadence, on_source_complex_cadence, complex_cadence, on_off_first, dat_file_list, SNR_cut, check_zero_drift, filter_threshold, is_test=False)
    


    #Used for debugging purposes
    #If checkpoint displays, all code is functional before checkpoint
    #Checkpoints need not be placed in exact positions as presented here
    ##compartmentalizing.checkpoint(3)


    
    #Converts the created candidate list into a pandas DataFrame
    find_event_output_dataframe = compartmentalizing.convert_to_dataframe_or_list(candidate_list)
        
        
        
    #Outputs the created DataFrame of candidate events 
    find_event_output_dataframe = compartmentalizing.outputs(saving, check_zero_drift, name, id_num, filter_threshold, SNR_cut, find_event_output_dataframe)

        
        
    return find_event_output_dataframe



#The "refactor_event_pipeline" calls below were used for testing purposes
#The list "HIP39826.lst" can be found in the "rtraas/radio-technosignature-searches-of-TESS-stars/turboseti" folder

#refactor_find_event_pipeline('HIP39826.lst')
#refactor_find_event_pipeline('HIP39826.lst', filter_threshold=2)
#refactor_find_event_pipeline('HIP39826.lst', filter_threshold=1)
