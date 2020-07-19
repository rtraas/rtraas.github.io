import os
#import logging
from collections import namedtuple
import glob


FileInfo = namedtuple('FileInfo', ['Name_of_File', 'MJD_value', 'TObs_value', 'SeqObs_value'])

def find_TObs(singleFile):
    return int(singleFile.split('_')[-3])

def find_SeqObs(singleFile):
    return int(singleFile.split('_')[-1].split('.')[0])

def find_MJDObs(singleFile):
    return int(singleFile.split('_')[-4])

def SeqObs_sort(FileName):
    """used with sorted() to sort list in numerical order of Sequence # of Observation"""
    return int(filename.split('_')[-1].split('.')[0])

def SeqObs_filter(matched_filelist, unmatched_filelist):
    """use in list comprehension to filter out files with irrelevant Sequence #'s of Observation"""
    pass

def _bySeqObs(input_FileInfo):
    return input_FileInfo.SeqObs_value

def TObs_filter(matched_filelist, unmatched_filelist):
    pass

def TripleFilter(matched_filelist, unmatched_filelist, name_of_input_file):
    #TObs_values = [find_TObs(element) for element in matched_filelist]
    #TObs_min = TObs_values[0]
    #TObs_max = TObs_min + 1800          #1800 seconds = 30 minutes = Maximum duration of a cadence

    #SeqObs_values = [find_TObs
    
    quadruplets = [FileInfo(filename, find_MJDObs(filename), find_TObs(filename), find_SeqObs(filename)) for filename in unmatched_filelist]

    #name_matched_quadruplets_indices = sorted([N for N in quadruplets if name_of_input_file in N.Name_of_File])
    #print("quadruplets \n")
    #for quad in quadruplets:
    #    print(quad)
    name_matched_quadruplets = sorted([N for N in quadruplets if name_of_input_file in N.Name_of_File], key=_bySeqObs)
    #print("name_matched_quadruplets")
    #for nm in name_matched_quadruplets:
    #    print(nm)
    #Quadruplets = [quadruplets[i] for i in 
    lower_bound = name_matched_quadruplets[0]
    upper_bound = name_matched_quadruplets[-1]
    #mjd_matched = [N for N in quadruplets if N.MJD_value == lower_bound.MJD_value]
    #print("mjd_matched")
    #for m in mjd_matched:
    #    print(m)
    #print("bounds", lower_bound, upper_bound)
    
    #t_match = [N for N in quadruplets if N.TObs_value in range(lower_bound.TObs_value, lower_bound

    filtered_quadruplets = [N for N in quadruplets if (N.MJD_value == lower_bound.MJD_value) and (N.TObs_value in range(lower_bound.TObs_value, lower_bound.TObs_value + 1800 + 1)) and (N.SeqObs_value in range(lower_bound.SeqObs_value, upper_bound.SeqObs_value + 2))]
    #print("filtered_quadruplets")
    #for f in filtered_quadruplets:
    #    print(f)

    sorted_quadruplets = sorted(filtered_quadruplets, key=_bySeqObs)
    #print("sorted quadruplets \n")
    #for quad in sorted_quadruplets:
    #    print(quad)
    #print("Anything past here is not a print statement made within TripleFilter()")
    return sorted_quadruplets

def testtriple(filelist):
    triplets = [FileInfo(find_MJDObs(filename), find_TObs(filename), find_SeqObs(filename)) for filename in filelist]


    filtered_unmatched_filelist = [element for element in unmatched_filelist if find_TObs(element) in range(TObs_min, TObs_max + 1)]    #+1 because of Python's zero-indexing
    filtered_unmatched_filelist = sorted(filtered_unmatched_filelist, key=find_TObs)

def triple(filepath):
    try:
        File = FindFile(filepath)
        #logging.info()
        print("Found file %s : %s" % (filepath, File))
    except:
        print("Unable to find file %s" % (filepath))
        raise FileNotFoundError
    try:
        extension = File.split('.')[-1]
    except:
        print("Error before getting extension")
        raise IOError
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
            print("Files with a matching target name exist! ", matched)
        else:
            raise Exception("No files with a matched target name :( ")
    except:
        raise Exception("No files with a matched target name :( ")
    TripleFilter(matched, File_directory_list)


