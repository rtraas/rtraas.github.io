#!/usr/bin/env python3
"""
Cadence building and file acquisition module.

The core module used in `auto_find_event_pipeline.py` and `autoplot.py` because it forgoes the need to
    1. Manually create lists of `.dat` and `{.fil, .h5}` files in order to run `find_event_pipeline.py` and `plot_event_pipeline.py`
    2. Manually position the files in the appropriate order in the cadence

Contains "filter functions" which support the "main functions" (i.e., the most useful ones).


Filter Functions are based on the file name conventions presented in the Breakthrough Listen Data Format Paper found with this link:
https://arxiv.org/pdf/1906.07391.pdf#page=28&zoom=100,49,228

File name convention:   blc<Node #>_guppi_<MJD Day>_<MJD Seconds>_<Target>_<Scan #>.gpuspec.<Resolution Type>.{fil, h5}


Author: Raffy Traas     raffytraas14@gmail.com
Last Modified: 07/23/2020
"""



import os
from collections import namedtuple

#####   Filter Functions    #####

# Stores file name in sections for quicker accessibility of components
FileInfo = namedtuple('FileInfo', ['Name_of_File', 'MJD_value', 'TObs_value', 'SeqObs_value'])

def find_TObs(singleFile):
    """For a given file, returns the Time of Observation (TObs) using MJD Seconds from the filename"""
    return int(singleFile.split('_')[-3])

def find_SeqObs(singleFile):
    """For a given file, returns the Sequence # of Observation (SeqObs) from the filename"""
    return int(singleFile.split('_')[-1].split('.')[0])

def find_MJDObs(singleFile):
    """For a given file, returns the Modified Julian Date of Observation (MJDObs) from the filename"""
    return int(singleFile.split('_')[-4])

def _bySeqObs(input_FileInfo):
    return input_FileInfo.SeqObs_value

def TripleFilter(matched_filelist, unmatched_filelist, name_of_input_file):
    """Uses """
    quadruplets = [FileInfo(filename, find_MJDObs(filename), find_TObs(filename), find_SeqObs(filename)) for filename in unmatched_filelist]
    name_matched_quadruplets = sorted([N for N in quadruplets if name_of_input_file in N.Name_of_File], key=_bySeqObs)

    lower_bound = name_matched_quadruplets[0]
    upper_bound = name_matched_quadruplets[-1]
    
    filtered_quadruplets = [N for N in quadruplets if (N.MJD_value == lower_bound.MJD_value) and (N.TObs_value in range(lower_bound.TObs_value, lower_bound.TObs_value + 1800 + 1)) and (N.SeqObs_value in range(lower_bound.SeqObs_value, upper_bound.SeqObs_value + 2))]
    sorted_quadruplets = sorted(filtered_quadruplets, key=_bySeqObs)

    return sorted_quadruplets



#####   Main Functions  #####

def FindFile(filename, ext_swap=None, if_none_create=False):
    """
    Locates the file
    """
    if ext_swap is not None:
        if "." in ext_swap:
            FindFile(filename.replace(filename.split('.')[-1], ext_swap))
        else:
            FindFile(filename.replace('.'+filename.split('.')[-1], ext_swap))
    else:
        for root, dirs, files in os.walk('/'+os.path.abspath(os.getcwd()).split('/')[1]):
            for file in files:
                if file == filename:
                    return os.path.join(root, file)
        if if_none_create:
            if (filename.split('.')[-1] == 'h5') and (ext_swap.split('.')[-1] == 'fil'):
                os.system('h52fil '+filename)
                return FindFile(filename)
            elif (filename.split('.')[-1] == 'fil') and (ext_swap.split('.')[-1] == 'h5'):
                os.system('fil2h5 '+filename)
                return FindFile(filename)
            else:
                print('%s does not exist' % (filename))
        raise FileNotFoundError

