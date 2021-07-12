import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt

'''
The intetion is to visualize all petrol stations which are given in the Data Set.
We are going to use a simple geo plot in form of a map of germany as basline with the 
borders of all federal states.
The petrol station are plotted than as scatter-points regarding their locations.
We take into account that some listed petrol station are no more extant. Those
of them we  do ignore.
'''




### load DataFrame of all stations with their geo- and metadata
df_stations = pd.read_csv('../__DATA__/GPS_META_Stations/stations.csv')

### load the list of petrol station those are not extant
df_not_extant_stations = pd.read_csv('../welche_Tankstellen_sind_aktuell/not_extant_petrol_stations.csv')



### we transform that DataFrame into GeoPandasDataFrame
df_stations = gpd.GeoDataFrame(
        df_stations, 
        geometry=gpd.points_from_xy(df_stations.longitude, df_stations.latitude)
    ).drop(['longitude', 'latitude'], axis=1)
    
  
print('Number of all Data Tuples : ',len(df_stations))
  
### we load here a GeoPandasdataFrame representing the federally staates of germany based on 
### a SHP-file taken from ESRI
shp_path      = '../__DATA__/SHP_data/germany_border_esri/Bundesländer_2017_mit_Einwohnerzahl.shp'
state_borders = gpd.read_file(shp_path)

### we set here the projection-scheme to WGS84 to be able to visualize GPS-data in further part
state_borders = state_borders.to_crs(4326)




#### Some cleansing

# we remove here all gas station which are no more extant
df_stations = df_stations[~df_stations['uuid'].isin(list(df_not_extant_stations['name']))]


### Since there is a point that is not within the border of germany, we have to take it out.
### we remove here all GPS-Points which not belong to the observation area

# compute the boundaray of the given SHP-file/GeoPandasDataFrame
# we use the boundary as criterion to check if a GPS-Point is valid (is within boundary) 
# or not
polygon  = state_borders.geometry.unary_union
boundary = gpd.GeoDataFrame(geometry=[polygon], crs=state_borders.crs)

# we remove here all invalid gas stations by check if their coordinate is within the 
# boundray
df_stations = df_stations.where(
    df_stations.geometry.apply(lambda pnt : pnt.within(boundary.geometry[0]))
)
df_stations = df_stations.drop(df_stations[df_stations.geometry==None].index)



print('Number of all Data Tuples after cleansing: ',len(df_stations))

################################## PLOT SECTIONS ######################################

size_fac = 6.5

fig, ax = plt.subplots(figsize=(size_fac, size_fac))

### we do plot here all borders of the federal states of germany 
state_borders.plot(color='blue', alpha=0.15, edgecolor='black', ax=ax, linewidth=0.5)

### we plot here the border of germany to get a better look
boundary.boundary.plot(ax=ax, edgecolor='k', linewidth=0.8, alpha=0.6)


state_borders.plot(facecolor='none', linewidth=0.2, edgecolor='black', alpha=0.6, ax=ax)



### we scatter here all locations of given gas stations as scatters into the map
df_stations.plot(
    ax = ax, 
    markersize = 6, 
    color = 'blue', 
    marker = '.', 
    alpha=0.3, 
    label = 'Petrol Station',
)


### we set here the title of the plot figure
ax.set_title('All Petrol Stations contained in the given Data Set') 

### we set off here frame and axes of the plot figure
fig.patch.set_visible(False)
ax.axis('off')

# we set here the aspect ratio to get a better look 
ax.set_aspect(aspect=1.5)

# we set here to get a legend
ax.legend(loc=3)
plt.show()