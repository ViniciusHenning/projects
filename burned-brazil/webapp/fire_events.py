class FireBrazil:
    def __init__(self, year):
        self.year = year

    def fire_map_dist(self, ax):
        ## getting the dataframe and risk of fire = 1

        df = dict_year[self.year].drop(columns = ['bioma', 'precipitacao'])
        df = df[df.riscofogo == 1].round(0)

        ## Grouping by latitude, longitude and counting the number of fire events
        fire_loc_gb = df.groupby(['latitude', 'longitude'])

        number_events = []
        lat = []
        long = []

        for info, dataframe in fire_loc_gb:
            lat.append(info[0])
            long.append(info[1])
            number_events.append(len(dataframe))

        ## Creating the dataframe with these information
        df_fire_loc = pd.DataFrame()

        df_fire_loc['latitude'] = lat
        df_fire_loc['longitude'] = long
        df_fire_loc['number_events'] = number_events

        scatter = ax.scatter(x = df_fire_loc.longitude, y = df_fire_loc.latitude,
                             c = df_fire_loc.number_events/1000,
                             cmap = 'copper_r')#gnuplot_r
        ax.set_title('Fire events during {} \nin Thousands'.format(self.year), fontsize = 16)
        ax.set_xlabel('Latitude', fontsize = 14)
        ax.set_ylabel('Longitude', fontsize = 14)

        return ax, scatter

    def biomes_distribution(self, ax):
        ## Looping through the biomes
        for biome_name, df in gb_biome:
            ax.plot(df.longitude, df.latitude, marker = '*',
            label = biome_name, linestyle = '', c = color_dict[biome_name])

        ax.set_xlabel('Latitude', fontsize = 14)
        ax.set_ylabel('Longitude', fontsize = 14)
        ax.set_title('Brazilian biomes', fontsize = 16)
        ax.legend(loc = 'lower left')

        return ax

    def pie_chart_year(self, biome, ax):

        biomes = ['Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal']
        fire_biome = []

        df = dict_year[self.year][['bioma', 'riscofogo']].copy()
        df = df[df.riscofogo == 1]

        ## COUNTING THE NUMBER OF BURNING EVENTS PER BIOME FOR AN SPECIFIC YEAR

        for biome_for in biomes:
            fire_biome.append(len(df[df.bioma == biome_for]))

        ## EXPLODING THE DESIRED BIOME

        index = biomes.index(biome)
        explode = [0, 0, 0, 0.1, 0, 0]
        explode[index] = 0.1

        ## PLOTTING
        colors = ['indianred', 'yellowgreen', 'cadetblue', 'black', 'lightsteelblue', 'bisque']

        ax.pie(fire_biome, labels = biomes, autopct = '%1.1f%%',
               explode = explode, startangle=-90, colors = colors)
        ax.axis('equal')
        ax.set_title('Number of burning events \nper biome in {}'.format(self.year),
                     fontsize = 16)

        #ADDING A WHITE CIRCLE AT THE CENTER (DONUT CHART)
        centre_circle = plt.Circle((0,0),0.70,fc = 'white')
        ax.add_patch(centre_circle)

        return ax
    
    def fire_biome(self, biome, ax):
        ## Looping through the biomes
        for biome_name, df in gb_biome:
            if biome_name != biome:
                ax.plot(df.longitude, df.latitude, marker = '*',
                label = biome_name, linestyle = '', c = color_dict[biome_name])

        ax.set_xlabel('Latitude', fontsize = 14)
        ax.set_ylabel('Longitude', fontsize = 14)
        ax.set_title('Fire events distribution in {} \nduring {}'.format(biome, self.year), fontsize = 16)
        ax.legend(loc = 'lower left')

        ## Plotting the specified biome
        df = dict_year[self.year][['latitude', 'riscofogo', 'longitude', 'bioma']].copy().round(1)
        df = df[(df.riscofogo == 1) & (df.bioma == biome)].copy()

        gb_loc = df.groupby(['latitude', 'longitude'])

        latitude = []
        longitude = []
        number_events = []

        for info, dataframe in gb_loc:
            latitude.append(info[0])
            longitude.append(info[1])
            number_events.append(dataframe.riscofogo.sum())

        ax.set_xlabel('Latitude')
        ax.set_ylabel('Longitude')

        plot = ax.scatter(x = longitude, y = latitude, c = number_events, cmap = 'magma_r')

        return ax, plot

    def timeseries_year_biome(self, biome, ax, day1 = 0, day2 = 0, month1 = 0, month2 = 0, position = [0.2, 0.6, .2, .2]):
        df = dict_year[self.year][['riscofogo', 'precipitacao', 'bioma']].copy()

        # electing the chosen biome
        df = df[df.bioma == biome]
        df = df.drop(columns = 'bioma')

        # fire vector
        df_fire = df[df['riscofogo'] == 1]['riscofogo'].copy()
        df_fire = df_fire.resample('D').sum()

        # precipitation vector
        df_prec = df['precipitacao'].resample('D').mean()

        ### PLOTTING SECTION ###

        ## Fire events plot##
        ax.plot(df_fire, alpha = 0.5, c = 'red')

        ax.set_xlabel('Months', fontsize = 14)
        ax.set_xlim(df_fire.index[0], df_fire.index[-1])
        ax.set_title('Number of fire events in Brazil\n in {} at the {}'.format(self.year, biome),
                     fontsize = 16)

        plt.gcf().autofmt_xdate()

        if day1 != 0 and day2 != 0 and month1 != 0 and month2 != 0:
            x1 = datetime.date(year, month1, day1)
            x2 = datetime.date(year, month2, day2)
            ax.axvspan(x1, x2, color='gray', alpha=0.2, lw=0)

        ## Mean precipitation plot ##
        ax_inset = plt.axes(position)
        ax_inset.plot(df_prec)
        ax_inset.set_xlim(df_prec.index[0], df_prec.index[-1])

        ax_inset.set_title('Mean \nprecipitation')
        ax_inset.set_xticks([])

        if day1 != 0 and day2 != 0 and month1 != 0 and month2 != 0:
            ax.axvspan(x1, x2, color='gray', alpha=0.2, lw=0)

        return ax