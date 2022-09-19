"""
This script reads and plots tropical extreme precipitation for several experiments. 
The code creates an exponential x.scale taht allows a better visualitation of the data.
@author: Alejandro UC
"""
#-----------------------------------------------------------------------------
## Libraries
#-----------------------------------------------------------------------------
import matplotlib 
matplotlib.use('Agg')
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import os
import os.path
import sys
import pylab as pl
import scipy.constants
from matplotlib.ticker import NullFormatter
from scipy.stats.stats import pearsonr
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedFormatter, FixedLocator, LinearLocator, FormatStrFormatter
#-----------------------------------------------------------------------------
## Function to create the exponential x-scale
#-----------------------------------------------------------------------------
class CloseToOne(mscale.ScaleBase):
    name = 'close_to_one'
    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        self.nines = kwargs.get('nines', 5)
    def get_transform(self):
        return self.Transform(self.nines)
    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(FixedLocator(
                np.array([100-10**(-k) for k in range(100+self.nines)])))
        axis.set_major_formatter(FixedFormatter(
                [str(100-10**(-k)) for k in range(100+self.nines)]))
    def limit_range_for_scale(self, vmin, vmax, minpos):
        return vmin, min(100 - 10**(-self.nines), vmax)
    class Transform(mtransforms.Transform):
        input_dims = 100
        output_dims = 100
        is_separable = True
        def __init__(self, nines):
            mtransforms.Transform.__init__(self)
            self.nines = nines
        def transform_non_affine(self, a):
            masked = ma.masked_where(a > 100-10**(-100-self.nines), a)
            if masked.mask.any():
                return -ma.log10(100-a)
            else:
                return -np.log10(100-a)
        def inverted(self):
            return CloseToOne.InvertedTransform(self.nines)
    class InvertedTransform(mtransforms.Transform):
        input_dims = 100
        output_dims = 100
        is_separable = True
        def __init__(self, nines):
            mtransforms.Transform.__init__(self)
            self.nines = nines
        def transform_non_affine(self, a):
            return 100. - 10**(-a)
        def inverted(self):
            return CloseToOne.Transform(self.nines)
mscale.register_scale(CloseToOne)
#-----------------------------------------------------------------------------
## Input, output paths
#-----------------------------------------------------------------------------
input='/DATA/'
experiments=[['APE_r2b4NOCV','APE_r2b5NOCV','APE_r2b6NOCV','APE_r2b8NOCV'],
            ['APE_r2b4CV','APE_r2b5CV','APE_r2b6CV']]
fig, axs = plt.subplots(1,2, figsize=(10,5), sharey=True)  #plt.subplots(1,1, figsize=(10,4))
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
plt.ylabel('Fractional change [$\%K^{-1}$]', labelpad=35)
plt.xlabel('Percentile', labelpad=10)
#-----------------------------------------------------------------------------
## Figure settings
#-----------------------------------------------------------------------------
tit=['R2B4','R2B5','R2B6','R2B8',]
color=['black','blue','red','orange']
tit=['R2B4','R2B5','R2B6','R2B8']
loc=np.array([ 1,  2,  3,  4])
label='CTL'
label4k='4k'
color=['black','blue','red','orange','black','blue','red']
#-----------------------------------------------------------------------------
## Looping along simulatons
#-----------------------------------------------------------------------------
for ax,exps in zip(axs.ravel(),experiments):
    #-----------------------------------------------------------------------------
    ## Initializing Clausius-Clapeyron (CC) data set
    #-----------------------------------------------------------------------------
    CCS=[]
    for exp,t,c in zip(exps,loc,color): 
        data = np.load(input+'perpr_'+exp+'.npz')
        CC=data['CC_trop']
        CCS.append(CC)
        ax1 = ax.twiny()
        if ax==axs[1]:
            t=t+0.5
        ax1.scatter(t,CC,color=c)
        ax1.set_xlim(0,5)
        ax1.spines["right"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.set_xticks([])
    #-----------------------------------------------------------------------------
    ## plotting CC mean
    #-----------------------------------------------------------------------------
    ax1.hlines(y=np.mean(CCS),xmin=0,xmax=5,linestyle='--',color='black',label='Mean CC')
    if ax==axs[0]:
        ax1.legend(frameon=False, loc=1)
fig.tight_layout()
per=np.arange(99, 100, 0.001)
#-----------------------------------------------------------------------------
## Looping along simulatons
#-----------------------------------------------------------------------------
for ax,exps in zip(axs.ravel(),experiments):
    #-----------------------------------------------------------------------------
    ## Defining simulation colors
    #-----------------------------------------------------------------------------
    ax.set_prop_cycle(color=['black','blue','red','orange','green'])
    for exp,l in zip(exps,tit):
        #-----------------------------------------------------------------------------
        ## Reading data
        #-----------------------------------------------------------------------------
        data = np.load(input+'perpr_'+exp+'.npz')
        rapr=(data['perpr4']-data['perpr'])/data['perpr']*100/4
        #-----------------------------------------------------------------------------
        ## Plotting EP
        #-----------------------------------------------------------------------------
        ax.plot(per,rapr,label=str(l))
        ax.set_xticks([99, 99.9, 99.99])
        ax.set_xlim(99.9,99.99)
        ax.set_ylim(0,27)
        #-----------------------------------------------------------------------------
        ## Selecting exponential x-scale
        #-----------------------------------------------------------------------------
        ax.set_xscale('close_to_one',nines=2)
        ax.xaxis.set_minor_locator(ticker.LinearLocator(50))
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
axs[0].legend(frameon=False, loc=2)
axs[0].set_title('Explicit convection')
axs[1].set_title('Parametrized convection')
fig.tight_layout()
#-----------------------------------------------------------------------------
## Saving figure as pdf
#-----------------------------------------------------------------------------
plt.savefig('SEP.pdf', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format='pdf', transparent=False,bbox_inches=None, pad_inches=0.1, frameon=None)      