def FindFile(filename, ext_swap=None, if_none_create=False):
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
        #logging.info()
        #print("Found file %s : %s" % (filepath, File))
    except:
        #print("Unable to find file %s" % (filepath))
        raise FileNotFoundError
    try:
        extension = File.split('.')[-1]
    except:
        #print("Error before getting extension")
        raise IOError
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
            pass#print("Files with a matching target name exist! ", matched)
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
        #print("separation_gaps ", separation_gaps)
    except:
        raise Exception("Error obtaining separation_gaps.  Might be an error with indexing")
    
    #try:
    #    lower_index = indices[0]
    #    highest_index = indices[-1]
        
    #    print("low index ", lower_index)
    #    print("high index ", highest_index)
    #except:
    #    raise IndexError("There was an error with obtaining indices")

    #if len(set(separation_gaps)) == 1:
        
        
        # returning list of filenames with index between range of the smallest index and the largest index + 1
        # highest_index + 2 is used because of Python's zero-indexing
     #   cadence = [FindFile(target_directory_list[i]) for i in range(lower_index, highest_index + 2)]
        
        # for debugging
            #print(cadence)
     #   return cadence
    #else:

        #########################################################################################################
        ### This is where the TObs_sort, SeqObs_sort, and MJDObs_sort will be used to find the cadence if the ###
        ### separation between files with matching names is not 1                                             ###
        #########################################################################################################

        #example filename: spliced_blc5051525354555657_guppi_58892_35102_HIP53639_0025.rawspec.0000.dat

    ordered_quadruplets = TripleFilter(matched, File_directory_list, Name)
    #print("ordered_quadruplets")
    #for oq in ordered_quadruplets:
    #    print(oq)
        #matched_name_indices = [ordered_quadruplets.index(quad) for quad in ordered_quadruplets if Name in quad.Name_of_File]
        
        #cadence_filenames = [ordered_quadruplets[i] for i in matched_name_indices]
        #cadence_filenames = [ordered_quadruplets[i].Name_of_File for i in range(matched_name_indices[0], matched_name_indices[-1] + 2)]         # +2 because of Python's zero-indexing
    cadence_filenames = [i for i in [n.Name_of_File for n in ordered_quadruplets]]
    #print("cadence_filenames")
    #for cf in cadence_filenames:
     #   print(cf)


    cadence_files = [FindFile(r) for r in cadence_filenames]
    
    if display:
        print("\n<^><^><^><^><^><^><^> Cadence for %s <^><^><^><^><^><^><^><^><^>\n" % (Name))
        for c in cadence_files:
            print(c)
        print("\n<^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^><^>\n")
    
    return cadence_files

        #print("check separation_gaps")
        #raise FileNotFoundError("Check separation gaps")

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
    
    #print(rtype)
    #print(ftype)

    #print("%s/*%s%s" % (directory, rtype, ftype))

    #print(sorted(glob.glob("%s/*.%s.%s" % (directory, rtype, ftype)), key=os.path.getmtime))
    filelist = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if str(rtype+ftype) in file:
                filelist.append(os.path.join(root,file))
                #filelist.append(file)
    
    return filelist #, key=os.path.getmtime)
    #return sorted(glob.glob("%s/*.%s.%s" % (directory, rtype, ftype)), key=os.path.getmtime)
    #key=getctimei


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
        #target_file = FindFile(target_name)
        #file_extension = target_file.split('.')[-1]
        name = target_name.split('_')[-2]
        print("************* Finding Cadence for " + name + " *************")
    # make list of all files within subdirectory where target_file lives
    # target_directory = target_file.split('/')[-2]
        target_directory = '/'.join(target_file.split('/')[:-1])+'/'
    #absfilepath = '/'.join(filepath.split('/')[:-1])+'/' 
    # debugging
    #print("target_directory ", target_directory)
        #print("name ", name)
        #print("first ", FindFile(os.listdir(target_directory)[0]))
        #print("matched names ", [filename for filename in os.listdir(target_directory) if (name in filename) and (str(".0000." + file_extension) in filename)])
    
    #print("path for first ", FindFile(os.listdir(target_directory)))

    #print("target_directory ", target_directory)
    #print("target_directory[0] ", target_directory[0])
    #print("paths for some ", FindFile(target_directory[0]))
    
    #print("os.listdir(target_directory) ", os.listdir(target_directory))

    #abspathslist = [os.path.abspath(filename) for filename in os.listdir(target_directory)]
    

    #print("abspaths for os.listdir(target_directory ", abspathslist)

    #found = [FindFile(filename) for filename in os.listdir(target_directory)]
    #print("FindFile(filename) for filename ", found)
    
    #target_directory_list = [os.path.abspath(filename) for filename in os.listdir(target_directory) if os.path.isfile(filename)]
    #target_directory_list = [os.path.abspath(filename) for filename in os.listdir(target_directory) if ".0000.h5" in filename]
    #target_directory_list = [filename for filename in target_directory_list if name in filename]
    #target_directory_list = [filename for filename in os.listdir(target_directory) if ".0000.h5" in filename]
    #I = [target_directory_list.index(filename) for filename in target_directory_list if name in filename]
    #print("I ", I)
        target_directory_list = [filename for filename in os.listdir(target_directory) if (str(".0000."+file_extension) in filename)]# and (name in filename)]
    #print("dirs ", )
        matched = [filename for filename in target_directory_list if name in filename]
    # debugging
        #print("target_directory_list ", target_directory_list)
        indices = [target_directory_list.index(filename) for filename in matched]
        #print("indices ", indices)
    # find index of all files with the same target_name (this does not mean same file!)
    #indices = [target_directory_list.index(filename) for filename in target_directory_list if target_name in filename]

    # check if indices have separation distance of 1 between their closest neighboring target of interest
        separation_gaps = [(indices[i+1]-indices[i])-1 for i in range(len(indices)-1)]
        #print("sep gaps ", separation_gaps)
        lower_index = indices[0]
        highest_index = indices[-1]

        if len(set(separation_gaps)) == 1:
        
        # returning list of filenames with index between range of the smallest index and the largest index + 1
        # highest_index + 2 is used because of Python's zero-indexing
            cadence = [FindFile(target_directory_list[i]) for i in range(lower_index, highest_index + 2)]
        
        # for debugging
            #print(cadence)
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

