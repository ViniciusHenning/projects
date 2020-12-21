## THIS FUNCTION RETURNS A TIME SERIES FOR THE BURNING EVENTS AND PRECIPITATION ALONG THE YEAR

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
import time

def biome_plot(ax, year, biome, rolling_mean = 3,
               day1 = 31, day2 = 20, month1 = 7, month2 = 11, inset_location = [0.2, 0.6, .2, .2]):
    
    ## BURNED DATAFRAME FOR AN SPECIFIC BIOME
    filename = '../cleaned-datasets/timeseries{}{}.csv'.format(str(year), biome)
    df = pd.read_csv(filename, parse_dates = [0], usecols = ['datahora', 'riscofogo'])
    
    df_prec = pd.read_csv('../../../dataset/data{}.csv'.format(year), usecols = ['precipitacao', 'bioma', 'datahora'],
                          index_col = 'datahora', parse_dates = True)
    
    df_prec = df_prec[df_prec.bioma == biome]
    df_prec = df_prec.resample('W').mean()
    
    #print(df_prec)
    
    ## PLOTTING SECTION ##
    
    ax.set_xlabel('Date', fontsize = 16)
    ax.set_ylabel('Number of events', fontsize = 16)
    ax.set_title('Number of burning incidents in Brazil\n at the {} in {}'.format(biome, year),
                 fontsize = 16)

    #plt.xticks(rotation = 45)
    ax.set_xlim(datetime.date(year, 1, 1), datetime.date(year, 12, 31) )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
    plt.xticks(rotation = 45)

    x1 = datetime.date(year, month1, day1)
    x2 = datetime.date(year, month2, day2)
    
    
    ax.axvspan(x1, x2, color='gray', alpha=0.2, lw=0)

    ax.plot(df.datahora, df.riscofogo,
    c = 'salmon')
    
    ax_inset = plt.axes(inset_location)
    ax_inset.set_xlim(datetime.datetime(year,1,1), datetime.datetime(year, 12, 31))
    ax_inset.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax_inset.plot(df_prec.index, df_prec.precipitacao)
    
    
    
    ax_inset.axvspan(x1, x2, color='gray', alpha=0.3, lw=0)
        
    plt.xticks(rotation = 45)
    plt.title('Precipitation')

    return ax
