import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
import time

st.title('Burning events in Brazil App')

st.write("## **Single year analysis**")

## Assigning the year choosen by the user to the variable "year"

st.sidebar.write("# **Single year analysis**")

year = st.sidebar.slider("Year", 2014, 2020)


## Assigning the biome choosen by the user to the variable "biome"

biome = st.sidebar.selectbox('Choose a biome', ('Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal'))



#######################################################################################################

### PYTHON CODE FOR THE PERTINENT PLOTS ###

## burning events throughout the country for a given year - 1st part ##

st.write("### Burning events throughout Brazil for an specific year")


with st.spinner('That is a big amount of data! Wait a minute...'):
	time.sleep(0.1)


def burning_given_year(year, ax1, ax2, fig):
    
    filename = '../cleaned-datasets/timeseries{}.csv'.format(str(year))
    df = pd.read_csv(filename,
                     parse_dates = [0])
    
    df = df[df.riscofogo == 1]
    
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
    
    biome_gb = df.groupby('bioma')

    plot = ax1.scatter(x = long, y = lat, c = blaze_df.number_events/1000, cmap = 'magma_r')
    ax1.set_title('Burning events in {} \nin Thousands'.format(year), fontsize = 18)
    ax1.set_xlabel('Latitude', fontsize = 14)
    ax1.set_ylabel('Longitude', fontsize = 14)

    ## EDITTING THE COLOR BAR POSITION

    position = fig.add_axes([0.46, 0.125, 0.015, 0.755])

    plt.colorbar(plot, cax=position)

    plt.subplots_adjust(wspace = 0.35)
    
    
    ## Brazil map per biome

    ax2.set_xlabel('Latitude', fontsize = 14)
    ax2.set_ylabel('Longitude', fontsize = 14)
    
    mpl.rcParams['agg.path.chunksize'] = 10000
    
    df = pd.read_csv('../cleaned-datasets/data-map.csv')
    
    biomes = ['Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal']
    colors = ['indianred', 'yellowgreen', 'cadetblue', 'mediumpurple', 'lightsteelblue', 'bisque']
    
    color_dict = dict(zip(biomes, colors))
    
    biome_gb = df.groupby('bioma')

    for biome_name, df in biome_gb:
        ax2.plot(df.longitude, df.latitude, marker = 'o',
                 label = biome_name, linestyle='', c = color_dict[biome_name])

    ax2.set_title('Brazilian biomes', fontsize = 18)
    ax2.legend(loc = 'lower left')
    
    return ax1, ax2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,6))

burning_given_year(year, ax1, ax2, fig)

st.pyplot(fig)
#######################################################################################################

