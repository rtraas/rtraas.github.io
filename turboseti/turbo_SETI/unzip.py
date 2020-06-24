import pandas as pd
import numpy as np
import time

def refactor_make_table(filename, init=False, to_save=False, debugging=False, to_debug=None):
    file = open(filename.strip())

    hits = file.readlines()

    all_hits = [hit.strip().split('\t') for hit in hits[9:]]

    FileID = hits[1].strip().split(':')[-1].strip()
    Source = hits[3].strip().split(':')[-1].strip()
    MJD = hits[4].strip().split('\t')[0].split(':')[-1].strip()
    RA = hits[4].strip().split('\t')[1].split(':')[-1].strip()
    DEC = hits[4].strip().split('\t')[2].split(':')[-1].strip()
    DELTAT = hits[5].strip().split('\t')[0].split(':')[-1].strip()   # s
    DELTAF = hits[5].strip().split('\t')[1].split(':')[-1].strip()   # Hz

    info = [FileID,Source,MJD,RA,DEC,DELTAT,DELTAF]

    def removal(hits):
        for h in hits:
            #if "File ID" in h:
            #    ind = hits.index(h)
            #    hits.pop(ind - 1)
            #    hits.pop(ind + 1)

            #if "DELTAT" in h:
            #    idx = hits.index(h)
            #    hits.pop(idx + 1)
            #    hits.pop(idx + 3)
            if '- o -' or '---' in h:
                hits.remove(h)
    def rem():
        for e in all_hits:
            if e[0] == ['# -------------------------- o --------------------------']:
                all_hits.remove(e)

    def eliminate(all_hits):
        for e in all_hits:
            if e[0][0] == '#':
                all_hits.remove(e)

        for e in all_hits:
            if '#' in e[0]:
                all_hits.remove(e)

        for i in all_hits:
            if i[0] == '# Source:HIP39826':
                all_hits.remove(i)
            if FileID in i[0]:
                all_hits.remove(i)
        for i in all_hits:
            if i[0] == '# Top_Hit_# ':
                all_hits.remove(i)

        for i in all_hits:
            for q in info:
                if q in i[0]:
                    all_hits.remove(i)

    eliminate(all_hits)


    def disp(all_hits, f=False):
        if f:
            for i in all_hits:
                print(i[0])
        else:
            for i in all_hits:
                print(i)

    #disp(all_hits, f=True)

    #disp(all_hits)

    def strip_blank(all_hits):
        for i in all_hits:
            for e in i:
                e = float(str(e).strip())

    #strip_blank(all_hits)

    #disp(all_hits)
    if debugging:
        print(str(FileID))
        print(Source)
        print(len(all_hits))
        disp(all_hits)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("\n\n\n")
    if debugging:
        if to_debug != None:
            try:
                counter = 0
                for i in all_hits:
                    print(i[to_debug])
                    counter += 1

            except IndexError:
                print("Iterated through " + str(counter) + " of " + str(len(all_hits)) + " entries before termination.")



    TopHitNum           = [i[0] for i in all_hits]
    DriftRate           = [i[1] for i in all_hits]
    SNR                 = [i[2] for i in all_hits]
    Freq                = [i[3] for i in all_hits]
    ChanIndx            = [i[5] for i in all_hits]
    FreqStart           = [i[6] for i in all_hits]
    FreqEnd             = [i[7] for i in all_hits]
    CoarseChanNum       = [i[10] for i in all_hits]
    FullNumHitsInRange  = [i[11] for i in all_hits]

    data = {'TopHitNum':TopHitNum,
            'DriftRate':DriftRate,
            'SNR':SNR,
            'Freq':Freq,
            'ChanIndx':ChanIndx,
            'FreqStart':FreqStart,
            'FreqEnd':FreqEnd,
            'CoarseChanNum':CoarseChanNum,
            'FullNumHitsInRange':FullNumHitsInRange
            }


    df_data = pd.DataFrame(data)
    df_data = df_data.apply(pd.to_numeric)

    # Adding columns from before
    df_data['FileID']   = FileID
    df_data['Source']   = Source.upper()
    df_data['MJD']      = MJD
    df_data['RA']       = RA
    df_data['DEC']      = DEC
    df_data['DELTAT']   = DELTAT
    df_data['DELTAF']   = DELTAF

    #Adding extra columns that will be filled out by this program
    df_data['Hit_ID'] = ''
    df_data['status'] = ''
    df_data['in_n_ons'] = ''
    df_data['RFI_in_range'] = ''

    print(type(df_data['status']))

    if to_save:
        df_data.to_pickle(str("./"+str(FileID[:-3])+".pkl"))
    print(df_data)
    return df_data
