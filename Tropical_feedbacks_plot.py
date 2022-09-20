"""
This script reads and plots tropical internal varaibility feedbacks (20°S-20°N) from simulations and observations. 
It includes the 5-95% confidence interval on the feedbacks.
@author: Alejandro UC
"""
#-----------------------------------------------------------------------------
## Libraries
#-----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import glob
#-----------------------------------------------------------------------------
## Input, output paths and initial settings
#-----------------------------------------------------------------------------
input='/home/alejandro/CL_feedbacks/data/'
input_data='/home/alejandro/CL_feedbacks/data_prod/'
#for Ty_sky in ('all',):#'cs','cre'):
Ty_sky='all'
fig, ax = plt.subplots(1,1, figsize=(8,4), sharey=True, sharex=True)
DATA = np.load(input_data+'CI_Feed_20_to_20_'+Ty_sky+'_Had5_V2.npz')
#-----------------------------------------------------------------------------
## Reading observed feedbacks
#-----------------------------------------------------------------------------
exps=[]
names=''
feed_lw=DATA['feed_lw']
top_lw_IC=DATA['top_lw_IC']
bot_lw_IC=DATA['bot_lw_IC']
feed_sw=DATA['feed_sw']
top_sw_IC=DATA['top_sw_IC']
bot_sw_IC=DATA['bot_sw_IC']
#-----------------------------------------------------------------------------
## Plotting 5-95% confidence interval on observed feedback
#-----------------------------------------------------------------------------
rect1 = matplotlib.patches.Rectangle((bot_sw_IC,bot_lw_IC), top_sw_IC, top_lw_IC-bot_lw_IC, color='black', alpha=0.25, label='Observations')
ax.add_patch(rect1)
#-----------------------------------------------------------------------------
## Looping along simulaton sets
#-----------------------------------------------------------------------------
for experiment,name in zip(('CMIP6_historical','AMIP'),('CMIP','AMIP')):
    names=names+name
    exps.append(experiment)
    #-----------------------------------------------------------------------------
    ## Looping along models
    #-----------------------------------------------------------------------------
    for exp in exps:
        models=[]
        #-----------------------------------------------------------------------------
        ## Retrieving model names
        #-----------------------------------------------------------------------------
        for i in glob.glob(input+exp+'/*'):
            models.append(i.replace('/home/alejandro/CL_feedbacks/data/'+exp+'/',''))
        if exp=='CMIP6_historical':
            c='blue'
        elif exp=='AMIP':
            c='red'
        mean_mod_lw=[];mean_mod_sw=[]
        #-----------------------------------------------------------------------------
        ## Loading model feedbacks
        #-----------------------------------------------------------------------------
        for k,mod in enumerate(models):
            DATA = np.load(input_data+'CI_Feed_20_to_20_'+Ty_sky+'_Had5_V2.npz')
            m_lw=DATA[exp+'_'+mod+'_m_lw']
            bot_lw_IC=DATA[exp+'_'+mod+'_lw_IC_min']
            top_lw_IC=DATA[exp+'_'+mod+'_lw_IC_max']
            m_sw=DATA[exp+'_'+mod+'_m_sw']
            bot_sw_IC=DATA[exp+'_'+mod+'_sw_IC_min']
            top_sw_IC=DATA[exp+'_'+mod+'_sw_IC_max']
            #-----------------------------------------------------------------------------
            ## Plotting model feedbacks
            #-----------------------------------------------------------------------------
            ax.scatter(m_sw,m_lw,color=c, s=4)
            #-----------------------------------------------------------------------------
            ## Plotting 5-95% confidence interval on model feedbacks
            #-----------------------------------------------------------------------------
            ax.plot([m_sw,m_sw],[bot_lw_IC,top_lw_IC],color=c, linewidth=0.5, label=name)
            ax.plot([bot_sw_IC,top_sw_IC],[m_lw,m_lw],color=c, linewidth=0.5)
#-----------------------------------------------------------------------------
## Setting plot parameters
#-----------------------------------------------------------------------------
ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.xaxis.set_ticks_position('top')
ax.set_xlabel('Shortwave feedback [Wm$^{-2}$ K$^{-1}$]')
ax.set_ylabel('Longwave feedback [Wm $^{-2}$ K$^{-1}$]')
ax.xaxis.set_label_position('top')
ax.xaxis.set_label_coords(0.84, 1.1)
ax.yaxis.set_label_coords(0.46, 0.35)
ax.set_ylim(-7,0)
ax.set_xlim(-7,7)
#-----------------------------------------------------------------------------
## Sorting legend
#-----------------------------------------------------------------------------
ax.legend(*[*zip(*{l:h for h,l in zip(*ax.get_legend_handles_labels())}.items())][::-1],loc='best',frameon=False)
fig.tight_layout()
#-----------------------------------------------------------------------------
## Saving figure as png
#-----------------------------------------------------------------------------
plt.savefig('/home/alejandro/CL_feedbacks/plots/paper/sin/20_20_feed_had5'+Ty_sky+'.png', dpi=300)
