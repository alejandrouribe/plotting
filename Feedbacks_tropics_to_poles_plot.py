"""
This script reads and plots internal varaibility feedbacks from simulations and observations. 
It creates a x-scale porportional to the size of grid cells which decreases toward the poles.
@author: Alejandro UC
"""
#-----------------------------------------------------------------------------
## Libraries
#-----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import glob
import scipy.stats as st
#-----------------------------------------------------------------------------
## Input, output paths
#-----------------------------------------------------------------------------
input='/home/alejandro/CL_feedbacks/data/'
input_data='/home/alejandro/CL_feedbacks/data_prod/'
#-----------------------------------------------------------------------------
## Looping along flux type
#-----------------------------------------------------------------------------
for Ty_sky,tit in zip(('all','cs','cre'),('All-sky','Clear-sky', 'Cloud radiative effects')):
    #-----------------------------------------------------------------------------
    ##  Defining plot settings
    #-----------------------------------------------------------------------------
    for l,domain in enumerate(('Local','Global')):
        fig, ax = plt.subplots(1,2, figsize=(11,5.5), sharey=True, sharex=True)
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
        plt.ylabel('Feedback [Wm$^{-2}$ K$^{-1}$]', labelpad=35)
        plt.xlabel('Latitude [Degree]', labelpad=20)
        plt.title(tit)
        #-----------------------------------------------------------------------------
        ## Creating bins width for x-scale
        #-----------------------------------------------------------------------------
        intervals=['','10','20','30','40','50','60','70','80','90']
        interval=np.linspace(10,90,9)
        xscale=np.sin(np.deg2rad(interval))
        vlines=xscale[:-1]+np.diff(xscale,n=1)/2
        vlines=np.append(vlines,2*xscale[-1]-vlines[-1])
        vlines=np.append(2*xscale[0]-vlines[0],vlines)
        feed_lw=[];top_lw_IC=[];bot_lw_IC=[];feed_sw=[];top_sw_IC=[];bot_sw_IC=[]
        #-----------------------------------------------------------------------------
        ## Reading and averaging hemispherical data (Observations)
        #-----------------------------------------------------------------------------
        for H in ('North', 'South'):
            DATA = np.load(input_data+'CI_Feed_Ftropics_'+Ty_sky+'_NOSI_NOI_'+H+'_Had5_V2.npz')
            #-----------------------------------------------------------------------------
            ## Setting plot limits (empirically)
            #-----------------------------------------------------------------------------
            if domain=='Global':
                ax[0].set_ylim(-17,17)
            if domain=='Local':
                ax[0].set_ylim(-11,11)
            if domain=='Local' and  Ty_sky=='cs':
                ax[0].set_ylim(-10,10)
            if domain=='Local' and  Ty_sky=='cre':
                ax[0].set_ylim(-10,10)
            #-----------------------------------------------------------------------------
            ## Grouping data
            #-----------------------------------------------------------------------------
            feed_lw.append(DATA['feed_lw_'+domain])
            top_lw_IC.append(DATA['top_lw_IC_'+domain])
            bot_lw_IC.append(DATA['bot_lw_IC_'+domain])
            feed_sw.append(DATA['feed_sw_'+domain])
            top_sw_IC.append(DATA['top_sw_IC_'+domain])
            bot_sw_IC.append(DATA['bot_sw_IC_'+domain])
        #-----------------------------------------------------------------------------
        ## Computing means
        #-----------------------------------------------------------------------------   
        feed_lw=np.mean(feed_lw,axis=0)
        top_lw_IC=np.mean(top_lw_IC,axis=0)
        bot_lw_IC=np.mean(bot_lw_IC,axis=0)
        feed_sw=np.mean(feed_sw,axis=0)
        top_sw_IC=np.mean(top_sw_IC,axis=0)
        bot_sw_IC=np.mean(bot_sw_IC,axis=0)
        #-----------------------------------------------------------------------------
        ## Plotting zonal band feedbacks
        #-----------------------------------------------------------------------------
        ax[0].scatter(xscale,feed_lw,marker='.',color='black')
        ax[1].scatter(xscale,feed_sw,marker='.',color='black')
        #-----------------------------------------------------------------------------
        ## Coloring confidence interval feedbacks for observations
        #-----------------------------------------------------------------------------
        for j,i in enumerate(xscale):
            ax[0].fill_between(np.linspace(vlines[j],vlines[j+1]),bot_lw_IC[j],top_lw_IC[j], color='black', alpha=0.3,label='Observations')
            ax[1].fill_between(np.linspace(vlines[j],vlines[j+1]),bot_sw_IC[j],top_sw_IC[j], color='black', alpha=0.3)
        ax[0].vlines(x=vlines,ymin=-30,ymax=30,linestyle='-', color='black', lw=1,alpha=0.05)
        ax[1].vlines(x=vlines,ymin=-30,ymax=30,linestyle='-', color='black', lw=1,alpha=0.05)
        exps=[]
        names=''
        #-----------------------------------------------------------------------------
        ## Simulations
        #-----------------------------------------------------------------------------
        for experiment,name in zip(('CMIP6_historical','AMIP'),('CMIP','AMIP')):
            names=names+name
            exps.append(experiment)
            for exp in exps:
                models=[]
                #-----------------------------------------------------------------------------
                ## Retrieving model nammes and setting their colors.
                #-----------------------------------------------------------------------------
                for i in glob.glob(input+exp+'/*'):
                    models.append(i.replace('/home/alejandro/CL_feedbacks/data/'+exp+'/',''))
                if exp=='CMIP6_4xCO2':
                    c='magenta'
                elif exp=='CMIP6_historical':
                    c='blue'
                elif exp=='AMIP':
                    c='red'
                mean_mod_lw=[];mean_mod_sw=[]
                for k,mod in enumerate(models):
                    m_lw=[];bot_lw_IC=[];top_lw_IC=[];m_sw=[];bot_sw_IC=[];top_sw_IC=[]
                    #-----------------------------------------------------------------------------
                    ## Reading and averaging hemispherical data (simulations)
                    #-----------------------------------------------------------------------------
                    for H in ('North', 'South'):
                        DATA = np.load(input_data+'CI_Feed_Ftropics_'+Ty_sky+'_NOSI_NOI_'+H+'_Had5_V2.npz')
                        m_lw.append(DATA[exp+'_'+mod+'_m_lw_'+domain])
                        bot_lw_IC.append(DATA[exp+'_'+mod+'_lw_IC_min_'+domain])
                        top_lw_IC.append(DATA[exp+'_'+mod+'_lw_IC_max_'+domain])
                        m_sw.append(DATA[exp+'_'+mod+'_m_sw_'+domain])
                        bot_sw_IC.append(DATA[exp+'_'+mod+'_sw_IC_min_'+domain])
                        top_sw_IC.append(DATA[exp+'_'+mod+'_sw_IC_max_'+domain])
                    m_lw=np.mean(m_lw,axis=0)
                    bot_lw_IC=np.mean(bot_lw_IC,axis=0)
                    top_lw_IC=np.mean(top_lw_IC,axis=0)
                    m_sw=np.mean(m_sw,axis=0)
                    bot_sw_IC=np.mean(bot_sw_IC,axis=0)
                    top_sw_IC=np.mean(top_sw_IC,axis=0)
                    mean_mod_lw.append(m_lw)
                    mean_mod_sw.append(m_sw)
                    for j,i in enumerate(xscale):
                        xtick_mo=vlines[j]+(vlines[j+1]-vlines[j])*k/(len(models))
                        #-----------------------------------------------------------------------------
                        ## Plotting zonal band feedbacks for each model
                        #-----------------------------------------------------------------------------
                        ax[0].scatter(xtick_mo,m_lw[j],marker='.',color=c,linewidth=0.1, alpha=0.2)
                        ax[1].scatter(xtick_mo,m_sw[j],marker='.',color=c,linewidth=0.1, alpha=0.2)
                        #-----------------------------------------------------------------------------
                        ## Plotting zonal band feedbacks confidence interval for each model
                        #-----------------------------------------------------------------------------
                        ax[0].plot([xtick_mo,xtick_mo],[bot_lw_IC[j],top_lw_IC[j]],color=c, linewidth=0.5, alpha=0.2)
                        ax[1].plot([xtick_mo,xtick_mo],[bot_sw_IC[j],top_sw_IC[j]],color=c, linewidth=0.5, alpha=0.2)
                mean_lw=np.mean(mean_mod_lw,axis=0)
                mean_sw=np.mean(mean_mod_sw,axis=0)
            #-----------------------------------------------------------------------------
            ## Computing model mean confidence intervals.
            #-----------------------------------------------------------------------------
            CI_LW=st.t.interval(alpha=0.95, df=len(mean_mod_lw)-1, loc=np.mean(mean_mod_lw,axis=0), scale=st.sem(mean_mod_lw)) 
            CI_SW=st.t.interval(alpha=0.95, df=len(mean_mod_sw)-1, loc=np.mean(mean_mod_sw,axis=0), scale=st.sem(mean_mod_sw)) 
            #-----------------------------------------------------------------------------
            ## Coloring confidence interval feedbacks for mean simulations
            #-----------------------------------------------------------------------------
            for j,i in enumerate(xscale):
                ax[0].fill_between(np.linspace(vlines[j],vlines[j+1]),CI_LW[0][j],CI_LW[1][j], color=c, alpha=0.3,label=name)
                ax[1].fill_between(np.linspace(vlines[j],vlines[j+1]),CI_SW[0][j],CI_SW[1][j], color=c, alpha=0.3)
            #-----------------------------------------------------------------------------
            ## Ploting model mean feedbacks
            #-----------------------------------------------------------------------------
            ax[0].scatter(xscale,mean_lw,marker='.',linewidth=2,color=c)
            print('model SW '+name+' '+tit)
            print(np.round(mean_sw,1))
            print(np.round(mean_sw-CI_SW,1))
            #-----------------------------------------------------------------------------
            ## Defining plot parameters
            #-----------------------------------------------------------------------------
            ax[1].scatter(xscale,mean_sw,marker='.',linewidth=2,color=c)
            ax[0].hlines(y=0, xmin=-1, xmax=10,linestyle='--', color='black', lw=1)
            ax[1].hlines(y=0, xmin=-1, xmax=10,linestyle='--', color='black', lw=1)
            ax[0].spines['right'].set_color('none')
            ax[0].spines['top'].set_color('none')
            ax[1].spines['right'].set_color('none')
            ax[1].spines['top'].set_color('none')
            ax[0].set_title('Longwave feedback')
            ax[0].legend(*[*zip(*{l:h for h,l in zip(*ax[0].get_legend_handles_labels())}.items())][::-1],loc=1,frameon=False)
            ax[1].set_title('Shortwave feedback')
            ax[0].set_xlim(2*xscale[0]-vlines[1],1.01)
            ax[0].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            ax[0].set_xticks(vlines)
            ax[0].set_xticklabels(intervals)
        #-----------------------------------------------------------------------------
        ## Removing extra labels
        #-----------------------------------------------------------------------------
        for label in ax[0].get_xaxis().get_ticklabels()[0::2]:
            label.set_visible(False)
        for label in ax[1].get_xaxis().get_ticklabels()[0::2]:
            label.set_visible(False)
        fig.tight_layout()
        #-----------------------------------------------------------------------------
        ## Saving figure as png
        #-----------------------------------------------------------------------------
        plt.savefig('/home/alejandro/CL_feedbacks/plots/paper/sin/mod_feedbacks_local_'+Ty_sky+'_'+domain+'.png', dpi=300)