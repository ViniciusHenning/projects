## THIS FUNCTION PLOTS THE BURNING EVENTS THROUGHOUT THE CONTRY FOR A GIVEN YEAR

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
import time

def burning_given_year(year, ax1, ax2, fig):
    
    filename = '../cleaned-datasets/entire_country{}.csv'.format(str(year))
    df = pd.read_csv(filename,
                     parse_dates = [0])
    
    ## Rounding the numbers for better visualization
    df = df.round(0)

    ## CREATING A NEW SIMPLE DF WITH THE PERTINENT INFORMATION
    df_loc_gb = df.groupby(['latitude', 'longitude'])

    number_events = []
    lat = []
    long = []

    for info, dataframe in df_loc_gb:
        lat.append(info[0])
        long.append(info[1])
        number_events.append(len(dataframe))
    
    ##THE DATAFRAME ITSELF
    blaze_df = pd.DataFrame()

    blaze_df['latitude']= lat
    blaze_df['longitude'] = long
    blaze_df['number_events'] = number_events

    plot = ax1.scatter(x = long, y = lat, c = blaze_df.number_events/1000, cmap = 'cividis_r')
    ax1.set_title('Burning events in {} \nin Thousands'.format(year), fontsize = 16)
    ax1.set_xlabel('Latitude', fontsize = 14)
    ax1.set_ylabel('Longitude', fontsize = 14)

    ## EDITTING THE COLOR BAR POSITION

    position = fig.add_axes([0.46, 0.125, 0.015, 0.755])

    plt.colorbar(plot, cax=position)

    plt.subplots_adjust(wspace = 0.35)
    
    
    ## Brazil map per biome

    ax2.set_xlabel('Latitude', fontsize = 14)
    ax2.set_ylabel('Longitude', fontsize = 14)
    
    df = pd.read_csv('../cleaned-datasets/data-map.csv')
    
    biomes = ['Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal']
    colors = ['indianred', 'yellowgreen', 'cadetblue', 'mediumpurple', 'lightsteelblue', 'bisque']
    
    color_dict = dict(zip(biomes, colors))
    
    biome_gb = df.groupby('bioma')

    for biome_name, df in biome_gb:
        ax2.plot(df.longitude, df.latitude, marker = 'o',
                 label = biome_name, linestyle='', c = color_dict[biome_name])

    ax2.set_title('Brazilian biomes', fontsize = 14)
    ax2.legend(loc = 'lower left')
    
    return ax1, ax2
