import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
from fire_events import FireBrazil

sns.set_theme(style="darkgrid")

import streamlit as st

st.title('Fire events in Brazil app')

## Loading the dataset

@st.cache
def data(condition):
    df2014 = pd.read_csv('../datasets/df2014.csv')
    df2014 = pd.read_csv('../datasets/df2014.csv', parse_dates = True, index_col = 'datahora')
    df2015 = pd.read_csv('../datasets/df2015.csv', parse_dates = True, index_col = 'datahora')
    df2016 = pd.read_csv('../datasets/df2016.csv', parse_dates = True, index_col = 'datahora')
    df2017 = pd.read_csv('../datasets/df2017.csv', parse_dates = True, index_col = 'datahora')
    df2018 = pd.read_csv('../datasets/df2018.csv', parse_dates = True, index_col = 'datahora')
    df2019 = pd.read_csv('../datasets/df2019.csv', parse_dates = True, index_col = 'datahora')
    df2020 = pd.read_csv('../datasets/df2020.csv', parse_dates = True, index_col = 'datahora')
    dict_year = {2014 : df2014, 2015 : df2015, 2016 : df2016, 2017 : df2017 , 2018 : df2018 , 2019 : df2019, 2020 : df2020}
    if condition == 'all':
        return dict_year

dict_year = data('all')



## Creating the  variables for the biome plot

############################################################################################################################################
## Starting the app configuration

st.subheader('Choose an **year** to be analyzed')
year = st.slider('Years', min_value = 2014, max_value = 2020) ## Getting the year

@st.cache
def df_function(year):
    return dict_year[year]					      ## Getting the corresponding dataframe in cache

df = df_function(year)					         ## Getting the corresponding dataframe

@st.cache
def fire_brazil_cache(df, year):
    return FireBrazil(df, year)
fire_brazil = fire_brazil_cache(df, year)

st.write('### The fire distribution in Brazil during {}'.format(year))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,6))

fire_brazil.biomes_distribution(ax1, dict_year[2014])
fire_map = fire_brazil.fire_map_dist(ax2)

plt.colorbar(fire_map[1], ax = ax2)

fig1 = st.pyplot(fig)


st.write('### Individual biome analysis in {}'.format(year))


biome = st.selectbox('Brazilian biomes', ['Amazonia', 'Caatinga', 'Cerrado','Mata Atlantica', 'Pampa', 'Pantanal'])

## Creating the composed plot

fig = plt.figure(constrained_layout = False, figsize = (28, 12))
gs = fig.add_gridspec(nrows = 6, ncols = 2, left = 0.05, right = 0.48, wspace = 0.2, hspace = 1.5)
ax1 = fig.add_subplot(gs[:3, :1])
ax2 = fig.add_subplot(gs[:3, 1:])
ax3 = fig.add_subplot(gs[3:, :])

fire_brazil.pie_chart_year(biome, ax = ax1)
fire_biome_plot = fire_brazil.fire_biome(biome, ax2, dict_year[2014])[1]
fig.colorbar(fire_biome_plot, ax = ax2)
fire_brazil.timeseries_year_biome(biome, ax = ax3, position = [0.08, 0.34, .08, .12])

st.pyplot(fig)
