import matplotlib.pyplot as plt
import pandas as pd
import fileio
from mpl_toolkits import mplot3d


def getdf(home='/tess_container', ftype='.csv'):
    big = pd.concat([pd.read_csv(f) for f in fileio.look(ftype, home='/tess_container') if ftype in f], ignore_index=True, sort=False)
    return big
def freq_snr(dataframe, saved_as):
    plt.figure(figsize=(20,10))
    plt.scatter(dataframe.Freq, dataframe.SNR, s=10, c=dataframe.DriftRate, cmap='viridis')
    plt.xlabel('Frequency', fontsize=15)
    plt.ylabel('SNR', fontsize=15)
    plt.title('Frequency by SNR')
    bar=plt.colorbar()
    bar.set_label('DriftRate')
    plt.savefig(saved_as)
    return

def plot3d(a1,a2,a3,save, rfi=False, dotsize=10, logscale=True):
    ax = plt.axes(projection='3d')
    ax.scatter3D(a1,a2,a3,c=a3, cmap='viridis')
    plt.savefig(save)
    return


def plot(arg1, arg2, arg3, saved_as, rfi=False, home='/tess_container', size=(20,10), dotsize=10, color='viridis', ftype='.csv',logscale=True,d3=False):

    dataframe = getdf(ftype=ftype)
    if d3:
        return plot3d(dataframe[arg1],dataframe[arg2],dataframe[arg3],saved_as, rfi=rfi,dotsize=dotsize,logscale=logscale)
    plt.figure(figsize=size)
    if rfi:
        if arg1 != "Freq":
            raise Exception("'rfi' option can only be used if x='Freq'")
        else:
            rfi_df = pd.read_csv('rfspec_allocation_bands.csv')
            start = rfi_df['BandStart(MHZ)']
            stop = rfi_df['BandEnd(MHZ)']
            for i in range(len(start)):
                if (start[i] in range(round(dataframe[arg1].min()), round(dataframe[arg1].max()))) and (stop[i] in range(round(dataframe[arg1].min()), round(dataframe[arg1].max()))):
                    plt.axvspan(start[i], stop[i], alpha=0.25, facecolor='r', zorder=3)
                else:
                    continue

    plt.scatter(dataframe[arg1], dataframe[arg2], s=dotsize, c=dataframe[arg3], cmap=color)
    plt.xlabel(arg1, fontsize=15)
    plt.ylabel(arg2, fontsize=15)
    if logscale:
        plt.yscale('log')
    plt.xlim((round(dataframe[arg1].min()),round(dataframe[arg1].max())))
    plt.title('%s by %s'%(arg1, arg2))
    bar=plt.colorbar()
    bar.set_label(arg3)

    plt.savefig(saved_as)
    return


