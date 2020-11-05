## THE CORRESPONDING PIE CHART

def pie_chart_year(ax, year, biome):
    
    biomes = ['Amazonia', 'Mata Atlantica', 'Cerrado', 'Pampa', 'Caatinga', 'Pantanal']
    burn_ev = []
    
    ## COUNTING THE NUMBER OF BURNING EVENTS PER BIOME FOR AN SPECIFIC YEAR    
    for biome_for_loop in biomes:
        filename = 'cleaned-datasets/peryear{}{}.csv'.format(str(year), biome_for_loop)
        df = pd.read_csv(filename, usecols = ['riscofogo'])
        burn_ev.append(len(df.index))    
    
    ## EXPLODING THE DESIRED BIOME
    
    index = biomes.index(biome)
    explode = [0, 0, 0, 0.1, 0, 0]
    explode[index] = 0.1
    
    ## PLOTTING
    colors = ['indianred', 'yellowgreen', 'cadetblue', 'black', 'lightsteelblue', 'bisque']
    
    ax.pie(burn_ev, labels = biomes, autopct='%1.1f%%',
           explode = explode, startangle=-90, colors = colors)
    ax.axis('equal')
    ax.set_title('Number of burning events \nper biome in {}'.format(year),
                 fontsize = 16)
    
    #ADDING A WHITE CIRCLE AT THE CENTER (DONUT CHART)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax.add_patch(centre_circle)
    
    return ax