def Find(filepath, display=False):
    try:
        File = FindFile(filepath)
    except:
        raise FileNotFoundError("Unable to find file %s" % (filepath))

    try:
        extension = File.split('.')[-1]
    except:
        raise IOError("Error before getting extension")

    try:
        Name = filepath.split('_')[-2]
    except:
        raise IOError('Error in extracting name from input file %s' % (filepath))
    try:
        File_directory = '/'.join(File.split('/')[:-1])+'/'

    except:
        raise
    if not os.path.isdir(File_directory):
        raise IOError("%s does not exist" % (File_directory))

    File_directory_list = [filename for filename in os.listdir(File_directory) if (str(".0000."+extension) in filename)]#
    if not File_directory_list:
        raise Exception("File_directory_list is empty")

    try:
        matched = [filename for filename in File_directory_list if Name in filename]
        if matched:
            pass
        else:
            raise Exception("No files with a matched target name :( ")
    except:
        raise Exception("No files with a matched target name :( ")
    
    try:
        indices = [File_directory_list.index(filename) for filename in matched]
    except:
        raise Exception("Matched files exist, but error when obtaining indices")
    
    try:
        separation_gaps = [(indices[i+1]-indices[i])-1 for i in range(len(indices)-1)]
    except:
        raise Exception("Error obtaining separation_gaps.  Might be an error with indexing")

    ordered_quadruplets = TripleFilter(matched, File_directory_list, Name)
    cadence_filenames = [i for i in [n.Name_of_File for n in ordered_quadruplets]]
    cadence_files = [FindFile(r) for r in cadence_filenames]
    
    if display:
        print("\n<^><^><^><^><^><^><^> Cadence for %s <^><^><^><^><^><^><^><^><^>\n" % (Name))
        for c in cadence_files:
            print(c)
        print("\n<^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^>\n")
    
    return cadence_files


def to_list(directory, resolution_type='0', file_type=".h5"):
    """
    resolution type:
        0   high spectral resolution
        1   high time resolution
        8   8-bit integer high time resolution
        2   medium spectral/time resolution

    file type:
        h5  HDF5 format
        fil filterbank format

    types from Breakthrough Listen Data Format Paper
    https://arxiv.org/pdf/1906.07391.pdf#page=28&zoom=100,49,228
    """
    
    resolutions = {'0':'0000', '1':'0000', '8':'8.00001', '2':'00002'}
    files_typings = ['.h5', '.fil']

    if resolution_type not in resolutions.keys():
        raise KeyError("resolution_type must be either '0' (default), '1', '8', or '2'")
    else:
        rtype = resolutions[resolution_type]

    if file_type not in files_typings:
        raise KeyError("file_type must be either 'h5' (default) or 'fil'")
    else:
        ftype = file_type
    
    filelist = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if str(rtype+ftype) in file:
                filelist.append(os.path.join(root,file))

    return filelist


def Seek(target_directory):
    for root, dirs, files in os.walk('/'+os.path.abspath(os.getcwd()).split('/')[1]):
        for dir in dirs:
            if dir == list(filter(None, target_directory.split('/')))[0]:
                return os.path.join(root, dir)

            
def FindCadence(target_name, extension=None):
    """Finds path to target_name file (please specify the entire the filename (not the path)), 
       makes a list of all files within subdirectory containing target_name file,
       searches for files containing the target_name as a substring and saves their indices from within the list,
       checks all saved indices are 1-space apart from neighboring files of interest,
       returns a list of filenames (given as absolute paths) within the range of the smallest index to the largest index + 1.
    """
    
    target_file = FindFile(target_name)
    file_extension = target_file.split('.')[-1]
    
    if extension==None:
        # finding path to target_name file
        name = target_name.split('_')[-2]
        
       
        print("************* Finding Cadence for " + name + " *************")
        
        # make list of all files within subdirectory where target_file lives
        target_directory = '/'.join(target_file.split('/')[:-1])+'/'
    
        target_directory_list = [filename for filename in os.listdir(target_directory) if (str(".0000."+file_extension) in filename)]
        matched = [filename for filename in target_directory_list if name in filename]
        
        # find index of all files with the same target_name (this does not mean same file!)
        indices = [target_directory_list.index(filename) for filename in matched]

        # check if indices have separation distance of 1 between their closest neighboring target of interest
        separation_gaps = [(indices[i+1]-indices[i])-1 for i in range(len(indices)-1)]

        lower_index = indices[0]
        highest_index = indices[-1]

        if len(set(separation_gaps)) == 1:
            # returning list of filenames with index between range of the smallest index and the largest index + 1
            # highest_index + 2 is used because of Python's zero-indexing
            cadence = [FindFile(target_directory_list[i]) for i in range(lower_index, highest_index + 2)]

            return cadence
        else:
            print("check separation_gaps")
    
    else:
        base_cadence = FindCadence(target_name, extension=file_extension)
        swapped_extensions = [filename.split('/')[-1].replace(filename.split('.')[-1], extension.split('.')[-1]) for filename in base_cadence]
        swapped_extension_cadence = [FindFile(filename) for filename in swapped_extensions]
        print(swapped_extension_cadence)
        return swapped_extension_cadence


def FindDatCadence(filepath):

    extension = filepath.split('.')[-1]
    swapped_path = filepath.replace(extension, "h5")

    swapped_cadence = FindCadence(swapped_path)

    swapped_dat = [filename.split('/')[-1].replace(filename.split('.')[-1], extension) for filename in swapped_cadence]
    print(swapped_dat)
    dat_cadence = [FindFile(filename) for filename in swapped_dat]
    return dat_cadence




