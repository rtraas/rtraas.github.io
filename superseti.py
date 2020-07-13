import os
import glob

files = glob.glob("*.0000.h5")
for fi in files:
    print(fi)
    try:
        os.system("turboSETI -M 4 -s 10 " +str(fi))
    except:
        continue
