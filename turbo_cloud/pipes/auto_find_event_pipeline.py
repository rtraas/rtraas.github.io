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
    Version 2.0 - Sofia Sheikh (ssheikhmsa@gmail.com) 
    Version 1.0 - Emilio Enriquez (jeenriquez@gmail.com)
    
Last updated: 07/14/2020

***
NOTE: This code works for .dat files that were produced by seti_event.py
after turboSETI version 0.8.2, and blimpy version 1.1.7 (~mid 2019). The 
drift rates *before* that version were recorded with the incorrect sign
and thus the drift rate sign would need to be flipped in the make_table 
function.
***

'''

#required packages and programs
#import find_event
import pandas as pd
#import refactor_find_event_pipeline
#import refactor_find_event

#for debugging
import Sofia_find_event

#required for find_event
import time
import numpy as np

#feature enhancement imports
import fileio



def find_event_pipeline(dat_file_list,
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
    dat_file_list_str = dat_file_list[0].split('/')[-1]
    if on_source_complex_cadence == False:
        print("Assuming the first observation is an " + on_off_first)
        complex_cadence=on_source_complex_cadence
    if on_source_complex_cadence != False:
        print("Assuming a complex cadence for the following on source: " + on_source_complex_cadence)
        
    #Opening list of files
    #dat_file_list = open(dat_file_list_str).readlines()
    #dat_file_list = [files.replace('\n','') for files in dat_file_list]
    #dat_file_list = [files.replace(',','') for files in dat_file_list]
    #dat_file_list = [fileio.FindFile(files) for files in dat_file_list]
    #dat_file_list = [str("../../outs_l_band/"+files) for files in dat_file_list]
    n_files = len(dat_file_list)
    name = ''
    #Getting source names
    #/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_01530_BLGCsurvey_Cband_B02_0019.gpuspec.0000.dat
    #/tess_container/outs_TIC154089169/spliced_blc4041424344454647_guppi_58844_30202_TIC154089169_0088.gpuspec.0000.dat
    source_name_list = []
    for dat in dat_file_list:
        #source_name = dat.split('Cband_')[1]
        #source_name=source_name.split('_')[0]
        #source_name = dat.split('/')[-1].split('_')[-2]
        source_name = dat.split('_')[-2]
        source_name_list.append(source_name)
        
    if on_source_complex_cadence != False:
        complex_cadence = []
        for i in range(0, len(source_name_list)):
            source = source_name_list[i]
            if source == on_source_complex_cadence:
                complex_cadence.append(1)
            else:
                complex_cadence.append(0)
        print("The derived cadence is: " + str(complex_cadence))
    
    print("There are " + str(len(dat_file_list)) + " total files in the filelist " + dat_file_list_str)
    print("therefore, looking for events in " + str(int(n_files/number_in_cadence)) + " on-off set(s)")
    print("with a minimum SNR of " + str(SNR_cut))
    
    if filter_threshold == 1:
        print("Present in an A source only, above SNR_cut")
    if filter_threshold == 2:
        print("Present in at least one A source with RFI rejection from the off-sources")
    if filter_threshold == 3:
        print("Present in all A sources with RFI rejection from the off-sources")
    
    if check_zero_drift == False:
        print("not including signals with zero drift")
    if check_zero_drift == True:
        print("including signals with zero drift")
    if saving == False:
        print("not saving the output files")
    if saving == True:
        print("saving the output files")    
    
    if user_validation == False:
        #question = "Do you wish to proceed with these settings?"
        #while "the answer is invalid":
            #reply = str(input(question+' (y/n): ')).lower().strip()
            #if reply == '':
            #    return
            #if reply[0] == 'y':
            #    break
            #if reply[0] == 'n':
            #    return
    
        #Looping over number_in_cadence chunks.
        candidate_list = []
        for i in range((int(n_files/number_in_cadence))):
            file_sublist = dat_file_list[number_in_cadence*i:((i*number_in_cadence)+(number_in_cadence))]
            if complex_cadence == False:
                if on_off_first == 'ON':
                    #name = file_sublist[0].split('Cband_')[1]
                    name = file_sublist[0].split('_')[-2]
                    name=name.split('_')[0]  
                    print ('name', name)
                    #id_num = (file_sublist[0].split('_')[6]).split('.')[0]
                    id_num = (file_sublist[0].split('_')[6])
                if on_off_first == 'OFF':
                    #name = file_sublist[1].split('Cband_')[1]
                    name = file_sublist[1].split('_')[-2]
                    name=name.split('_')[0] 
                    #id_num = (file_sublist[1].split('_')[6]).split('.')[0]
                    id_num = (file_sublist[1].split('_')[6]).split('.')[0]
            else:
                name = file_sublist[complex_cadence.index(1)].split('_')[5]  
                id_num = file_sublist[complex_cadence.index(1)].split('_')[6].split('.')[0]
                
            print()
            print("***       " + name + "       ***")
            print()
            cand = Sofia_find_event.find_events(file_sublist, 
                                          SNR_cut=SNR_cut, 
                                          check_zero_drift=check_zero_drift, 
                                          filter_threshold=filter_threshold, 
                                          on_off_first=on_off_first,
                                          complex_cadence=complex_cadence)
            cand_len = 1
            if cand is None:
                cand_len = 0
            if cand_len != 0:
                candidate_list.append(cand)
        if len(candidate_list) > 0:
            find_event_output_dataframe = pd.concat(candidate_list)
        else:
            "Sorry, no potential candidates with your given parameters :("
            find_event_output_dataframe = []
    
        print("************  ENDING FIND_EVENT PIPELINE   **************")
    
    if saving == True:
        if check_zero_drift == True:
            filestring = name + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '_zero' + '.csv'
        else:
            filestring = name + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '.csv'            
        if not isinstance(find_event_output_dataframe, list):
            find_event_output_dataframe.to_csv(filestring)
        else:
            print("Sorry, no events to save :(")

    return(find_event_output_dataframe)

#find_event_pipeline(2,20,'A00_C07_dat.lst',on_off_first='ON',number_in_sequence=3,saving=True,zero_drift_parameter=False,user_validation=False)
#find_event_pipeline('/datax/scratch/karenp/SETI_events/B02_B05_pair/B02_ON/B02_B05_dat.lst', SNR_cut=20, check_zero_drift=False, filter_threshold=2, on_off_first='ON', number_in_cadence=6, on_source_complex_cadence=False, saving=True, user_validation=False)
#find_event_pipeline('/tess_container/outs_TIC154089169/TIC154089169.lst', SNR_cut=10, check_zero_drift=False, filter_threshold=2, on_off_first='ON', number_in_cadence=6, on_source_complex_cadence=False, saving=True, user_validation=False)
#for reference
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_01530_BLGCsurvey_Cband_B02_0019.gpuspec.0000.dat
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_01840_BLGCsurvey_Cband_B05_0020.gpuspec.0000.dat
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_02149_BLGCsurvey_Cband_B02_0021.gpuspec.0000.dat
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_02459_BLGCsurvey_Cband_B05_0022.gpuspec.0000.dat
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_02768_BLGCsurvey_Cband_B02_0023.gpuspec.0000.dat
#/datax/scratch/karenp/SETI_events/SETI_eventsspliced_blc00010203040506o7o0111213141516o7o0212223242526o7o031323334353637_guppi_58705_03078_BLGCsurvey_Cband_B05_0024.gpuspec.0000.dat
#find_event_pipeline('../../TIC159510109.lst', SNR_cut=10, check_zero_drift=False, filter_threshold=2, on_off_first='ON', number_in_cadence=6, on_source_complex_cadence=False, saving=True, user_validation=False)
#find_event_pipeline('../../TIC159510109.lst', SNR_cut=10, check_zero_drift=False, filter_threshold=3, on_off_first='ON', number_in_cadence=6, on_source_complex_cadence=False, saving=True, user_validation=False)

import argparse
import sys
import glob
def cmd_utility(args=None):
    P = argparse.ArgumentParser(description="a command line utility for accessing turbo_seti's pipeline code")
    
    P.add_argument('-a', '--auto', action='store', default=False, dest='auto', type=bool, help='Automate running find_event_pipeline on multiple cadences.  To run on all available cadences, type "a" after "-a".')
    #P.add_argument('', '--
    P.add_argument('-f', '--dats_lst', action='store', default=None, dest='dat_file_list', type=str)
    #P.add_argument('-f', '--fils_lst', action='store', default=None, dest='fils_list', type=str)
    P.add_argument('-s', '--snr', action='store', default=10, dest='snr', type=int)
    P.add_argument('-z', '--check_zero', action='store', default=False, dest='check_zero_drift', type=bool)
    P.add_argument('-t', '--filter_threshold', action='store', default=3, dest='filter_threshold', type=int)
    P.add_argument('-b', '--on_off_first', action='store', default='ON', dest='on_off_first', type=str)
    P.add_argument('-n', '--number_in_cadence', action='store', default=6, dest='number_in_cadence', type=int)
    P.add_argument('-c', '--complex_cadence', action='store', default=False, dest='on_source_complex_cadence', type=bool)
    P.add_argument('-S', '--saving', action='store', default=True, dest='saving', type=bool)
    P.add_argument('-u', '--user_validation', action='store', default=False, dest='user_validation', type=bool)

    #if args is None:
    #    args = sys.argv[1:]
        
    #    if len(sys.argv)==1:
    #        print('Indicate event file path')
    #        sys.exit()
    args = P.parse_args(args)

    if args.auto is False:
        print('Need to use auto')
        sys.exit()
    if args.auto is not False:
        def Testfileio(filename):
            print("\n |><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><|\n")
            print("Checking %s" % (filename))
            return fileio.Find(filename)

        list_of_dat_files = glob.glob("../../**/*.dat")
        list_to_check = [filename.split('/')[-1] for filename in list_of_dat_files if ("Voyager" not in filename.split('/')[-1]) and ("HIP" not in filename.split('/')[-1])]
        
        all_cadences = []
        cadence_list = []
        not_analyzed = []

        for Filename in list_to_check:
            in_cadence=False
            for cadence in all_cadences:
                if Filename in cadence.split('/')[-1]:
                    in_cadence = True
            if in_cadence:
                cadence_to_add = fileio.Find(Filename)
                FilePath = [N for N in list_of_dat_files if Filename in N]
                FilePath = FilePath[0]
                FilePath = '/'.join(FilePath.split('/')[:-1])+'/'
                if len(cadence_to_add) == 6:
                    cadence_list.append([len(cadence_to_add), Filename, FilePath, cadence_to_add])
                    for individual in cadence_to_add:
                        all_cadences.append(individual)
                else:
                    not_analyzed.append([len(cadence_to_add), Filename, FilePath, cadence_to_add])
        
        for g in cadence_list:
            print(g)
                



#for filename in list_to_check:
    #print(filename)
    #    L = []
    #all_cadences = []
    #for Filename in list_to_check:
    #for FCG in all_cadences:
    #    print(FCG)
    #    in_all_cadences = 0
    #    for FC in all_cadences:
    #        if Filename in FC.split('/')[-1]:
    #            in_all_cadences += 1
    #    if in_all_cadences == 0:
    #        C = Testfileio(Filename)
    #        Fpath = [N for N in list_of_dat_files if Filename in N]
    #        Fpath = Fpath[0]
    #        Fpath = '/'.join(Fpath.split('/')[:-1])+'/'
    #        L.append([len(C), Filename, Fpath, C])
    #        for cfile in C:
    #            all_cadences.append(cfile)


    #print("\n\n\nLengths of cadences:\n")
    #for element in L:
    #    print("\nLength of Cadence: %s \t Filename: %s \t Path: %s" % (element[0], element[1], element[2]))
    #    if element[0] != 6:
    #        print("\n\t%sCadence" % (element[1].split('_')[-2]))
    #        #print(element[3])
    #        for element_file in element[3]:
    #            print("\t\t",element_file)
        #find_event_pipeline(args.dat_file_list, SNR_cut=args.snr, check_zero_drift=args.check_zero_drift, filter_threshold=args.filter_threshold, on_off_first=args.on_off_first, number_in_cadence=args.number_in_cadence, on_source_complex_cadence=args.on_source_complex_cadence, saving=args.saving, user_validation=args.user_validation)

#def automate(args=None):
    #auto = argparse.ArgumentParser(description="automated find_event_pipeli
#if __name__ == "__main__":
    #cmd_utility()

list_of_dat_files = glob.glob("../../**/*.dat")
list_to_check = [filename.split('/')[-1] for filename in list_of_dat_files if ("Voyager" not in filename.split('/')[-1]) and ("HIP" not in filename.split('/')[-1])]

all_cadences = []
cadence_list = []
not_analyzed = []
full_list = []
#print(list_to_check)
for Filename in list_to_check:
    in_cadence=True
    for cadence in all_cadences:
        if Filename in cadence.split('/')[-1]:
            in_cadence = False
    #print(in_cadence)
    if in_cadence:
        cadence_to_add = fileio.Find(Filename)
        FilePath = [N for N in list_of_dat_files if Filename in N]
        FilePath = FilePath[0]
        FilePath = '/'.join(FilePath.split('/')[:-1])+'/'
        #full_list.append(cadence_to_add)
        if len(cadence_to_add) == 6:
            cadence_list.append([len(cadence_to_add), Filename, FilePath, cadence_to_add, None])
            for individual in cadence_to_add:
                all_cadences.append(individual)
        else:
            not_analyzed.append([len(cadence_to_add), Filename, FilePath, cadence_to_add, None])

        
#for g in cadence_list:
    #print(g[3])
    #print(len(g[3]))
error_list = []
f3 = []
f2 = []
f1 = []
for na in cadence_list:
    print("\n\n<><><><><><><> %s Cadence <><><><><><><>\n" % (na[1]))
    for i in range(len(na[3])):
        print(na[3][i])
    try:
        DF1 = find_event_pipeline(na[3], filter_threshold=1)
        #if len(DF)=0:
        #    raise Exception
        #na[4]=3
        f1.append(na)
        if len(DF1)!=0:
            DF2=find_event_pipeline(na[3], filter_threshold=2)
                #if len(DF)==0:
                #    raise Exception
                #na[4]=2
            f2.append(na)
            if len(DF2)!=0:
                
                DF3=find_event_pipeline(na[3], filter_threshold=3)
                        #if len(DF)==0:
                        #raise Exception
                        #na[4]=2
                na[4]=3
                f3.append(na)
            else:
                na[4]=2
        else:
            if len(DF1)==0:
                raise Exception
            na[4]=1
            
    except:

        print("There was an error")
        error_list.append(na)

for na in not_analyzed:
    print("\n\n<><><><><><><> %s Cadence <><><><><><><>\n" % (na[1]))
    for i in range(len(na[3])):
        print(na[3][i])
    try:
        DF1 = find_event_pipeline(na[3], filter_threshold=1)
        #if len(DF)=0:
        #    raise Exception
        #na[4]=3
        f1.append(na)
        if len(DF1)!=0:
            DF2=find_event_pipeline(na[3], filter_threshold=2)
                #if len(DF)==0:
                #    raise Exception
                #na[4]=2
            f2.append(na)
            if len(DF2)!=0:
                
                DF3=find_event_pipeline(na[3], filter_threshold=3)
                        #if len(DF)==0:
                        #raise Exception
                        #na[4]=2
                na[4]=3
                f3.append(na)
            else:
                na[4]=2
        else:
            if len(DF1)==0:
                raise Exception
            na[4]=1
            
    except:

        print("There was an error")
        error_list.append(na)
    #except:
    #    try:
    #        DF=find_event_pipeline(na[3], filter_threshold=2)
    #        if len(DF)==0:
    #            raise Exception
    #        na[4]=2
    #        f2.append(na)
    #    except#:
          #  try#:
          #      DF = find_event_pipeline(na[3], filter_threshold=3)
          #      if len(DF)==0:
          #          raise Exception
          #      na[4]=1
          #      f1.append(na)
          #  except:
          #      print("There was an error")
          #      error_list.append(na)
       # continue


print("\n\n<><><><><><><><><><><><><><><><><><><><> Summary of Findings <><><><><><><><><><><><><><><><><><><><>")
print("\nFilter Threshold Level:\t 3")
for E in f3:
    print("\n\nCadence: %s \t Length of Cadence: %s \t Path: %s" % (E[1].split('_')[-2], E[0], E[2]))
print("\nFilter Threshold Level:\t 2")
for E in f2:
    print("\n\nCadence: %s \t Length of Cadence: %s \t Path: %s" % (E[1].split('_')[-2], E[0], E[2]))
print("\nFilter Threshold Level:\t 1")
for E in f1:
    print("\n\nCadence: %s \t Length of Cadence: %s \t Path: %s" % (E[1].split('_')[-2], E[0], E[2]))




if not error_list:
    print("\n\nThere were no errors!\n")
else:
    print("\n\n<><><><><><><><><><><><><><><><><><><><> LOGGED ERRORS <><><><><><><><><><><><><><><><><><><><>")
    for E in error_list:
        #if E[0] == 6:
        print("\n\nCadence: %s \t Length of Cadence: %s \t Path: %s" % (E[1].split('_')[-2], E[0], E[2]))
        for cad in E[3]:
            print("\t%s" % (cad))
        

