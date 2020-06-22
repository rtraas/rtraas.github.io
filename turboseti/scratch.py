dat_file_list_str = 'HIP39826.lst'
dat_file_list = open(dat_file_list_str).readlines()
dat_file_list = [files.replace('\n','') for files in dat_file_list]
dat_file_list = [files.replace(',','') for files in dat_file_list]
print('dat_file_list = ', dat_file_list)
print("length of dat_file_list", len(dat_file_list))
def all_split():
    for n in range(len(dat_file_list)):
        sp = dat_file_list[n].split('_')
        print(sp)

all_split()

def split():
    source_name_list = []
    for dat in dat_file_list:
        source_name = dat.split('_')[5]
        source_name_list.append(source_name)

n_files = 6
number_in_cadence = 6
complex_cadence = False
on_off_first = 'ON'

for i in range((int(n_files/number_in_cadence))):
    file_sublist = dat_file_list[number_in_cadence*i:((i*number_in_cadence)+(number_in_cadence))]

def name():
    if complex_cadence == False:
        if on_off_first == 'ON':
            # if we want 5 use 5 (USE ONLY IF YOU'RE USING SPLICED FILES)
            #if dat.split('_')[0] == 'spliced':
                #source_name = dat.split('_')[5]
            # if we want 3 use 3 (because we're not using "spliced files")
            if file_sublist[0].split('_')[0] == 'spliced':
                name = file_sublist[0].split('_')[5]
                id_num = (file_sublist[0].split('_')[6]).split('.')[0]
            else:
                name = file_sublist[0].split('_')[3]
                id_num = (file_sublist[0].split('_')[4]).split('.')[0]
        # No support for spliced/non-spliced option select
        if on_off_first == 'OFF':
            name = file_sublist[1].split('_')[5]
            id_num = (file_sublist[1].split('_')[6]).split('.')[0]

print("file_sublist = ", file_sublist)

nm = file_sublist[0].split('_')[3]
ID = (file_sublist[0].split('_')[4]).split('.')[0]
print(nm)
print(ID)
