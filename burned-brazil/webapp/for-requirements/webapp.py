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

#######################################################################################################

### IMPORTING THE FUNCTIONS ###

from burning_given_year import burning_given_year as entire_country
from burning_specific_biome import burning_map_brazil as specific_biome_year
from piechart import pie_chart_year as piechart
from time_series import biome_plot as time_series

#######################################################################################################

st.title('Burning events in Brazil App')

st.write("## **Single year analysis**")

## Assigning the year choosen by the user to the variable "year"

st.sidebar.write("# **Single year analysis**")

year = st.sidebar.slider("Year", 2014, 2020)



#######################################################################################################

### PYTHON CODE FOR THE PERTINENT PLOTS ###

## burning events throughout the country for a given year - 1st part ##

st.write("### Burning events throughout Brazil for an specific year")


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,6))

entire_country(year, ax1, ax2, fig)

st.pyplot(fig)

#######################################################################################################


## Assigning the biome choosen by the user to the variable "biome"

biome = st.sidebar.selectbox('Choose a biome', ('Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal'))


#######################################################################################################

## burning events throughout the country for a given year and specific biome - 2nd part ##

st.write("### Burning events for an specific year and biome")


fig = plt.figure(figsize = (18,15))

gs = fig.add_gridspec(2, 2, hspace = 0.4)

ax1 = fig.add_subplot(gs[0, :-1])
ax2 = fig.add_subplot(gs[0,-1])
ax3 = fig.add_subplot(gs[1, :])

specific_biome_year(ax1, year, biome, fig, cbar_location = [0.46, 0.565, 0.01, 0.315],)
piechart(ax2, year, biome)
time_series(ax3, year, biome, inset_location = [0.2, 0.25, .16, .13])

st.pyplot(fig)

#######################################################################################################

## Assigning the year choosen by the user to the variable "year"

st.sidebar.write("# **Several years analysis**")

