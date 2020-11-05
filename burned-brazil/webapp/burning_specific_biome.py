## THIS FUNCTION RETURNS THE BURNING DISTRIBUTION IN THE BRAZIL MAP FOR AN SPECIFIC BIOME AND YEAR

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
import time

def burning_map_brazil(ax, year, biome, fig, cbar_location = [0.92, 0.1, 0.015, 0.78]):
        
    df_map = pd.read_csv('../cleaned-datasets/data-map.csv')
    
    filename = '../cleaned-datasets/timeseries{}{}.csv'.format(str(year), biome)
    
    df = pd.read_csv(filename, parse_dates = [0], usecols = ['bioma', 'latitude', 'longitude'])
    
    gb_biome = df_map.groupby('bioma')

    ## CREATING THE INFORMATION RELATED TO DESIRED BIOME
    
    df['latitude'] = df['latitude'].round(1) 
    df['longitude'] = df['longitude'].round(1) 

    gb_loc = df.groupby(['latitude', 'longitude'])

    latitude = []
    longitude = []
    number_events = []

    for info, df in gb_loc:
        latitude.append(info[0])
        longitude.append(info[1])
        number_events.append(len(df))
    
    ## EDITING THE AXIS
    
    ax.set_xlabel('Latitude', fontsize = 14)
    ax.set_ylabel('Longitude', fontsize = 14)

    plot = ax.scatter(x = longitude, y = latitude, c = number_events, cmap = 'magma_r')
    
    biomes = ['Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal']
    colors = ['indianred', 'yellowgreen', 'cadetblue', 'mediumpurple', 'lightsteelblue', 'bisque']
    
    color_dict = dict(zip(biomes, colors))

    for biome_name, df in gb_biome:
        if biome_name != biome:
            ax.plot(df.longitude, df.latitude, marker = 'o', label = biome_name,
                    linestyle='', alpha = 0.4, c = color_dict[biome_name])

    ax.set_title('Brazilian biomes distribution and \nburning events at the {} in {}'.format(biome, str(year)) ,fontsize = 16)
    ax.legend(loc = 'lower left')

    ## EDITTING THE COLOR BAR POSITION

    position=fig.add_axes(cbar_location)

    fig.colorbar(plot, cax=position)

    plt.subplots_adjust(wspace = 0.35)

    return ax