#def Find(filepath):
#    File





def uFindCadence(filepath, swap_ext=None):
    File = FindFile(filepath)
    extension = File.split('.')[-1]

    if extension == "h5":
        #File = FindFile(filepath)
        #extension = File.split('.')[-1]
        name = filepath.split('_')[-2]
        target_directory = '/'.join(filepath.split('/')[:-1])+'/'
        print(target_directory)
        target_directory_list = [filename for filename in os.listdir(target_directory) if (str(".0000."+extension) in filename) and (name in filename)]
        print(target_directory_list)
        matched = [filename for filename in target_directory_list if name in filename]
        print(matched)
        indices = [target_directory_list.index(filename) for filename in matched]
        print(indices)
        separation_gaps = [(indices[i+1]-indices[i])-1 for i in range(len(indices)-1)]
        lower_index = indices[0]
        highest_index = indices[-1]
        if len(set(separation_gaps)) == 1:
        
        # returning list of filenames with index between range of the smallest index and the largest index + 1
        # highest_index + 2 is used because of Python's zero-indexing
            cadence = [FindFile(target_directory_list[i]) for i in range(lower_index, highest_index + 2)]
        
        # for debugging
            
            swapped_extensions = [filename.split('/')[-1].replace(filename.split('.')[-1], extension.split('.')[-1]) for filename in cadence]
            swapped_extension_cadence = [FindFile(filename) for filename in swapped_extensions]

            return swapped_extension_cadence
        else:
            print("check separation_gaps")
            return
    else:
        return FindCadence(filepath, swap_ext="h5")




