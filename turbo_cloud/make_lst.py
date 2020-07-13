import glob
import os

if __name__=="__main__":

    F = [str(f + "\n") for f in glob.glob("*") if ".dat" in f]
    def SeqObs_sort(filename):
        """used with sorted() to sort list in numerical order of Sequence # of Observation"""
        return int(filename.split('_')[-1].split('.')[0])
    
    F = sorted(F,key=SeqObs_sort)

    target = os.getcwd().split('_')[-1]
    
    lst_file = open(str(str(target) + ".lst"),"w")
    lst_file.writelines(F)
