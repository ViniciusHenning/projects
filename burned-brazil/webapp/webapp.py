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
	df2014 = pd.read_csv('df2014.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2015 = pd.read_csv('df2015.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2016 = pd.read_csv('df2016.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2017 = pd.read_csv('df2017.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2018 = pd.read_csv('df2018.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2019 = pd.read_csv('df2019.csv', parse_dates = True, index_col = 'Unnamed: 0')
	df2020 = pd.read_csv('df2020.csv', parse_dates = True, index_col = 'Unnamed: 0')

	df2014_loc = pd.read_csv('df2014_loc.csv')
	df2015_loc = pd.read_csv('df2015_loc.csv')
	df2016_loc = pd.read_csv('df2016_loc.csv')
	df2017_loc = pd.read_csv('df2017_loc.csv')
	df2018_loc = pd.read_csv('df2018_loc.csv')
	df2019_loc = pd.read_csv('df2019_loc.csv')
	df2020_loc = pd.read_csv('df2020_loc.csv')

	dict_year = {2014 : df2014, 2015 : df2015, 2016 : df2016, 2017 : df2017 , 2018 : df2018 , 2019 : df2019, 2020 : df2020}
	dict_year_loc = {2014 : df2014_loc, 2015 : df2015_loc, 2016 : df2016_loc, 2017 : df2017_loc , 2018 : df2018_loc , 2019 : df2019_loc, 2020 : df2020_loc}

	if condition == 'all':
		return dict_year, dict_year_loc

dict_year = data('all')[0]
dict_year_loc = data('all')[1]
dfmap = pd.read_csv('dfmap.csv')


## Creating the  variables for the biome plot

############################################################################################################################################
## Starting the app configuration

st.subheader('Choose an **year** to be analyzed')

year = st.slider('Years', min_value = 2014, max_value = 2020) ## Getting the year by the use

fire_brazil_loc = FireBrazil(dict_year_loc[year], year)
st.write('### The fire distribution in Brazil during {}'.format(year))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,6))

@st.cache(suppress_st_warning = True)
def biomes_distribution(dfmap, ax1):
	return fire_brazil_loc.biomes_distribution(ax1, dfmap)	

@st.cache(suppress_st_warning=True)
def fire_dist_brazil(year):
	fire_map = fire_brazil_loc.fire_map_dist(ax2)
	plt.colorbar(fire_map[1], ax = ax2)

fig1 = st.pyplot(fig)


first_figure(year)

st.write('### Individual biome analysis in {}'.format(year))


biome = st.selectbox('Brazilian biomes', ['Amazonia', 'Caatinga', 'Cerrado','Mata Atlantica', 'Pampa', 'Pantanal'])

## Creating the composed plot using gridspec

@st.cache(suppress_st_warning=True)
def second_figure(year, biome):
	fire_brazil = FireBrazil(dict_year[year], year)
	fire_brazil_loc = FireBrazil(dict_year_loc[year], year)

	fig = plt.figure(constrained_layout = False, figsize = (28, 12))
	gs = fig.add_gridspec(nrows = 6, ncols = 2, left = 0.05, right = 0.48, wspace = 0.2, hspace = 1.5)
	ax1 = fig.add_subplot(gs[:3, :1])
	ax2 = fig.add_subplot(gs[:3, 1:])
	ax3 = fig.add_subplot(gs[3:, :])

	fire_brazil.pie_chart_year(biome, ax = ax1)
	fire_biome_plot = fire_brazil_loc.fire_biome(biome, ax2, dfmap)[1]
	fig.colorbar(fire_biome_plot, ax = ax2)
	fire_brazil.timeseries_year_biome(biome, ax = ax3, position = [0.08, 0.34, .08, .12])

	st.pyplot(fig)


second_figure(year, biome)


















