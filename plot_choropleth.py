import os
import pickle
import pandas as pd
import geopandas as gpd
import json
from bokeh.io import output_notebook, show, output_file, save
from bokeh.plotting import figure, output_file, show
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.resources import CDN
from bokeh.embed import autoload_static

def geoplot():
    '''
    This function is used to plot choropleth
    of countries according to the obesiry data.
    '''

    shapefile = './data/countries_110m/ne_110m_admin_0_countries.shp'
    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    
    index = gdf[gdf['country'] == 'Antarctica'].index.values.astype(int)
    gdf = gdf.drop(index.astype(int))
    
    datafile = './data/obesity.csv'
    #Read csv file using pandas
    df = pd.read_csv(datafile, names = ['entity', 'code', 'year', 'per_cent_obesity'], skiprows = 1)
    #Change NULL data for SUDAN with 0
    df.loc[df['code'].isnull()] = 'SDN'
    df_2016 = df[df['year'] == 2016]
    merged = gdf.merge(df_2016, left_on = 'country_code', right_on = 'code', how = 'left')
    
    #Read data to json.
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)
    palette = brewer['YlGnBu'][8]
    palette = palette[::-1]
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40)
    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    p = figure(title = 'Share of adults who are obese', plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.title.text_font_size = '17pt'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'per_cent_obesity', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    p.add_layout(color_bar, 'below')
    p.axis.visible = False
    output_notebook()
    #Display figure.
    show(p)

#https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0
