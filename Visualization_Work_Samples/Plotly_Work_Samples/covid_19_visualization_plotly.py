# -*- coding: utf-8 -*-
"""Covid-19_Visualization_Plotly.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mazVI3oZoOQSn9LephFPr4O8TNZ2k7sW

## Data import
"""

from google.colab import files
import io
uploaded = files.upload()

import pandas as pd
import io
import pandas_profiling

df_covid=pd.read_csv('covid_19_data.csv')

"""## Summarizing dataset"""

pandas_profiling.ProfileReport(df_covid)

""" ## importing necessary libraries for maps


"""

import plotly.express as px
import plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import init_notebook_mode,plot,iplot
import datetime as dt

"""## Preprocessing dataset"""

df_covid['Country/Region'][df_covid['Country/Region'] == 'Mainland China']='China'

df_covid['ObservationDate']=pd.to_datetime(df_covid['ObservationDate'])

"""## group by countries and sorting the dataframe on date"""

df_covid.sort_values(by=['Country/Region'],inplace=True)
df_covid=df_covid.groupby(['Country/Region'])
df_covid=df_covid.apply(lambda x: x.sort_values(['ObservationDate'], ascending=True)).reset_index(drop=True)
df_covid.head()

df_covid_19=df_covid[['ObservationDate','Country/Region','Confirmed','Deaths','Recovered']]
df_covid_19.columns=['ObservationDate','Country','Confirmed','Deaths','Recovered']
df_covid_19.head()

df_covid_cases=df_covid_19.groupby(['Country','ObservationDate'])['Confirmed','Deaths','Recovered'].sum().reset_index()
df_covid_cases.tail(10)

df_covid_cases['ObservationDate']=df_covid_cases['ObservationDate'].astype(str)

map_fig=px.choropleth(df_covid_cases,locations='Country',locationmode='country names',color='Confirmed',animation_frame='ObservationDate',projection='natural earth',color_continuous_scale='OrRd')
map_fig.update_layout(title='World Wide Confirmed Cases')
map_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
map_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10
map_fig.show()

sca_fig=px.scatter_geo(df_covid_cases,locations='Country',locationmode='country names',color='Recovered',size='Recovered',animation_frame='ObservationDate',hover_name='Country',projection='natural earth',color_continuous_scale='Tealgrn')
sca_fig.update_layout(title='World Wide Recovered Cases')
sca_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
sca_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
sca_fig.show()

sca_fig=px.scatter_geo(df_covid_cases,locations='Country',locationmode='country names',color='Deaths',size='Deaths',animation_frame='ObservationDate',hover_name='Country',projection='natural earth',color_continuous_scale='Reds')
sca_fig.update_layout(title='World Wide Deaths',template='plotly_dark')
sca_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
sca_fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
sca_fig.show()

