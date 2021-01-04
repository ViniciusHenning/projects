import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#import streamlit as st
import time



def several_years_biome(years, biome, ax1, ax2, fig):
    
    color_options = ['indianred', 'yellowgreen', 'cadetblue', 'darkkhaki', 'lightseagreen', 'bisque']
    colors = color_options[:len(years)]
    color_dict = dict(zip(years, colors))
    
    df_all_burned = pd.DataFrame(columns = ['datahora', 'bioma', 'ano', 'day_month'])
    
    for year in years:
        df = pd.read_csv('cleaned-datasets/timeseries{}{}.csv'.format(year, biome), usecols = ['datahora', 'bioma'], parse_dates = True)
		df['day_month'] = df['datahora'].dt.strftime('%m-%d')
		df['ano'] = df['datahora'].year
	    df_all_burned = df_all_burned.append(df, ignore_index = True)
   
    df_all_burned.set_index('datahora', inplace = True)

    df_all_burned.groupby(['ano', 'day_month']).count().unstack(level = 0)\
                    .plot(figsize = (14,6), ax = ax1, color = colors)
    
    title = 'Burning events for different years in {} - Brazil'.format(biome)
    ax1.set_title(title, fontsize = 16)
    ax1.set_xlabel('Months', fontsize = 14)
    ax1.set_ylabel('Number of Burning events')

    handles, labels = ax1.get_legend_handles_labels()

    ## EDITING THE LABELS
    import re
    new_labels = []
    
    for label in labels:
        new_labels.append(re.search(',\s(.+?)\)', label).group(1))

    ax1.legend(new_labels, fontsize = 14)

    ## ADJUSTING THE LOCATORS AND TICKS ##

    locs, labels = plt.xticks()

    plt.gcf().autofmt_xdate()
    ax1.set_xlim(-5,365)
    
    year_gb = df_all_burned.groupby('ano')

    years = []
    n_events = []
    for year, dataframe in year_gb:
        years.append(year)
        n_events.append(len(dataframe))

    ax2.pie(n_events, labels = years, autopct='%1.1f%%',shadow=True, startangle=-70, colors = colors)
    ax2.axis('equal')
    ax2.set_title('Number of burning events throughout\n the years in {}'.format(biome), fontsize = 18)
    plt.rcParams['font.size'] = 12
    
    ## ADDING THE CIRCLE
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax2.add_patch(centre_circle)

    return (ax1, ax2)
