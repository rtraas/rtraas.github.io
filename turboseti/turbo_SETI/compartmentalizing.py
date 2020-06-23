import refactor_find_event
import pandas as pd

import time
import numpy as np

def checkpoint(num):
    print('========================= This is checkpoint number ' + str(num) + ' =====================')

def opener(file_list, is_test=False):
    """
    OUTPUTS: dats_list, num_dats
    Opens the files and returns a list of data files, and the length of that list.
    """

    dats = open(file_list).readlines()
    dats = [files.replace('\n','') for files in dats]
    dats = [files.replace(',','') for files in dats]
    dats_list = dats

    num_dats = len(dats)

    if is_test:
        print("dat_file_list = ", dats_list)
        print("n_files = ", num_dats)

    return dats_list, num_dats

def get_source_names(dat_list, is_test=False):
    """
    OUTPUTS: source_names [list]
    Creates a list of source names.
    """

    sources = []
    for dat in dat_list:
        if dat.split('_')[0] == 'spliced':
            s_name = dat.split('_')[5]
        else:
            s_name = dat.split('_')[3]
        sources.append(s_name)
    if is_test:
        print("source_names = ", sources)

    return sources

def get_complex_cadence(on_source_complex_cadence, source_names):
    """
    OUTPUTS: Returns a list for complex_cadence.
    Creates complex_cadence list.
    """

    if on_source_complex_cadence != False:
        CC = []
        for i in range(0, len(source_names)):
            source = source_names[i]
            if source == on_source_complex_cadence:
                CC.append(1)
            else:
                CC.append(0)
        print("The derived cadence is: " + str(CC))
        return CC

def filter_threshold_statements(f_thresh):
    if f_thresh == 1:
        print("Present in A source only, above SNR_cut")
    if f_thresh == 2:
        print("Present in at least one A source with RFI rejection from the off-sources")
    if f_thresh == 3:
        print("Present in all A sources with RFI rejection from the off-sources")

def check_zero_drift_statements(check_drift):
    if check_drift == False:
        print("not including signals with zero drift")
    if check_drift == True:
        print("including signals with zero drift")

def save_statements(save):
    if save == False:
        print("Not saving the output files")
    if save == True:
        print("Saving the output files")

def validation(get_validation):
    if get_validation == True:
        question = "Do you wish to proceed with these settings?"
        while "the answer is invalid":
            reply = str(input(question+' (y/n): ')).lower().strip()
            if reply == '':
                return
            if reply[0] == 'y':
                break
            if reply[0] == 'n':
                return

def get_candidates(n_files, number_in_cadence, on_source_complex_cadence, complex_cadence, on_off_first, dat_file_list, SNR_cut, check_zero_drift, filter_threshold, is_test=False):
    """
    OUTPUTS: list_of_candidates, target_name, target_id
    Creates a list of candidate events by looping over cadence "chunks".
    Also returns target names and target ID numbers.
    """
    list_of_candidates = []
    for i in range((int(n_files/number_in_cadence))):
        sublist = dat_file_list[number_in_cadence*i:((i*number_in_cadence)+(number_in_cadence))]
        #made switch from "complex_cadence" to "on_source_complex_cadence" (06/22/2020:::16:18)
        #if complex_cadence == False:
        if on_source_complex_cadence == False:
            if on_off_first == "ON":

                if sublist[0].split('_')[0] == "spliced":
                    target_name = sublist[0].split('_')[5]
                    target_id = (sublist[0].split('_')[6]).split('.')[0]

                else:
                    target_name = sublist[0].split('_')[3]
                    target_id = (sublist[0].split('_')[4]).split('.')[0]
        else:
            if sublist[0].split('_')[0] == "spliced":
                target_name = sublist[complex_cadence.index(1)].split('_')[5]
                target_id = sublist[complex_cadence.index(1)].split('_')[6].split('.')[0]
            else:
                target_name = sublist[complex_cadence.index(1)].split('_')[3]
                target_id = sublist[complex_cadence.index(1)].split('_')[4].split('.')[0]

        print()
        print("***       " + target_name + "       ***")
        print()

        C = refactor_find_event.find_events(sublist,
                                   SNR_cut=SNR_cut,
                                   check_zero_drift=check_zero_drift,
                                   filter_threshold=filter_threshold,
                                   on_off_first=on_off_first,
                                   on_source_complex_cadence=on_source_complex_cadence,
                                   complex_cadence=complex_cadence)
        C_len = 1
        if C is None:
            C_len = 0
        if C_len != 0:
            list_of_candidates.append(C)

        return list_of_candidates, target_name, target_id

def convert_to_dataframe_or_list(cs):
    """
    OUTPUTS: Retuns the find_event_output_dataframe (if candidates exist).
    If candidates exist, this function converts the candidate_list to a pandas dataframe.
    """

    if len(cs) > 0:
        df = pd.concat(cs)
    else:
        print("Sorry, no potential candidates with your given parameters :(")
        df = []
    print("************  ENDING FIND_EVENT PIPELINE   **************")
    return df

def outputs(saving, check_zero_drift, name, id_num, filter_threshold, SNR_cut, find_event_output_dataframe):
    """
    OUTPUTS: Returns an updated find_event_output_dataframe.
    Updates the find_event_output_dataframe.
    """

    if saving == True:
        if check_zero_drift == True:
            f_string = name + "_" + id_num + "_f" + str(filter_threshold) + "_snr" + str(SNR_cut) + "_zero" + ".csv"
        else:
            f_string = name + "_" + id_num + "_f" + str(filter_threshold) + "_snr" + str(SNR_cut) + ".csv"

        if not isinstance(find_event_output_dataframe, list):
            find_event_output_dataframe.to_csv(f_string)
        else:
            print("Sorry, no event to save :(")
    return find_event_output_dataframe
